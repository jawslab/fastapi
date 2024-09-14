from datetime import datetime
from pydantic import BaseModel, EmailStr



class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

#pydantic data model
class Post(PostBase):
    id: int
    # title: str
    # content: str
    # published: bool
    created_at: datetime
    # rating: Optional[int] = None
    # ORM Sqlalchemy to Pydantic model to convert the data to a dictionary
    class Config:
        orm_mode = True

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True