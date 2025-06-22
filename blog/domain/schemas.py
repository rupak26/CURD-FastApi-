import email
from token import OP
from fastapi import Body
from pydantic import BaseModel
from pydantic.generics import GenericModel 
from typing import Optional , Generic , List , TypeVar

T = TypeVar('T') 

class ErrorDetails(BaseModel):
    field: str
    message: str

class ApiResponse(GenericModel , Generic[T]):
    message: str
    errorDetails: Optional[List[ErrorDetails]] = None
    statusCode: Optional[int] = None
    dataList: Optional[List[T]] = None

class User2(BaseModel):
    username : str 
    email : str 
    password : str 

class showUser(BaseModel):
    username : str 
    email : str 
    
    class config:
        orm_mode = True
    
        

class BLog2(BaseModel):
    title : str 
    body : str 

    
class BLogPatch(BaseModel):
    title : Optional[str] = None 
    body : Optional[str] = None 


class showBlog(BaseModel):
    title : str 
    body : str 

    class Config:
        from_attributes = True

class Login(BaseModel):
     username : str 
     password : str 


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email : Optional[str] = None



