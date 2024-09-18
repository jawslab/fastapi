# from .database import client, session
from app import models, schemas, config

from jose import jwt, JWTError
import pytest

def test_root(client):
    response = client.get("/")
    print(response.json())
    assert response.status_code == 200
    assert response.json() == {"message": "welcome to my api -test for reload"}

def test_create_user(client):
    response = client.post("/users/", json={"email": "test@example.com", "password": "testpassword"})
    print(response.json())
    assert response.status_code == 201
    assert "id" in response.json()
    assert response.json()["email"] == "test@example.com"

def test_get_user(client):
    postresponse = client.post("/users/", json={"email": "test@example.com", "password": "testpassword"})
    print("post", postresponse.json())
    userid = postresponse.json()["id"]
    response = client.get(f"/users/{userid}")
    print("get", response.json())
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"

def test_login_user(test_user, client):
    response = client.post("/login/", data={"username": test_user['email'], "password": test_user['password']})
    print("login", response.json())
    login_response = schemas.Token(**response.json())
    payload = jwt.decode(login_response.access_token, config.settings.SECRET_KEY, algorithms=config.settings.ALGORITHM)
    id = payload.get("user_id")
    assert id == test_user["id"]
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@example.com', 'testpassword', 403),
    ('test@example.com', 'wrongpassword', 403),
     (None, 'wrongpassword', 403),
    #  (None, 'wrongpassword', 422),
])
def test_login_user_fail(test_user, client, email, password, status_code):
    response = client.post("/login/", data={"username": email, "password": password})
    print("login", response.json())
    assert response.status_code == status_code
    assert "detail" in response.json()
    # assert response.json()["detail"] == "Invalid Credentials"
