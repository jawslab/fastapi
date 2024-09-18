import pytest
from app.routers.oauth2 import create_access_token

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

print ("Testing Database.py is using", settings.database_hostname)

#default is "function"
@pytest.fixture(scope="function")
# @pytest.fixture(scope="session")
# @pytest.fixture(scope="module")
def session():
    print ("Testing Database.py is using", SQLALCHEMY_DATABASE_URL)
    print("my session fixture ran")
    #run DB session code before run test
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    # Dependency
    try:
        yield db
    finally:
        db.close()

# client = TestClient(app)
@pytest.fixture
def client(session):
    #run Client code before
    # Dependency
    def override_get_db():
        print("my override_get_db ran")
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
 
    yield TestClient(app)
    #run code after run test


# class TestClient(
#     app: ASGIApp,
#     base_url: str = "http://testserver",
#     raise_server_exceptions: bool = True,
#     root_path: str = "",
#     backend: Literal['asyncio', 'trio'] = "asyncio",
#     backend_options: dict[str, Any] | None = None,
#     cookies: CookieTypes | None = None,
#     headers: dict[str, str] | None = None,
#     follow_redirects: bool = True
# )

@pytest.fixture
def test_user(client):
    user_data = {"email": "test@example.com", "password": "testpassword"}
    response = client.post("/users/", json=user_data)
    print("test_user", response.json())
    assert response.status_code == 201
    new_user = response.json()
    new_user['password'] = user_data['password']
    print("new_user", new_user)
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token(data={"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(test_user, session):
    posts_data = [{
        "title": "First Post",
        "content": "First Post Content",
        "owner_id": test_user['id']
    }, {
        "title": "Second Post",
        "content": "Second Post Content",
        "owner_id": test_user['id']
    }, {
        "title": "Third Post",
        "content": "Third Post Content",
        "owner_id": test_user['id']
    }]
    # map(func,posts_data)

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    #convert the map to list
    posts = list(post_map)
    session.add_all(posts)
    session.commit()
    posts = session.query(models.Post).all()
    return posts