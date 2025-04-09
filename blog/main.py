from fastapi import FastAPI , APIRouter
from . import models
from .Database import engine
from .routers import user , blog , authentications

app = FastAPI() 

models.Base.metadata.create_all(engine) 

app.include_router(authentications.router)
app.include_router(user.router) 
app.include_router(blog.router)


