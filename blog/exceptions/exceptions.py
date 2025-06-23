from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException
from fastapi.exception_handlers import request_validation_exception_handler
from ..response.schema import ApiResponse

# Handle Pydantic validation errors globally
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for err in exc.errors():
        field = ".".join(str(loc) for loc in err["loc"][1:])  # skip 'body'
        errors.append(f"{field}: {err['msg']}")
        
    return ApiResponse(
            message = "Validation Error" ,
            statusCode =  status.HTTP_422_UNPROCESSABLE_ENTITY ,
            datalist = []
        )


# Handle database integrity errors globally (e.g. duplicate keys)
async def integrity_exception_handler(request: Request, exc: IntegrityError):
    return ApiResponse(
            message = "Integrity error - possible duplicate or constraint violation.",
            statusCode =  status.HTTP_409_CONFLICT ,
            datalist = []
        )


# Handle SQLAlchemy general errors
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    return ApiResponse(
            message = "Database error occurred.",
            statusCode =  status.HTTP_500_INTERNAL_SERVER_ERROR,
            datalist = []
        )


# Handle HTTPExceptions explicitly (optional, FastAPI already does this)
async def http_exception_handler(request: Request, exc: HTTPException):
     return ApiResponse(
            message = str(exc.detail),
            statusCode =  404,
            datalist = []
        )
    


# Catch-all handler for unhandled exceptions
async def general_exception_handler(request: Request, exc: Exception):
    return ApiResponse(
            message =  "An unexpected error occurred. Please try again later.",
            statusCode =  status.HTTP_500_INTERNAL_SERVER_ERROR,
            datalist = []
        )
    

