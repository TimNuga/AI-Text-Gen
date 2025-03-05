import pytest
from flask import Flask

def test_register_success(client, session):
    response = client.post("/auth/register", json={
        "username": "SomeUser",
        "password": "somepass"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "User registered"

def test_register_duplicate_username(client):
    # Register once
    client.post("/auth/register", json={
        "username": "DupUser",
        "password": "testpass"
    })
    # Register again -> Should fail
    response = client.post("/auth/register", json={
        "username": "DupUser",
        "password": "anotherpass"
    })
    assert response.status_code == 400
    data = response.get_json()
    assert "already exists" in data["message"]

def test_login_success(client):
    client.post("/auth/register", json={
        "username": "LoginUser",
        "password": "password123"
    })
    response = client.post("/auth/login", json={
        "username": "LoginUser",
        "password": "password123"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert "access_token" in data

def test_login_invalid_credentials(client):
    response = client.post("/auth/login", json={
        "username": "NoUser",
        "password": "whatever"
    })
    assert response.status_code == 401
    data = response.get_json()
    assert data["message"] == "Invalid credentials"
