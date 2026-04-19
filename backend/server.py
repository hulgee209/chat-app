# backend/server.py

import asyncio
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from client_handler import connect, disconnect, broadcast
from storage import save_message

app = FastAPI()

# Frontend холбогдох боломжтой болгоно
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            
            # Мессеж хадгалах
            save_message(data)
            
            # Бүх хэрэглэгч рүү тараах
            await broadcast(data)

    except:
        await disconnect(websocket)

# Сервер ажиллуулах
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)