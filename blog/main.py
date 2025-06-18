from fastapi import FastAPI , APIRouter , HTTPException
from .domain import models
from .Database import engine
from .exceptions.exceptions import (
    validation_exception_handler,
    integrity_exception_handler,
    sqlalchemy_exception_handler,
    http_exception_handler,
    general_exception_handler,
)
from .routers import user , blog , authentications
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError 


app = FastAPI() 

models.Base.metadata.create_all(engine) 

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(IntegrityError, integrity_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

app.include_router(authentications.router)
app.include_router(user.router) 
app.include_router(blog.router)


