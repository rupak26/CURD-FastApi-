from  sqlalchemy.orm import Session  
from .. import models
from ..schemas import BLog2 , User2 , showBlog , showUser
from fastapi import  status , Response , HTTPException , APIRouter

def get_all(db : Session):
    return  db.query(models.Blog).all() 
    
def me(db:Session , id:int):
    return db.query(models.User).filter(models.User.id == id).first()

def get_by_id(id , db : Session):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if blog is None:
       raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , 
                           detail= f"Blog with {id} did not exists")
    return blog 

def create(request:BLog2 , db : Session , id : int):
    new_blog = models.Blog(title=request.title , body=request.body , user_id = id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
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