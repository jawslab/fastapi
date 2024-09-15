from typing import List, Optional
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends

from random import randrange
# Note: the module name is psycopg, not psycopg3
from . import models
from .database import engine, get_db
from .routers import post, user, auth
from .config import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI()




my_posts = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "title of post 2", "content": "content of post 2", "id": 2},
]

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "welcome to my api"}

