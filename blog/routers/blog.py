from fastapi import Depends, FastAPI , status , Response , HTTPException , APIRouter
from ..domain.schemas import BLog2 , User2 , showBlog , showUser , BLogPatch
from ..domain import models
from ..Database import engine , SessionLocal , get_db
from ..hasing import Hasing
from  sqlalchemy.orm import Session  
from  typing import List
from .oauth2 import get_current_user
from ..repository import blog

router = APIRouter(
    prefix='/blog' ,
    tags=['Blogs']
)

@router.post('/' , status_code= status.HTTP_201_CREATED)
def create(request:BLog2 , db : Session = Depends(get_db),get_current_user : User2 = Depends(get_current_user)):
    return blog.create(request , db ,  get_current_user)

# Customize request_model via using response schema 
@router.get('/' , status_code= status.HTTP_200_OK, response_model = List[showBlog])
def details(db : Session = Depends(get_db),get_current_user : User2 = Depends(get_current_user)):
    return blog.get_all(db)


@router.get('/{id}' , status_code= status.HTTP_200_OK)
def details_by_id(id , db : Session = Depends(get_db),get_current_user : User2 = Depends(get_current_user)):
    return blog.get_by_id(id , db)

@router.delete('/{id}' , status_code=status.HTTP_200_OK)
def distroy_by_id(id , db : Session = Depends(get_db),get_current_user : User2 = Depends(get_current_user)):
    return blog.delete_by_id(id,db)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_by_id(request:BLog2 , id:int ,  db : Session = Depends(get_db),get_current_user : User2 = Depends(get_current_user)):
    return blog.updated_by_id(id , request , db)

@router.patch('/{id}',status_code=status.HTTP_202_ACCEPTED)
def update_Partiali_by_id(request:BLogPatch , id:int , db : Session = Depends(get_db),get_current_user : User2 = Depends(get_current_user)):
    return blog.updatedPartiali_by_id(id , request  , db)