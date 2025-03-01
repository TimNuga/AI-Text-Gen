import pytest
from flask_jwt_extended import create_access_token
from app.models import User, GeneratedText, db

@pytest.fixture
def test_user(db):
    """
    Creates a user directly in the database, returns the user model instance.
    """
    user = User(username="testuser")
    user.set_password("testpassword")
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture
def auth_token(test_user):
    """
    Creates a valid JWT token for the test_user. 
    """
    # We can't access Flask context here directly, so let's do it in a function
    return create_access_token(identity=str(test_user.id))

def test_generate_text_success(client, test_user, auth_token, mock_openai_completion):
    """
    Test generating text with a valid JWT, mocking out openai call.
    """
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.post("/generate-text", json={"prompt": "Hello AI"}, headers=headers)
    
    # If successful, we expect status 201
    assert response.status_code == 201, response.data
    data = response.get_json()
    assert data["response"] == "Mocked AI response"  # from our fixture
    assert data["prompt"] == "Hello AI"

def test_generate_text_unauthorized(client):
    """
    Test attempting to generate text without a JWT.
    """
    response = client.post("/generate-text", json={"prompt": "Hello AI"})
    assert response.status_code == 401

def test_get_generated_text(client, db, test_user, auth_token):
    """
    Test retrieving a stored text.
    """
    # Insert a record into DB
    gen_text = GeneratedText(
        user_id=test_user.id,
        prompt="Stored Prompt",
        response="Stored Response"
    )
    db.session.add(gen_text)
    db.session.commit()

    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get(f"/generated-text/{gen_text.id}", headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data["prompt"] == "Stored Prompt"
    assert data["response"] == "Stored Response"

def test_update_generated_text(client, db, test_user, auth_token):
    """
    Test updating an existing text.
    """
    gen_text = GeneratedText(
        user_id=test_user.id,
        prompt="Original Prompt",
        response="Original Response"
    )
    db.session.add(gen_text)
    db.session.commit()

    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.put(f"/generated-text/{gen_text.id}", json={
        "prompt": "Updated Prompt",
        "response": "Updated Response"
    }, headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data["prompt"] == "Updated Prompt"
    assert data["response"] == "Updated Response"

def test_delete_generated_text(client, db, test_user, auth_token):
    """
    Test deleting an existing text.
    """
    gen_text = GeneratedText(
        user_id=test_user.id,
        prompt="To be deleted",
        response="Irrelevant"
    )
    db.session.add(gen_text)
    db.session.commit()
    gen_text_id = gen_text.id

    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.delete(f"/generated-text/{gen_text_id}", headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == f"Generated text with ID {gen_text_id} deleted"

    # Ensure the record is gone
    gone_record = GeneratedText.query.get(gen_text_id)
    assert gone_record is None
