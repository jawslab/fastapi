from typing import List, Optional
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends

from random import randrange
# Note: the module name is psycopg, not psycopg3
import psycopg2
import time
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db
from . import utils
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()




my_posts = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "title of post 2", "content": "content of post 2", "id": 2},
]


try:
    conn = psycopg2.connect(host='localhost', dbname='fastapi', user='postgres', password='aQbvvgL1ekDasXJ0Ntwg')
    cursor = conn.cursor()
    print("Database connection was successful!")
except Exception as error:
    print("Error connecting to database: ", error)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "welcome to my api"}

