from fastapi import (
             FastAPI , APIRouter , HTTPException ,
             WebSocket , WebSocketDisconnect 
)
from fastapi.responses import HTMLResponse
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
from .socket.configuration import manager


app = FastAPI() 


models.Base.metadata.create_all(engine) 

@app.websocket("/ws/notifications")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # keep alive, or handle incoming messages
    except WebSocketDisconnect:
        await manager.disconnect(websocket)

@app.get("/test-broadcast")
async def test_broadcast():
    await manager.broadcast("🚨 New blog created!")
    return {"message": "Broadcast sent"}

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
                    let item = document.createElement("li");
                    item.textContent = event.data;
                    document.getElementById("notifications").appendChild(item);
                };
            </script>
        </body>
        </html>
    ''')

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(IntegrityError, integrity_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

app.include_router(authentications.router)
app.include_router(user.router) 
app.include_router(blog.router)


