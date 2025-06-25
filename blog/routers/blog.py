from fastapi import Depends, FastAPI , status , Response , HTTPException , APIRouter
from ..domain.schemas import BLog2 , User2 , showBlog , showUser , BLogPatch 
from ..domain import models
from ..Database import engine , SessionLocal , get_db
from ..hasing import Hasing
from  sqlalchemy.orm import Session  
from  typing import List , Any
from .oauth2 import get_current_user
from ..repository import blog
from ..core import swagger_doc as s
from ..response.schema import ApiResponse
import logging 

logger = logging.getLogger("routers.blog")

router = APIRouter(
    prefix='/blog' ,
    tags=['Blogs']
)

@router.post('/' ,
              summary="Create new blog",
              description=s.blog_desc, 
              status_code= status.HTTP_201_CREATED)
async def create(request:BLog2 , db : Session = Depends(get_db),get_current_user : User2 = Depends(get_current_user)):
    logger.info(f"API call: POST /blog/")
    return await blog.create(request , db ,  get_current_user)

# Customize request_model via using response schema 
@router.get('/' ,
            summary="Get all Blog",
            description='''
            Get all Blogs from Database
            ''',
            status_code= status.HTTP_200_OK, response_model = ApiResponse)
def details(db : Session = Depends(get_db),get_current_user : User2 = Depends(get_current_user)):
    logger.info(f"API call: GET /blog/")
    return blog.get_all(db)


@router.get('/{id}' ,
            summary="Get individual Blog via Id",
            description='''
            Get individual Blog via Id 
            ''',
            status_code= status.HTTP_200_OK,
            response_model= ApiResponse)
def details_by_id(id , db : Session = Depends(get_db),get_current_user : User2 = Depends(get_current_user)):
    logger.info(f"API call: GET /blog/{id}")
    return blog.get_by_id(id , db)

@router.delete('/{id}' ,
               summary="Delete Blog via Id",
               description='''Delete the blog of this id''' ,
               status_code=status.HTTP_200_OK,
               response_model= ApiResponse)
def distroy_by_id(id , db : Session = Depends(get_db),get_current_user : User2 = Depends(get_current_user)):
    logger.info(f"API call: DELETE /blog/{id}")
    return blog.delete_by_id(id,db)


@router.put('/{id}', 
            summary="Update Blog via Id" ,
            description='''
            Logged User can update the blog of this id
            ''',status_code=status.HTTP_202_ACCEPTED,
            response_model= ApiResponse)
def update_by_id(request:BLog2 , id:int ,  db : Session = Depends(get_db),get_current_user : User2 = Depends(get_current_user)):
    logger.info(f"API call: PUT /blog/{id}")
    return blog.updated_by_id(id , request , db)

@router.patch('/{id}',
              summary="Update Blog partiali via id",
              description='''
               Logged User can partiali update the blog of this id
              ''',status_code=status.HTTP_202_ACCEPTED,
              response_model= ApiResponse)
def update_Partiali_by_id(request:BLogPatch , id:int , db : Session = Depends(get_db),get_current_user : User2 = Depends(get_current_user)):
    logger.info(f"API call: PATCH /blog/{id}")
    return blog.updatedPartiali_by_id(id , request  , db)



# @router.get("/unauthorized")
# def test_unauthorized():
#     raise HTTPException(status_code=401, detail="User not authenticated")

# @router.get("/forbidden")
# def test_forbidden():
#     raise HTTPException(status_code=403, detail="Access denied")

# @router.get("/notfound")
# def test_notfound():
#     raise HTTPException(status_code=404, detail="This item was not found")

# @router.get("/badgateway")
# def test_badgateway():
#     raise HTTPException(status_code=502, detail="External service error")