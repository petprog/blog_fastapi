from typing import List
from fastapi import APIRouter, FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from ..database import engine, get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db),
              current_user: schemas.UserResponse = Depends(
        oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts;""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).filter(
        models.Post.author_id == current_user.id).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate,
                 db: Session = Depends(get_db),
                 current_user: schemas.UserResponse = Depends(
                     oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING *""",
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    print(current_user.email)
    new_post = models.Post(author_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/latest", response_model=schemas.PostResponse)
def get_latest_post(db: Session = Depends(get_db),
                    current_user: schemas.UserResponse = Depends(
        oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts ORDER BY id DESC LIMIT 1 """)
    # post = cursor.fetchone()
    post_query = db.query(models.Post).order_by(models.Post.id.desc())
    # count = post_query.count(models.Post.id)
    # print(count)
    queried_post = post_query.first()
    return queried_post
# {id} represent path parameter


@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(
        oauth2.get_current_user)):
    # print(type(id))
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()
    post_query = db.query(models.Post).filter(models.Post.id == str(id))
    queried_post = post_query.first()
    if not queried_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    if queried_post.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")
        
    return post_query.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(
        oauth2.get_current_user)):
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
    if queried_post.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.PostResponse)
def update_post(post: schemas.PostCreate,
                id: int,
                db: Session = Depends(get_db),
                current_user: schemas.UserResponse = Depends(
        oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published= %s WHERE id = %s RETURNING * """,
    #                (post.title, post.content, post.published, str(id),))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    queried_post = post_query.first()
    if not queried_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    if queried_post.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    updated_post = post_query.first()
    return updated_post
