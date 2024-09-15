from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

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
    owner_id: int
    owner: UserOut
    # rating: Optional[int] = None
    # ORM Sqlalchemy to Pydantic model to convert the data to a dictionary
    class Config:
        orm_mode = True

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass



class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
    # email: EmailStr
