from fastapi.testclient import TestClient
from app import models
from app.main import app

#copy from database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.database import get_db

import pytest


# (host='localhost', dbname='fastapi', user='postgres', password='aQbvvgL1ekDasXJ0Ntwg')
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:aQbvvgL1ekDasXJ0Ntwg@localhost/fastapi_test"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# copy from main.py to allow models.py create a test database - {settings.database_name}_test
# models.Base.metadata.drop_all(bind=engine)
# models.Base.metadata.create_all(bind=engine)
# end of copy from database.py

print ("Testing Database.py is using", SQLALCHEMY_DATABASE_URL)


@pytest.fixture
def session():
    #run DB session code before run test
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    # Dependency
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    override_get_db

# client = TestClient(app)
@pytest.fixture
def client(session):
    #run Client code before
    yield TestClient(app)
    #run code after run test


def test_root(client):
    response = client.get("/")
    print(response.json())
    assert response.status_code == 200
    assert response.json() == {"message": "welcome to my api -test for reload"}

def test_create_user(client):
    response = client.post("/users", json={"email": "test@example.com", "password": "testpassword"})
    print(response.json())
    assert response.status_code == 201
    assert "id" in response.json()
    assert response.json()["email"] == "test@example.com"