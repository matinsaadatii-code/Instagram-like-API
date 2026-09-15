from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class Post(PostBase):
    pass

class UserBase(BaseModel):
    email: EmailStr
    created_at: datetime = Field(default_factory=datetime.now)

class UserSchema(UserBase):
    password: str

class UserSchemaResponse(UserBase):
    id: int

    class Config:
        from_attributes = True

class PostSchemaResponse(PostBase):
    user_id: int
    id: int
    created_at: datetime = Field(default_factory=datetime.now)
    user: UserSchemaResponse

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int]