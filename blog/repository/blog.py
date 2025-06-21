from  sqlalchemy.orm import Session  
from ..domain import models
from ..domain.schemas import BLog2 , User2 , showBlog , showUser , BLogPatch
from fastapi import  status , Response , HTTPException , APIRouter
from ..socket.configuration import manager

def get_all(db : Session):
    return  db.query(models.Blog).all() 
    

def get_by_id(id , db : Session):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if blog is None:
       raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , 
                           detail= f"Blog with {id} did not exists")
    return blog 

async def create(request:BLog2 , db : Session , id : int):
    new_blog = models.Blog(title=request.title , body=request.body , user_id = id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    pid = new_blog.user_id
    user = db.query(models.User).filter(models.User.id==id).first()
    await manager.broadcast(f"New blog created by {user.username} titled {new_blog.title}")
    return new_blog

def delete_by_id(id , db : Session):
    blog = db.query(models.Blog).filter(models.Blog.id==id)
    if not blog:
       raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , 
                           detail= f"Blog with {id} did not exists")
    blog.delete(synchronize_session=False) 
    db.commit() 
    return ({'msg' : 'content deleted'})

def updated_by_id(id:int , request:BLog2 , db : Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).update(
        {
            "title": request.title,
            "body": request.body
        },
        synchronize_session=False
    )
    if blog == 0:
       raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                           detail= f"Blog with {id} did not exists")
    
    db.commit() 
    return ({'msg' : 'content updated'})

def updatedPartiali_by_id(id:int , request:BLogPatch , db : Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
       raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                           detail= f"Blog with {id} did not exists")
    if request.title is not None:
        blog.title = request.title

    if request.body is not None:
        blog.body = request.body
    
    db.commit()
    db.refresh(blog)
    return ({'msg' : 'content updated'})