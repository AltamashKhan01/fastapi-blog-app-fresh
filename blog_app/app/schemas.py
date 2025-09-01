# Import necessary modules
from pydantic import BaseModel
from typing import List, Optional


class BlogBase(BaseModel):
    """
    This class represents the base schema for a blog.
    """
    title: str
    body: str


class Blog(BlogBase):
    """
    This class represents the schema for a blog.
    """
    user_id: int

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    """
    This class represents the base schema for a user.
    """
    name: str
    email: str
    password: str


class User(BaseModel):
    """
    This class represents the schema for a user.
    """
    name: str
    email: str

    class Config:
        from_attributes = True


class ShowUser(BaseModel):
    """
    This class represents the schema for a user to be shown.
    """
    name: str
    email: str
    blogs: List[BlogBase] = []

    class Config:
        from_attributes = True


class ShowBlog(BaseModel):
    """
    This class represents the schema for a blog to be shown.
    """
    title: str
    body: str
    creator: User

    class Config:
        from_attributes = True


class Login(BaseModel):
    """
    This class represents the schema for a login request.
    """
    username: str
    password: str


class Token(BaseModel):
    """
    This class represents the schema for a token.
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    This class represents the schema for the data in a token.
    """
    username: Optional[str | None] = None