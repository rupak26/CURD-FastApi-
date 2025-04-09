from .. import models
from sqlalchemy.orm import Session 
from ..schemas import  User2 ,  showUser
from ..hasing import Hasing
from fastapi import HTTPException , status


def create_user(request:User2, db:Session):
    new_user = models.User(username = request.username,email=request.email,password=Hasing.hashPassword(request.password))
    db.add(new_user) 
    db.commit() 
    db.refresh(new_user)
    return new_user

def show_all_user(db : Session):
    return db.query(models.User).all() 

def show_user_by_id(id : int  , db : Session):
    users = db.query(models.User).filter(models.User.id == id).first() 
    if not users:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , 
                           detail= f"User with {id} did not exists")
    return users 