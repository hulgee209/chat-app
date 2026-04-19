import json
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

from client_handler import connect, disconnect, broadcast, get_online_count
from storage import save_message, save_system_message

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"

# css, js файлуудыг static байдлаар serve хийнэ
app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")


@app.get("/")
async def home():
    return FileResponse(FRONTEND_DIR / "index.html")


def now_time():
    return datetime.now().strftime("%H:%M:%S")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await connect(websocket)
    username = "Unknown user"

    try:
        while True:
            raw_data = await websocket.receive_text()
            data = json.loads(raw_data)

            message_type = data.get("type")

            if message_type == "join":
                username = data.get("username", "").strip()

                if not username:
                    await websocket.send_text(json.dumps({
                        "type": "error",
                        "message": "Нэр хоосон байж болохгүй."
                    }, ensure_ascii=False))
                    continue

                system_message = f"{username} чатад нэгдлээ."
                save_system_message(system_message)

                await broadcast(json.dumps({
                    "type": "system",
                    "message": system_message,
                    "time": now_time(),
                    "online": get_online_count()
                }, ensure_ascii=False))

            elif message_type == "chat":
                username = data.get("username", "").strip()
                message = data.get("message", "").strip()

                if not username:
                    await websocket.send_text(json.dumps({
                        "type": "error",
                        "message": "Нэрээ оруулна уу."
                    }, ensure_ascii=False))
                    continue

                if not message:
                    await websocket.send_text(json.dumps({
                        "type": "error",
                        "message": "Хоосон мессеж илгээж болохгүй."
                    }, ensure_ascii=False))
                    continue

                save_message(username, message)

                await broadcast(json.dumps({
                    "type": "chat",
                    "username": username,
                    "message": message,
                    "time": now_time()
                }, ensure_ascii=False))

    except WebSocketDisconnect:
        await disconnect(websocket)

        if username != "Unknown user":
            system_message = f"{username} чатнаас гарлаа."
            save_system_message(system_message)

            await broadcast(json.dumps({
                "type": "system",
                "message": system_message,
                "time": now_time(),
                "online": get_online_count()
            }, ensure_ascii=False))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)