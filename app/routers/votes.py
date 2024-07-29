from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from app import models, schema
from app.database import get_db
from app.routers import oauth2
from typing import List

router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schema.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {vote.post_id} does not exist")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()

    if vote.vote_dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user: {current_user.id} has already voted for post: {vote.post_id}")
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote not found")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully removed vote"}

@router.get("/posts_with_vote_count", response_model=List[schema.PostWithVoteCount])
def get_posts_with_vote_count(db: Session = Depends(get_db)):
    posts = (
        db.query(models.Post, func.count(models.Vote.id).label('vote_count'))
        .outerjoin(models.Vote, models.Post.id == models.Vote.post_id)
        .group_by(models.Post.id)
        .all()
    )

    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No posts found")

    return posts