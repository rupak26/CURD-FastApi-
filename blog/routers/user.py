from ..schemas import BLog2 , User2 , showBlog , showUser
from ..Database import get_db
from .. import models
from fastapi import Depends, FastAPI , status , Response , HTTPException , APIRouter
from sqlalchemy.orm import Session  
from ..hasing import Hasing
from typing import List
from ..repository import user

router = APIRouter(
    prefix= '/user',
    tags=['User'] 
) 

@router.post('/', status_code=status.HTTP_201_CREATED)
def create_user(request:User2 , db : Session = Depends(get_db)):
    return user.create_user(request , db)

@router.get('/',status_code=status.HTTP_202_ACCEPTED ,  response_model=List[showUser])
def show_user(db : Session = Depends(get_db)):
    return user.show_all_user(db)

@router.get('/{id}',status_code=status.HTTP_202_ACCEPTED ,  response_model=showUser)
def show_user(id:int , db : Session = Depends(get_db)):
    return user.show_user_by_id(id , db)

