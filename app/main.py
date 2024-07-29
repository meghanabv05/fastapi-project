import logging
from fastapi import FastAPI
from app.database import engine, Base
from app.routers import post, user, votes, auth
from app.models import Post, User, Vote
from fastapi.middleware.cors import CORSMiddleware

# Create all tables in the database
# Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["https://www.google.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(post.router)
app.include_router(user.router)
app.include_router(votes.router)
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}