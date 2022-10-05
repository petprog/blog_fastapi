from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine, get_db
from .routers import post, user, auth

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

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Nice update"}




