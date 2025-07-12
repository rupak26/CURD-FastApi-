from database import Base , engine 
from sqlalchemy import Column , Integer , String , ForeignKey , Text, DateTime, func
from sqlalchemy.orm import relationship 


class User(Base):
    __tablename__ = 'users' 

    id = Column(Integer , primary_key = True , index = True)
    username = Column(String(100))
    email = Column(String(200))
    password = Column(String(100)) 
    role = Column(String(200))