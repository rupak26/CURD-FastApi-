from ..domain.schemas import BLog2 , User2 , showBlog , showUser
from ..Database import get_db
from ..domain import models
from fastapi import Depends, FastAPI , status , Response , HTTPException , APIRouter
from sqlalchemy.orm import Session  
from ..hasing import Hasing
from typing import List
from ..repository import user

router = APIRouter(
    prefix= '/user',
    tags=['User'] 
) 

@router.post('/', 
             summary="Create new user"  , 
             description='''
             Create New Users
             ''',
             status_code=status.HTTP_201_CREATED)
def create_user_route(request: User2, db: Session = Depends(get_db)):
    return user.create_user(request, db)

@router.get('/',
            summary="Get all user",
            description='''
            Get all users
            ''',
            status_code=status.HTTP_202_ACCEPTED ,  response_model=List[showUser])
def show_user(db : Session = Depends(get_db)):
    return user.show_all_user(db)

@router.get('/{id}',
            summary="Get individul user",
            description='''
            Get individul user based upon their id
            ''',
            status_code=status.HTTP_202_ACCEPTED ,  response_model=showUser)
def show_user(id:int , db : Session = Depends(get_db)):
    return user.show_user_by_id(id , db)

