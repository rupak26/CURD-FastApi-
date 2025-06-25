from fastapi import (
             FastAPI , APIRouter , HTTPException , 
             WebSocket , WebSocketDisconnect , status , Request
)
from fastapi.responses import HTMLResponse
from .domain import models
from .Database import engine
from .routers import user , blog , authentications
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError 
from .socket.configuration import manager
from .response.schema import ApiResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging
from cofig2.logging_config import setup_logging
import time , asyncio


setup_logging()
logger = logging.getLogger(__name__)
app = FastAPI() 


models.Base.metadata.create_all(engine) 

@app.websocket("/ws/notifications")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()  # keep alive, or handle incoming messages
            if data == "pong":
                manager.last_pong[websocket] = time.time()
            else:
                await manager.broadcast(f"Message: {data}")
    except WebSocketDisconnect:
        await manager.disconnect(websocket)

@app.get("/test-broadcast")
async def test_broadcast():
    await manager.broadcast("🚨 New blog created!")
    return {"message": "Broadcast sent"}

@app.on_event("startup")
async def start_ping_loop():
    asyncio.create_task(manager.send_ping())


@app.get("/")
async def get():
    return HTMLResponse('''
        <!DOCTYPE html>
        <html>
        <body>
            <h2>Blog Notification</h2>
            <ul id="notifications"></ul>
            <script>      
                let ws = new WebSocket("ws://localhost:8000/ws/notifications");         
                ws.onmessage = function(event) {
                    if (event.data === "ping") {
                        ws.send("pong");
                    } else {
                        console.log("Received:", event.data);
                        let item = document.createElement("li");
                        item.textContent = event.data;
                        document.getElementById("notifications").appendChild(item);
                    }
                };
            </script>
        </body>
        </html>
    ''')


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


