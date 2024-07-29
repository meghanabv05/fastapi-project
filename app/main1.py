from random import randint
from fastapi import FastAPI, HTTPException, status, Response
from typing import Optional
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

my_post = [
    {
        "id": 1, "title": "this is the title of id1", "content": "this is the content of id1"
    },
    {
        "id": 2, "title": "this is the title of id2", "content": "this is the content of id2"
    }
]

class Post(BaseModel):
    title: str
    content: str
    is_published: bool = True
    rating: Optional[int] = None

while True:
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='fastapi',
            user='yourusername',
            password='yourpassword',
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)

@app.get("/")
def welcome():
    return "Welcome to FastAPI"

@app.get("/posts")
def get_posts():
    return {"data": my_post}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randint(0, 1000)
    my_post.append(post_dict)
    return {"data": post_dict}

@app.get("/posts/{id}")
def get_post_by_id(id: int):
    for posts in my_post:
        if posts["id"] == id:
            return {"data": posts}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")    

def find_index_post(id: int):
    for index, post in enumerate(my_post):
        if post["id"] == id:
            return index
    return None

@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_posts(id: int, post: Post):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    post_dict = post.dict()
    post_dict["id"] = id
    my_post[index] = post_dict
    return {"data": post_dict}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def del_post(id: int):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(status_code=404, detail="Post not found")
    my_post.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)