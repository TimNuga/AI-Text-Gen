import pytest

def test_register_success(client):
    """
    Test successful user registration.
    """
    response = client.post("/register", json={
        "username": "testuser",
        "password": "testpassword"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "User registered successfully"

def test_register_duplicate_username(client):
    """
    Test registering with an existing username.
    """
    # First registration
    client.post("/register", json={
        "username": "testuser",
        "password": "testpassword"
    })
    # Duplicate registration
    response = client.post("/register", json={
        "username": "testuser",
        "password": "newpassword"
    })
    assert response.status_code == 400
    data = response.get_json()
    assert data["message"] == "User already exists"

def test_login_success(client):
    """
    Test logging in with valid credentials.
    """
    # Register first
    client.post("/register", json={
        "username": "testuser",
        "password": "testpassword"
    })
    # Now login
    response = client.post("/login", json={
        "username": "testuser",
        "password": "testpassword"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert "access_token" in data

def test_login_invalid_credentials(client):
    """
    Test login with invalid credentials.
    """
    # Register
    client.post("/register", json={
        "username": "testuser",
        "password": "testpassword"
    })
    # Attempt login with wrong password
    response = client.post("/login", json={
        "username": "testuser",
        "password": "wrong"
    })
    assert response.status_code == 401
    data = response.get_json()
    assert data["message"] == "Invalid credentials"
