from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange

app = FastAPI()

#pydantic data model
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "title of post 2", "content": "content of post 2", "id": 2},
]

@app.get("/")
async def root():
    return {"message": "welcome to my api"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

# @app.post("/createposts")
# def create_posts(payload: dict = Body(...)):
#     return {"post": f"title: {payload['title']} content: {payload['content']}" }

# @app.post("/createposts")
# def create_posts(post: Post):
#     print(post.published)
#     print(post)
#     print(post.dict())
#     return {"post": f"data: {post}"}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    # print(post.published)
    # print(post)
    # print(post.dict())
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 1000000)
    my_posts.append(post_dict)
    print(my_posts)
    return {"post": f"data: {post_dict}"}

#path parameter
@app.get("/posts/latest")
def get_latest_post():
    return {"latest_post": my_posts[-1]}

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    print(id, type(id))
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
    #     response.status_code = status.HTTP_404_NOT_FOUND
    #     return {"message": f"post with id: {id} not found"}
    # print(post)
    # return {"post_details": f"Here is the {post}"}
    return {"post_details": post}

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    #deleting a post
    #find the index in the array that has required ID
    #my_posts.pop(index)
    print(id, type(id))
    print(my_posts)
    print(find_index_post(id))
    index = find_index_post(id)
    post = find_post(id)
    
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
    my_posts.pop(index)
    
    print(post)
    #no data is returned, only status code is returned
    # return {"message": "post was successfully deleted"}
    # return Response(status_code=status.HTTP_204_NO_CONTENT) #no data is returned
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
    post_dict = post.dict()
    post_dict["id"] = id
    my_posts[index] = post_dict
    return {"data": post_dict}