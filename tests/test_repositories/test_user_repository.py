import pytest
from app.repositories.user_repository import UserRepository

def test_create_user(session):
    repo = UserRepository(session)
    user = repo.create_user("RepoUser", "hashedpass")
    assert user.id is not None
    assert user.username == "repouser"  # normalized

def test_find_by_username(session):
    repo = UserRepository(session)
    user = repo.create_user("FindMe", "hash123")
    found = repo.find_by_username("findme")
    assert found is not None
    assert found.id == user.id

def test_find_by_username_not_found(session):
    repo = UserRepository(session)
    found = repo.find_by_username("nonexistent")
    assert found is None
