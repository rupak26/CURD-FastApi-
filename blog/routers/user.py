from ..domain.schemas import BLog2 , User2 , showBlog , showUser
from ..Database import get_db
from ..domain import models
from fastapi import Depends, FastAPI , status , Response , HTTPException , APIRouter
from sqlalchemy.orm import Session  
from .oauth2 import role_required
from ..hasing import Hasing
from typing import List
from ..repository import user
from ..response.schema import ApiResponse

router = APIRouter(
    prefix= '/api/v1/user',
    tags=['User'] ,
    dependencies= [Depends(role_required(["admin"]))] 
) 

@router.post('/create-user/', 
             summary="Create new user"  , 
             description='''
             Create New Users
             ''',
             status_code=status.HTTP_201_CREATED,
             response_model = ApiResponse)
def create_user_route(request: User2, db: Session = Depends(get_db)):
    return user.create_user(request, db)

@router.get('/get-all-users/',
            summary="Get all user",
            description='''
            Get all users
            ''',
            status_code=status.HTTP_202_ACCEPTED,
            response_model=ApiResponse)
def show_user(db : Session = Depends(get_db)):
    return user.show_all_user(db)

@router.get('/get-user/{id}',
            summary="Get individul user",
            description='''
            Get individul user based upon their id
            ''',
            status_code=status.HTTP_202_ACCEPTED,
            response_model=ApiResponse)
def show_user(id:int , db : Session = Depends(get_db)):
    return user.show_user_by_id(id , db)

