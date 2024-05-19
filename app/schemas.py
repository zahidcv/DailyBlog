from typing import List

from pydantic import BaseModel


class Blog(BaseModel):
    title: str
    body:str
    
class ShowUser(BaseModel):
    id: int

    email: str
    # blogs: List[Blog]
    class Config():
        orm_mode = True

class UserLogin(BaseModel):
    email: str
    password: str
    
class ShowBlog(BaseModel):
    id: int
    title: str
    content:str
    owner: ShowUser
    class Config():
        orm_mode = True
        
class User(BaseModel):
    # name: str
    email: str
    password: str

class Login(BaseModel):
    email: str
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class Vote(BaseModel):
    post_id: int
    direction: int