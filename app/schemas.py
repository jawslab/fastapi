from pydantic import BaseModel

#pydantic data model
# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True
#     # rating: Optional[int] = None

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass



