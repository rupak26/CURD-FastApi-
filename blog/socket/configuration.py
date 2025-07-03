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
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                disconnected.append(connection)
        # Remove any connections that failed
        for conn in disconnected:
            self.disconnect(conn)

    async def send_ping(self):
        while True:
            now = time.time
            for connection in list(self.active_connections):
                if now - self.last_pong.get(connection, 0) > 30:
                    await connection.close()
                    self.disconnect(connection)
                else:
                    try:
                        await connection.send_text("ping")
                    except Exception:
                        self.disconnect(connection)
            await asyncio.sleep(10) 
    
manager = ConnectionManager()