# schema, model
from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

# PostBase, PosCreate handle body/request sent by the user from input fields


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass

# Handles reponse to the user


class PostResponse(PostBase):
    id: int
    created_at: datetime
    author_id: int

    # to conver sqlachemy to pydantic model

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str
    pass


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(UserBase):
    password: str
    pass


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
