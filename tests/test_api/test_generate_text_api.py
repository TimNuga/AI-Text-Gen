import pytest

def test_generate_text_success(client, session, auth_headers, mock_openai_chat_completion):
    resp = client.post("/generate-text", json={"prompt": "Hello, AI!"}, headers=auth_headers)
    data = resp.get_json()
    assert resp.status_code == 201
    assert "id" in data
    assert data["prompt"] == "Hello, AI!"
    assert data["response"] == "Mocked AI response"

def test_generate_text_unauthorized(client, session):
    resp = client.post("/generate-text", json={"prompt": "No token here"})
    assert resp.status_code == 401

def test_get_generated_text(client, auth_headers):
    # 1) Generate text
    create_resp = client.post("/generate-text", json={"prompt": "Profile test"}, headers=auth_headers)
    text_id = create_resp.get_json()["id"]
    # 2) Retrieve it
    get_resp = client.get(f"/generated-text/{text_id}", headers=auth_headers)
    assert get_resp.status_code == 200
    data = get_resp.get_json()
    assert data["id"] == text_id
    assert data["prompt"] == "Profile test"

def test_get_generated_text_unauthorized(client, auth_headers):
    # Create as user 1
    create_resp = client.post("/generate-text", json={"prompt": "Mine only"}, headers=auth_headers)
    text_id = create_resp.get_json()["id"]
    # Attempt to GET as user 2 -> must register a new user
    client.post("/auth/register", json={
        "username": "SecondUser",
        "password": "pass2"
    })
    login_resp = client.post("/auth/login", json={
        "username": "SecondUser",
        "password": "pass2"
    })
    new_token = login_resp.get_json()["access_token"]
    new_headers = {"Authorization": f"Bearer {new_token}"}
    get_resp = client.get(f"/generated-text/{text_id}", headers=new_headers)
    assert get_resp.status_code == 403
    assert get_resp.get_json()["message"] == "Unauthorized"
