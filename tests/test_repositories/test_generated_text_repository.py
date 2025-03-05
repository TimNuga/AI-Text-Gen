import pytest
from app.repositories.generated_text_repository import GeneratedTextRepository

def test_create_text(session):
    repo = GeneratedTextRepository(session)
    text = repo.create_text(user_id=1, prompt="Hello", response="World")
    assert text.id is not None
    assert text.prompt == "Hello"

def test_find_by_id(session):
    repo = GeneratedTextRepository(session)
    new_text = repo.create_text(user_id=2, prompt="ABC", response="DEF")
    found = repo.find_by_id(new_text.id)
    assert found is not None
    assert found.prompt == "ABC"

def test_update_text(session):
    repo = GeneratedTextRepository(session)
    new_text = repo.create_text(user_id=3, prompt="Old", response="Data")
    updated = repo.update_text(new_text, new_prompt="New", new_response="Value")
    assert updated.prompt == "New"
    assert updated.response == "Value"

def test_delete_text(session):
    repo = GeneratedTextRepository(session)
    new_text = repo.create_text(user_id=4, prompt="Delete me", response="Ok")
    tid = new_text.id
    repo.delete_text(new_text)
    # Now searching should yield None
    gone = repo.find_by_id(tid)
    assert gone is None
