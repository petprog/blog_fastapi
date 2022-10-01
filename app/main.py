from random import randrange
from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
# key type with or without default value


while True:
    try:
        conn = psycopg2.connect(host='localhost',
                                database='blog-fastapi',
                                user='postgres',
                                password='password123',
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful!")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error, ", error)
        time.sleep(2)


# datastructures
my_post = [
    {
        "id": 1,
        "title": "title of post 1",
        "content": "content of post 1"
    },
    {
        "id": 2,
        "title": "Next rated artist nominees",
        "content": "These are the next rated artists: BNXN, Ruger, Portable"
    }
]


def find_post(id):
    for post in my_post:
        if post['id'] == id:
            return post


def find_index(id):
    for index, post in enumerate(my_post):
        if post['id'] == id:
            return index
    return -1

# request method, path, function


@app.get("/")
def root():
    return {"message": "Nice update"}


@app.get("/posts", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts;""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING *""",
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts/latest", response_model=schemas.PostResponse)
def get_latest_post(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts ORDER BY id DESC LIMIT 1 """)
    # post = cursor.fetchone()
    post_query = db.query(models.Post).order_by(models.Post.id.desc())
    # count = post_query.count(models.Post.id)
    # print(count)
    queried_post = post_query.first()
    return queried_post
# {id} represent path parameter


@app.get("/posts/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    # print(type(id))
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()
    post_query = db.query(models.Post).filter(models.Post.id == str(id))
    queried_post = post_query.first()
    if not queried_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    return post_query.first()


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # print(type(id))
    # cursor.execute(
    #     """DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == str(id))
    queried_post = post_query.first()
    if not queried_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.PostResponse)
def update_post(post: schemas.PostCreate, id: int, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published= %s WHERE id = %s RETURNING * """,
    #                (post.title, post.content, post.published, str(id),))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    queried_post = post_query.first()
    if not queried_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    print(update_post)
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    updated_post = post_query.first()
    return updated_post
