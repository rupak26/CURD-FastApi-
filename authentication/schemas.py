import email
from token import OP
from fastapi import Body
from pydantic import BaseModel , ConfigDict
from typing import Optional , List , TypeVar 
from datetime import datetime

class User2(BaseModel):
    username : str 
    email : str 
    password : str 
    role : str 


class showUser(BaseModel):
    username : str 
    email : str 
    
    model_config = {
        "from_attributes": True
    }


class Login(BaseModel):
     email : str 
     password : str 


class Token(BaseModel):
    access_token: str
    token_type: str



