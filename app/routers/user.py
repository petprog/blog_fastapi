from typing import Optional, List
from fastapi import APIRouter, FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users']
)
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as err:
        print(err)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail = f"user with email: {user.email} already exists")
    return new_user

@router.get("/latest", response_model=schemas.UserResponse)
def get_latest_user(db: Session = Depends(get_db)):
    user_query = db.query(models.User).order_by(models.User.id.desc())

    queried_user = user_query.first()
    return queried_user
    
@router.get('/{id}', response_model=schemas.UserResponse)
def get_user(id: int,  db: Session = Depends(get_db)):
    queried_user = db.query(models.User).filter(models.User.id == id).first()

    if not queried_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"user with id: {id} does not exist")
    return queried_user;


