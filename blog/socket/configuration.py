from fastapi import WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from typing import List
import asyncio
import time

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.last_pong: dict[WebSocket, float] = {}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.last_pong[websocket] = time.time()

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
           self.active_connections.remove(websocket)
           del self.last_pong[websocket]

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)
    
manager = ConnectionManager()