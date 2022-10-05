from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import schemas, models, utils, oauth2
from ..database import get_db


router = APIRouter(
    tags=["Authentication"]
)


@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_found = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()

    if not user_found:
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"no user with email: {user_credentials.email} does not exist")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    if not utils.verify(user_credentials.password, user_found.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

    access_token = oauth2.create_access_token(data = {
        "user_id": user_found.id,
    })

    return {"access_token": access_token, "token_type": "bearer"}
