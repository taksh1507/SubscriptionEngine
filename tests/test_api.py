import pytest

def test_docs_page(client):
    response = client.get("/docs")
    assert response.status_code == 200

def test_create_user(client):
    # This might fail if the user already exists in module scope DB, 
    # but for a simple isolated run it's fine.
    response = client.post(
        "/api/v1/users/",
        json={"email": "newuser@example.com", "password": "password123"}
    )
    if response.status_code == 400: # Already registered
        assert response.json()["detail"] == "Email already registered"
    else:
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "newuser@example.com"
        assert "id" in data
