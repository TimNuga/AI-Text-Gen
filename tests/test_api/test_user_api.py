import pytest

def test_get_profile(client, auth_headers):
    resp = client.get("/user/profile", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.get_json()
    assert "id" in data
    assert "username" in data

def test_get_profile_unauthorized(client):
    resp = client.get("/user/profile")
    assert resp.status_code == 401
