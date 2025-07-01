from ..Database import Base , engine 
from sqlalchemy import Column , Integer , String , ForeignKey 
from sqlalchemy.orm import relationship 


class Blog(Base):
    __tablename__ = 'blog' 
    
    id = Column(Integer , primary_key = True , index = True)
    title = Column(String(100))
    body = Column(String(200)) 
    user_id = Column(Integer , ForeignKey('users.id'))
    
    creator = relationship("User" , back_populates="blogs")


class User(Base):
    __tablename__ = 'users' 

    id = Column(Integer , primary_key = True , index = True)
    username = Column(String(100))
    email = Column(String(200))
    password = Column(String(100)) 
    role = Column(String(200))
    
    
    blogs = relationship("Blog" , back_populates = "creator")
