from fastapi import WebSocket

active_connections = []


async def connect(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)


async def disconnect(websocket: WebSocket):
    if websocket in active_connections:
        active_connections.remove(websocket)


async def broadcast(message: str):
    disconnected_clients = []

    for connection in active_connections:
        try:
            await connection.send_text(message)
        except Exception:
            disconnected_clients.append(connection)

    for client in disconnected_clients:
        if client in active_connections:
            active_connections.remove(client)


def get_online_count():
    return len(active_connections)