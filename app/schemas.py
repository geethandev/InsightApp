from pydantic import BaseModel,EmailStr
from typing import Optional
from fastapi import UploadFile

class User(BaseModel):
    email: str


class UserDetails(BaseModel):
    email:str
    username:str
    
class CreateUser(BaseModel):
    username:str
    email: EmailStr
    password: str

    
    
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None