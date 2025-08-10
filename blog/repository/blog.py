from  sqlalchemy.orm import Session  
from ..domain import models
from typing import List
from ..domain.schemas import BLog2 , User2 , showBlog , showUser , BLogPatch 
from fastapi import  status , Response , HTTPException , APIRouter , Query , Depends
from ..socket.configuration import manager
from ..response.schema import ApiResponse 
import logging , json
logger = logging.getLogger("repository.blog")

def get_all(
            db : Session , 
            redis_client ,
            limit,  
            offset,  
    ):
    try:
        cache_key = f"get_all_blogs:limit={limit}:offset={offset}"
        cached_data = redis_client.get(cache_key)
        if cached_data:
            data = json.loads(cached_data)
            return ApiResponse(
                message="Fetched from cache",
                statusCode=200,
                datalist=data
            )
        
        datalist = db.query(models.Blog).offset(offset).limit(limit).all() 
        blogs = [showBlog.from_orm(blog) for blog in datalist]
    
        if not blogs:
            logger.error(f"Database is empty")
            return ApiResponse(
                message = "Database is empty" ,
                statusCode =  204 ,
                datalist = []
            )
        
        #SET AND EXPIRES in ONE FNCTION "setex"

        redis_client.setex(cache_key, 300, json.dumps([blog.dict() for blog in blogs])) 
        
        return ApiResponse(
            message = "Fatching was successfull" ,
            statusCode = 200,
            datalist = blogs
        )
    except Exception as e:
        logger.error(f"{e}")

def get_by_id(id , db : Session):
    try:
        datalist = db.query(models.Blog).filter(models.Blog.id==id).first() 
        if datalist is None:
            logger.error(f"{id} is Not found")
            return ApiResponse(
                message = f"Blog with id {id} not found"  ,
                statusCode =  404 ,
                datalist = []
            )
        blogs = showBlog.from_orm(datalist)
        return ApiResponse(
            message = "Fatching was successfull" ,
            statusCode = status.HTTP_200_OK  ,
            datalist = blogs
        )
    except Exception as e:
        logger.error(f"{e}")


async def create(request:BLog2 , db : Session , id : int):
    try:
        new_blog = models.Blog(title=request.title , body=request.body , user_id = id)
        db.add(new_blog)
        db.commit()
        db.refresh(new_blog)
        pid = new_blog.user_id
        user = db.query(models.User).filter(models.User.id==pid).first()
        await manager.broadcast(f"New blog created by {user.username} titled {new_blog.title}")
        result =  showBlog.from_orm(new_blog)
        return ApiResponse(
            message = "Posting was successfull" ,
            statusCode = 200 ,
            datalist = result
        )
    except Exception as e:
        logger.error(f"{e}")


def delete_by_id(id , db : Session):
    try:
        blog = db.query(models.Blog).filter(models.Blog.id==id).first()
        if not blog:
            logger.error(f"{id} is Not found")
            return ApiResponse(
                message = f"Blog with id {id} not found" ,
                statusCode =  404 ,
                datalist = []
            )
        blog.delete(synchronize_session=False) 
        db.commit() 
        return ApiResponse(
                message = "Blog deleted" ,
                statusCode =  204 ,
                datalist = []
        )
    except Exception as e:
        logger.error(f"{e}")

def updated_by_id(id:int , request:BLog2 , db : Session):
    try:
        blog = db.query(models.Blog).filter(models.Blog.id == id).update(
            {
                "title": request.title,
                "body": request.body
            },
            synchronize_session=False
        )
        if not blog:
            logger.error(f"{id} is Not found")
            return ApiResponse(
                message =  f"Blog with id {id} not found" ,
                statusCode =  404 ,
                datalist = []
            )
        
        db.commit() 
        return ApiResponse(
                message = "Blog Updated" ,
                statusCode =  200 ,
                datalist = []
            )
    except Exception as e:
        logger.error(f"{e}")

def updatedPartiali_by_id(id:int , request:BLogPatch , db : Session):
    try:
        blog = db.query(models.Blog).filter(models.Blog.id == id).first()
        if not blog:
            logger.error(f"{id} is Not found")
            return ApiResponse(
                message = f"Blog with id {id} not found" ,
                statusCode =  404 ,
                datalist = []
            )
        if request.title is not None:
            blog.title = request.title

        if request.body is not None:
            blog.body = request.body
        
        db.commit()
        db.refresh(blog)
        return ApiResponse(
                message = "Blog Updated" ,
                statusCode =  200 ,
                datalist = []
            )
    except Exception as e:
        logger.error(f"{e}")