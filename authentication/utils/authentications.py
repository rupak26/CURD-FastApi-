from ast import mod
from datetime import datetime, timedelta, timezone
from models import User
from fastapi import APIRouter , Depends , HTTPException , status , Request
from sqlalchemy.orm import Session 
from database import get_db 
from .hasing import Hasing
from schemas import Login , RefreshTokenSchema
from .token import create_access_token , create_refresh_token , decode_token
from fastapi.security import OAuth2PasswordRequestForm
import os 

ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
REFRESH_TOKEN_EXPIRE_MINUTES = os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES")

router = APIRouter(
    prefix='/api/v1/auth',
    tags=['Authentication']
) 

@router.post('/login')
def login(request:Login, db : Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first() 
    if not user:
       raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , 
                           detail= "email did not exists")
    if not Hasing.verify(request.password , user.password):
       raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , 
                           detail= "Incorrect Password") 
    #Generate Token 
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token_expires = timedelta(minutes=int(REFRESH_TOKEN_EXPIRE_MINUTES))
    payload = {
        "email": user.email,
        "user_id": user.id,
        "user_role": user.role,
    }
    access_token = create_access_token(payload , access_token_expires)
    refresh_token = create_refresh_token(payload, refresh_token_expires)

    return { "access_token" :access_token, "refresh_token" : refresh_token ,"token_type" :"bearer"}


# Making access_token using refresh_token 

@router.post("/refresh-token")
def refresh_token(request : RefreshTokenSchema):
    token = request.refresh_token
    if not token:
       raise HTTPException(status_code=400, detail="Refresh token missing")
    
    payload = decode_token(token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
    
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(payload, access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}
