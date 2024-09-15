from fastapi import FastAPI, Request,APIRouter,HTTPException,status, Depends
from pydantic import BaseModel
from .. import models, schemas, utils, database
from . import oauth2

from sqlalchemy.orm import Session
from typing import Optional

router = APIRouter(
    # prefix="/vote"  #this will add /vote before every route in this router
    # ,tags=['vote'] #this will group all the routes in this router under /vote
    prefix = "/vote",
    tags = ['vote']
    )


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), login_user: int = Depends(oauth2.get_current_user)):
    # vote.user_id = login_user.id
    found_post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if found_post == None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"post is not exist {vote.post_id}")
        # return {"message": "Post is not exsit, vote deleted successfully"}
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == login_user.id)
    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {login_user.id} has already voted on post {vote.post_id}")
        new_vote = models.Vote(post_id = vote.post_id, user_id = login_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Vote added successfully"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Vote deleted successfully"}