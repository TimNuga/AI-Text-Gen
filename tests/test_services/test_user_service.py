import pytest
from unittest.mock import MagicMock
from app.services.user_service import UserService
from app.models import User
from passlib.hash import bcrypt

def test_register_user_success():
    repo_mock = MagicMock()
    repo_mock.find_by_username.return_value = None  # No existing user
    service = UserService(repo_mock)
    
    user = service.register_user("TestUser", "testpass")
    repo_mock.create_user.assert_called_once()
    assert user is not None

def test_register_user_duplicate():
    repo_mock = MagicMock()
    existing_user = User(username="duplicate", password_hash="hash")
    repo_mock.find_by_username.return_value = existing_user
    service = UserService(repo_mock)
    
    with pytest.raises(ValueError) as exc:
        service.register_user("Duplicate", "pass123")
    assert "already exists" in str(exc.value)

def test_verify_credentials_success():
    repo_mock = MagicMock()
    user_stub = User(username="creds", password_hash=bcrypt.hash("mypassword"))
    repo_mock.find_by_username.return_value = user_stub
    service = UserService(repo_mock)
    
    user = service.verify_credentials("creds", "mypassword")
    assert user == user_stub

def test_verify_credentials_fail():
    repo_mock = MagicMock()
    repo_mock.find_by_username.return_value = None  # user not found
    service = UserService(repo_mock)
    
    user = service.verify_credentials("nope", "pass")
    assert user is None
