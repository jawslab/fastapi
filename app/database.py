from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
# (host='localhost', dbname='fastapi', user='postgres', password='aQbvvgL1ekDasXJ0Ntwg')
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:aQbvvgL1ekDasXJ0Ntwg@localhost/fastapi"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


import psycopg2

try:
    conn = psycopg2.connect(host='localhost', dbname='fastapi', user='postgres', password='aQbvvgL1ekDasXJ0Ntwg')
    cursor = conn.cursor()
    print("Database connection was successful!")
except Exception as error:
    print("Error connecting to database: ", error)
