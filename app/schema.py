from pydantic import BaseModel, conint
from typing import Optional
from datetime import datetime

class LoginData(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: str

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None

class PostResponse(PostBase):
    id: int
    created_at: datetime
    user_id: int

    class Config:
        from_attributes = True

class PostWithVoteCount(PostResponse):
    vote_count: int

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class Vote(BaseModel):
    post_id: int
    vote_dir: conint(ge=0, le=1)  # type: ignore # Accepts 0 or 1

    class Config:
        from_attributes = True