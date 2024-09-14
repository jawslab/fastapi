from typing import List, Optional
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends

from random import randrange
# Note: the module name is psycopg, not psycopg3
import psycopg2
import time
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db

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
    
@app.get("/")
async def root():
    return {"message": "welcome to my api"}

#List typing for the return
@app.get("/posts", response_model= List[schemas.Post])
def test(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

# @app.get("/posts")
# def get_posts():
#     cursor.execute("SELECT * FROM posts")
#     posts = cursor.fetchall()
#     print (posts)
#     return {"data": posts}

# @app.post("/createposts")
# def create_posts(payload: dict = Body(...)):
#     return {"post": f"title: {payload['title']} content: {payload['content']}" }

# @app.post("/createposts")
# def create_posts(post: schemes.Post):
#     print(post.published)
#     print(post)
#     print(post.dict())
#     return {"post": f"data: {post}"}

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model= schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # print(post.published)
    # print(post)
    # print(post.dict())

    # post_dict = post.dict()
    # post_dict["id"] = randrange(0, 1000000)
    # my_posts.append(post_dict)
    # return {"post": f"data: {post_dict}"}

    # print(post)
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, (post.published)))
    # new_post = cursor.fetchone()
    # conn.commit()
    
    print(post)
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# #path parameter
# @app.get("/posts/latest")
# def get_latest_post():
#     return {"latest_post": my_posts[-1]}

# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p

@app.get("/posts/{id}", response_model= schemas.Post)
def get_post(id: int, response: Response, db:Session = Depends(get_db)):
    # print(id, type(id))
    # post = find_post(id)
    # if not post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
    # return {"post_details": post}

    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
    return post

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db:Session = Depends(get_db)):
    #deleting a post
    #find the index in the array that has required ID
    #my_posts.pop(index)

    # print(id, type(id))
    # print(my_posts)
    # print(find_index_post(id))
    # index = find_index_post(id)
    # post = find_post(id)
    # if index == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
    # my_posts.pop(index)

    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id), ))
    # post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    print(post_query)

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
    print(post)
    
    # post.delete(synchronize_session=False)
    db.delete(post)
    db.commit()

    #no data is returned, only status code is returned
    # return {"message": "post was successfully deleted"}
    # return Response(status_code=status.HTTP_204_NO_CONTENT) #no data is returned
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", response_model= schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    # index = find_index_post(id)
    # if index == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
    # post_dict = post.dict()
    # post_dict["id"] = id
    # my_posts[index] = post_dict
    # return {"data": post_dict}

    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, (post.published), (str(id))))
    # post = cursor.fetchone()
    # conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    print(post_query)
    oldpost = post_query.first()
    
    if oldpost == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
    print(post)
#   The error happens because SQLAlchemy models don't have a .dict() method like Pydantic models.
#   Use Pydantic models to handle validation and convert the data using .dict() for updates.
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    new_post = post_query.first()
    return new_post