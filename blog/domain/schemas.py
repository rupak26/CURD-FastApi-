import email
from token import OP
from fastapi import Body
from pydantic import BaseModel , ConfigDict
from typing import Optional , List , TypeVar 


class User2(BaseModel):
    username : str 
    email : str 
    password : str 


class showUser(BaseModel):
    username : str 
    email : str 
    
    model_config = {
        "from_attributes": True
    }
    
class showBlog(BaseModel):
    title : str 
    body : str 
    creator : Optional[showUser] = None

    model_config = {
        "from_attributes": True
    }


class BLog2(BaseModel):
    title : str 
    body : str 

    
class BLogPatch(BaseModel):
    title : Optional[str] = None 
    body : Optional[str] = None 



class Login(BaseModel):
     username : str 
     password : str 


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email : Optional[str] = None



