##replaced by conftest.py
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

#default is "function"
@pytest.fixture(scope="function")
# @pytest.fixture(scope="session")
# @pytest.fixture(scope="module")
def session():
    print("my session fixture ran")
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