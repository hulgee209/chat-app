from fastapi import WebSocket


class ConnectionManager:
    def __init__(self) -> None:
        self.connected_clients: list[WebSocket] = []
        self.usernames: dict[WebSocket, str] = {}

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.connected_clients.append(websocket)

    def disconnect(self, websocket: WebSocket) -> str | None:
        if websocket in self.connected_clients:
            self.connected_clients.remove(websocket)

        return self.usernames.pop(websocket, None)

    def set_username(self, websocket: WebSocket, username: str) -> None:
        self.usernames[websocket] = username

    def get_username(self, websocket: WebSocket) -> str | None:
        return self.usernames.get(websocket)

    async def send_json(self, websocket: WebSocket, payload: dict) -> None:
        await websocket.send_json(payload)

    async def broadcast_json(self, payload: dict) -> None:
        disconnected_clients: list[WebSocket] = []

        for client in self.connected_clients:
            try:
                await client.send_json(payload)
            except Exception:
                disconnected_clients.append(client)

        for client in disconnected_clients:
            self.disconnect(client)


manager = ConnectionManager()
