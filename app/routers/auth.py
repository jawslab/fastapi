from fastapi import APIRouter,Depends,status, HTTPException, Response
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from datetime import datetime
from .. import schemas, utils
from . import oauth2

router = APIRouter(
    prefix="/login",
    tags=['Auth']
)

@router.post("/")
# def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    # user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
#     {
#     "username": "user6@g.com", - from Broswer "username" - mapping to email in the db
#     "password": "kdkaksk"
#      }
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}