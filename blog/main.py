from fastapi import (
             FastAPI , APIRouter , HTTPException , Depends , Query ,
             WebSocket , WebSocketDisconnect , status , Request
)
from typing import List 
from .domain import models , schemas
from .Database import engine
from .routers import user , blog , authentications
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse , HTMLResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError 
from .socket.configuration import manager
from .response.schema import ApiResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging , os
from cofig2.logging_config import setup_logging
import time , asyncio
from sqlalchemy import insert, select
from .core import swagger_doc as s 
from .routers.oauth2 import role_required
from .routers.token import verify_token
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt
from .routers.token import verify_token
setup_logging()
logger = logging.getLogger(__name__)
app = FastAPI() 
models.Base.metadata.create_all(engine) 


# Utility to extract the token from the query parameters or headers
async def get_jwt_token(websocket: WebSocket):
    # Try to get the token from query parameters
    token = websocket.query_params.get("token")
    if not token:
        # If no token is passed, try the headers
        token = websocket.headers.get("Authorization")
        #print(f"Token from headers------->: {token}")
        if token:
            token = token.split(" ")[1]  # Bearer token format
    return token

# Secure WebSocket endpoint
@app.websocket("/wss")
async def websocket_endpoint(websocket: WebSocket, token: str = Depends(get_jwt_token)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = verify_token(token , credentials_exception)
  #  print(f"Payload from token-----12-->: {payload}")
    if not payload["user_id"]:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Received your message: {data}")

    except Exception:
        manager.disconnect(websocket)
    finally:
        manager.disconnect(websocket)





@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"→ {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"← {request.method} {request.url} — {response.status_code}")
    return response

# Custom error response format
def custom_error_response(status_code: int, message: str , errorDetails : str):
    # return ApiResponse(
    #     message = message , 
    #     statusCode = status_code , 
    #     datalist = errorDetails 
    # )
    return JSONResponse( 
        status_code=status_code,
        content= {
            "statusCode": status_code,
            "message" : message,
            "ErrDetails" : errorDetails
        }
    )

@app.exception_handler(StarletteHTTPException)
async def handle_http_exception(request: Request, exc: StarletteHTTPException):
    if exc.status_code == status.HTTP_404_NOT_FOUND:
        return custom_error_response(404, "Resource not found", str(exc))
    elif exc.status_code == status.HTTP_403_FORBIDDEN:
        return custom_error_response(403, "Forbidden access", str(exc))
    elif exc.status_code == status.HTTP_401_UNAUTHORIZED:
        return custom_error_response(401, "Unauthorized access", str(exc))
    elif exc.status_code == status.HTTP_502_BAD_GATEWAY:
        return custom_error_response(502, "Bad gateway", str(exc))
    else:
        return custom_error_response(exc.status_code, exc.detail, str(exc))



app.include_router(authentications.router)
app.include_router(user.router) 
app.include_router(blog.router)


