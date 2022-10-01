# schema, model
from pydantic import BaseModel
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

    # to conver sqlachemy to pydantic model

    class Config:
        orm_mode = True
