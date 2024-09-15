from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import func

from .. import models, schemas, utils
from ..database import get_db
from typing import List, Optional
from . import oauth2

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

# #List typing for the return
@router.get("/", response_model= List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), limit: int = 5, skip: int =0, search: Optional[str] =""):
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
       # Convert posts to JSON format
    # print("Posts (JSON):", jsonable_encoder(posts))  # This will print the posts in JSON format

    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).\
        join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).\
        filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
#     print('Join', results)
#  # Convert join results to JSON-serializable format and print
#     serialized_results = [
#         {
#             "post": jsonable_encoder(result[0]),  # The Post object
#             "votes": result[1]  # The vote count
#         }
#         for result in results
#     ]
#     print("Join Results (JSON):", serialized_results)

    return results

#List typing for the return
@router.get("/myposts", response_model= List[schemas.Post])
def get_posts(db: Session = Depends(get_db), login_user: int = Depends(oauth2.get_current_user)):
    # print(login_user.id)
    posts = db.query(models.Post).filter(models.Post.owner_id==login_user.id).all()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return posts

# @app.get("/posts")
# def get_posts():
#     cursor.execute("SELECT * FROM posts")
#     posts = cursor.fetchall()
#     print (posts)
#     return {"data": posts}


# #path parameter
# @app.get("/posts/latest")
# def get_latest_post():
#     return {"latest_post": my_posts[-1]}

# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p

@router.get("/{id}", response_model= schemas.Post)
def get_post(id: int, response: Response, db:Session = Depends(get_db), login_user: int = Depends(oauth2.get_current_user)):
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

# @app.post("/createposts")
# def create_posts(payload: dict = Body(...)):
#     return {"post": f"title: {payload['title']} content: {payload['content']}" }

# @app.post("/createposts")
# def create_posts(post: schemes.Post):
#     print(post.published)
#     print(post)
#     print(post.dict())
#     return {"post": f"data: {post}"}

@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), login_user: int = Depends(oauth2.get_current_user)):
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
    
    # get from schema.UserLogin 
    print(login_user.email)
    print(post)
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(owner_id=login_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db:Session = Depends(get_db), login_user: int = Depends(oauth2.get_current_user)):
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
    # get from schema.UserLogin 
    print(login_user.email)
    if post.owner_id != login_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    print(post, post.title,post.content, post.published)
    
    post_query.delete(synchronize_session=False)
    # db.delete(post)
    db.commit()

    #no data is returned, only status code is returned
    # return {"message": "post was successfully deleted"}
    # return Response(status_code=status.HTTP_204_NO_CONTENT) #no data is returned
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model= schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
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
