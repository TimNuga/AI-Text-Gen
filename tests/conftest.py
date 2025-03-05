import os
import pytest
from dotenv import load_dotenv
from unittest.mock import patch, MagicMock
from sqlalchemy.orm import scoped_session, sessionmaker
import subprocess

from app.main import create_app
from app.models import db as _db

# Load environment variables from .env.test
# (pytest-dotenv can also do this automatically but, this is to be more explicit.
load_dotenv(".env.test")

@pytest.fixture(scope="session")
def app():
    """
    Returns a Flask application instance configured for tests.
    """
    # Create the Flask app
    _app = create_app()
    
    # Override the DB URI to use the test database from .env.test
    test_db_uri = (
        f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
        f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
    )
    _app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI=test_db_uri,
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )
    return _app

@pytest.fixture(scope="session")
def db(app):
    """
    Creates a clean database for the entire test session.
    Drops all tables when the session is complete.
    """
    with app.app_context():
        _db.create_all()
        yield _db
        _db.drop_all()

@pytest.fixture(scope="function", autouse=True)
def session(app, db):
    """
    Runs each test in its own transaction and then rolls it back,
    preventing leftover data from one test affecting others.
    """
    engine = db.engine 

    connection = engine.connect()
    transaction = connection.begin()

    session_factory = sessionmaker(bind=connection)
    Session = scoped_session(session_factory)

    old_session = db.session
    db.session = Session

    yield Session 

    Session.remove()
    transaction.rollback()
    connection.close()

    # 6. Restore the old session object
    db.session = old_session

@pytest.fixture(scope="function")
def client(app, db):
    """
    Returns a Flask test client.
    """
    with app.test_client() as client:
        yield client

@pytest.fixture(scope="session", autouse=True)
def run_migrations():
    """
    Runs Alembic migrations once at the beginning of the test session
    and optionally downgrades at the end.
    """
    subprocess.run(["alembic", "upgrade", "head"], check=True)
    yield


@pytest.fixture
def mock_openai_chat_completion():
    """
    Fixture that mocks openai.Completion.create calls to avoid real API usage.
    You can override return values as needed in your tests.
    """
    with patch("openai.chat.completions.create") as mock_chat_create:
        mock_chat_create.return_value = MagicMock(
            choices=[MagicMock(message={"content": "Mocked AI response"})]
        )
        yield mock_chat_create

@pytest.fixture
def auth_headers(client):
    """
    Creates a default user and logs them in, returning the Authorization header.
    """
    # Register
    client.post("/auth/register", json={
        "username": "TestUser",
        "password": "password123"
    })
    # Login
    login_resp = client.post("/auth/login", json={
        "username": "TestUser",
        "password": "password123"
    })
    token = login_resp.get_json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
