from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_and_login():
    register_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "strongpassword"
    }

    response = client.post("/register", json=register_data)
    assert response.status_code == 201

    login_data = {
        "username": "testuser",
        "password": "strongpassword"
    }
    response = client.post("/login", json=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
