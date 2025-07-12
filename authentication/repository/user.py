from models import User
from sqlalchemy.orm import Session 
from schemas import  User2 ,  showUser
from utils.hasing import Hasing
from fastapi import HTTPException , status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from response.schema import ApiResponse
    
def create_user(request: User2, db: Session):
    users = db.query(User).filter(User.username == request.username).first() 
    if users:
        return ApiResponse(
            message = f"User already exist" ,
            statusCode =  status.HTTP_409_CONFLICT ,
            datalist = []
        )
    new_user = User(
        username=request.username,
        email=request.email,                                                                                                         
        password=Hasing.hashPassword(request.password),
        role=request.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    data =  {
        "userName": new_user.username,
        "email": new_user.email,
        "role": new_user.role
    }
    return ApiResponse(
            message = f"New User Created" ,
            statusCode =  status.HTTP_201_CREATED,
            datalist = data
        )
    
    
def show_all_user(db : Session):
    users =  db.query(User).all() 
    user = [showUser.from_orm(u) for u in users]
    if not user:
        return ApiResponse(
            message = "Database is empty or No user" ,
            statusCode =  204 ,
            datalist = []
        )
    return ApiResponse(
        message = "Fatching was successfull" ,
        statusCode = 200,
        datalist = user
    )

def show_user_by_id(id : int  , db : Session):
    users = db.query(User).filter(User.id == id).first() 
    if users is None:
        return ApiResponse(
            message = f"User with id {id} not found"  ,
            statusCode =  404 ,
            datalist = []
        )
    user = showUser.from_orm(users)
    return ApiResponse(
        message = "Fatching was successfull" ,
        statusCode = status.HTTP_200_OK  ,
        datalist = user
    )

