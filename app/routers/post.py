from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.schema import PostCreate, PostUpdate, PostWithVoteCount, UserResponse  # Import UserResponse and PostUpdate schemas
from app.models import Post, Vote
from app.routers.oauth2 import get_current_user  # Import the dependency

router = APIRouter()

@router.get("/posts", response_model=list[PostWithVoteCount])
def get_posts(db: Session = Depends(get_db), search: str = "", limit: int = 10, skip: int = 0):
    posts = db.query(Post, func.count(Vote.post_id).label("vote_count")) \
              .outerjoin(Vote, Vote.post_id == Post.id) \
              .group_by(Post.id) \
              .filter(Post.title.contains(search) | Post.content.contains(search)) \
              .limit(limit) \
              .offset(skip) \
              .all()
    return [
        PostWithVoteCount(
            id=post.id,
            title=post.title,
            content=post.content,
            published=post.published,
            created_at=post.created_at,
            user_id=post.user_id,
            vote_count=vote_count
        )
        for post, vote_count in posts
    ]

@router.post("/posts", response_model=PostWithVoteCount)
def create_post(post: PostCreate, db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    db_post = Post(
        title=post.title,
        content=post.content,
        published=post.published,
        user_id=current_user.id
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return PostWithVoteCount(
        id=db_post.id,
        title=db_post.title,
        content=db_post.content,
        published=db_post.published,
        created_at=db_post.created_at,
        user_id=db_post.user_id,
        vote_count=0
    )

@router.get("/posts/{post_id}", response_model=PostWithVoteCount)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post, func.count(Vote.post_id).label("vote_count")) \
              .outerjoin(Vote, Vote.post_id == Post.id) \
              .group_by(Post.id) \
              .filter(Post.id == post_id) \
              .first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post, vote_count = post
    return PostWithVoteCount(
        id=post.id,
        title=post.title,
        content=post.content,
        published=post.published,
        created_at=post.created_at,
        user_id=post.user_id,
        vote_count=vote_count
    )

@router.put("/posts/{post_id}", response_model=PostWithVoteCount)
def update_post(post_id: int, updated_post: PostUpdate, db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    post_query = db.query(Post).filter(Post.id == post_id, Post.user_id == current_user.id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    post_data = updated_post.dict(exclude_unset=True)
    for key, value in post_data.items():
        setattr(post, key, value)

    db.add(post)
    db.commit()
    db.refresh(post)

    return PostWithVoteCount(
        id=post.id,
        title=post.title,
        content=post.content,
        published=post.published,
        created_at=post.created_at,
        user_id=post.user_id,
        vote_count=db.query(func.count(Vote.post_id)).filter(Vote.post_id == post.id).scalar()
    )

@router.delete("/posts/{post_id}", status_code=204)
def delete_post(post_id: int, db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    post_query = db.query(Post).filter(Post.id == post_id, Post.user_id == current_user.id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    db.delete(post)
    db.commit()

@router.get("/posts/{post_id}/votes")
def get_votes_count(post_id: int, db: Session = Depends(get_db)):
    count = db.query(func.count(Vote.post_id)).filter(Vote.post_id == post_id).scalar()
    return {"post_id": post_id, "votes_count": count}