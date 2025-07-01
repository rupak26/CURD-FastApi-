from ast import mod
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter , Depends , HTTPException , status
from ..domain.schemas import Login , Token
from ..domain import models
from sqlalchemy.orm import Session 
from ..Database import get_db 
from ..hasing import Hasing
from .token import create_access_token 
from fastapi.security import OAuth2PasswordRequestForm
import os 

ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

router = APIRouter(
    tags=['Authentication']
) 

@router.post('/login')
def login(request:OAuth2PasswordRequestForm = Depends() , db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first() 
    if not user:
       raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , 
                           detail= "email did not exists")
    if not Hasing.verify(request.password , user.password):
       raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , 
                           detail= "Incorrect Password") 
    #Generate Token 
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={
           "email" : user.email,
           "user_id" : user.id ,
           "user_role" : user.role,
        }
    )
    return { "access_token" :access_token, "token_type" :"bearer"}