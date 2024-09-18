from typing import List, Optional
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from random import randrange
# Note: the module name is psycopg, not psycopg3
from . import models
from .database import engine, get_db
from .routers import post, user, auth, vote
from .config import settings



# disable it to let Alembic to create it from models.py
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "https://www.google.com",
    "http://localhost:8000",  # Add localhost for development
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


my_posts = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "title of post 2", "content": "content of post 2", "id": 2},
]

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
async def root():
    return {"message": "welcome to my api -test for reload"}

