from datetime import datetime, timedelta
from jose import jwt, JWTError
from .. import schemas, database, models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from ..config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
#to get a string like this run:
#openssl rand -hex 32
#copy the output
#paste it in the .env file
#SECRET_KEY
#Algorithm
#Expiration time
# openssl rand -hex 32

#SECRET_KEY
#Algorithm
#Expiration time
# openssl rand -hex 32

# SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30
SECRET_KEY = f"{settings.SECRET_KEY}"
ALGORITHM = f"{settings.ALGORITHM}"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
# print(SECRET_KEY)
# print(ALGORITHM)
# print(ACCESS_TOKEN_EXPIRE_MINUTES)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        userid: str = payload.get("user_id")
        if userid is None:
            raise credentials_exception
        # str(userid) to avoid error
        token_data = schemas.TokenData(id=str(userid))
        # print(token_data)
    except JWTError:
        raise credentials_exception
    return token_data
    
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db) ):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = verify_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    # <app.models.User object at 0x000002300DFBC2B0>
    # print(user)
    return user
    # return verify_token(token, credentials_exception)