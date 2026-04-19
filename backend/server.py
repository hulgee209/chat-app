from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn

from client_handler import manager
from storage import load_history, save_chat_message, save_system_message


app = FastAPI()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    await manager.connect(websocket)
    await manager.send_json(
        websocket,
        {
            "type": "history",
            "messages": load_history(),
        },
    )

    try:
        while True:
            data = await websocket.receive_json()
            action = data.get("action")

            if action == "join":
                username = str(data.get("username", "")).strip()
                if username == "":
                    continue

                manager.set_username(websocket, username)
                entry = save_system_message(f"{username} чатад нэгдлээ.")
                await manager.broadcast_json(entry)

            elif action == "message":
                username = manager.get_username(websocket)
                message = str(data.get("message", "")).strip()

                if not username or message == "":
                    continue

                entry = save_chat_message(username, message)
                await manager.broadcast_json(entry)
    except WebSocketDisconnect:
        username = manager.disconnect(websocket)

        if username:
            entry = save_system_message(f"{username} чатнаас гарлаа.")
            await manager.broadcast_json(entry)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
