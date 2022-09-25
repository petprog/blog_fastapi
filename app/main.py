from random import randrange
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel


app = FastAPI()

# key type with or without default value
# schema, model
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

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
    return {"message" : "Nice update"}

@app.get("/posts")
def get_posts():
    return {"data": my_post}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 100000000000000)
    my_post.append(post_dict)
    return {"data": post_dict}

@app.get("/posts/latest")
def get_latest_post():
    post = my_post[len(my_post) - 1]
    return {"data": post}

# {id} represent path parameter
@app.get("/posts/{id}")
def get_post(id: int):
    # print(type(id))
    post = find_post(int(id))
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    return {"data": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # print(type(id))
    found_index = find_index(int(id))
    if found_index < 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    my_post.pop(found_index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(post: Post, id: int):
    found_index = find_index(int(id))
    print(found_index)
    if found_index < 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    post_dict = post.dict()
    post_dict['id'] = id
    my_post[found_index] =  post_dict
    return {"message" : "post was updated successfully"}