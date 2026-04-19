from fastapi import WebSocket

active_connections = []
client_usernames = {}  # websocket -> username


async def connect(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)


async def disconnect(websocket: WebSocket):
    if websocket in active_connections:
        active_connections.remove(websocket)
    if websocket in client_usernames:
        del client_usernames[websocket]


def set_username(websocket: WebSocket, username: str):
    client_usernames[websocket] = username


def get_username(websocket: WebSocket):
    return client_usernames.get(websocket)


def get_online_count():
    return len(active_connections)


def get_online_users():
    return list(client_usernames.values())


def is_username_taken(username: str):
    return username in client_usernames.values()


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
        if client in client_usernames:
            del client_usernames[client]


async def send_to_one(websocket: WebSocket, message: str):
    await websocket.send_text(message)