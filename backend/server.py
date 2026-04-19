import json
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

from client_handler import (
    connect,
    disconnect,
    broadcast,
    send_to_one,
    get_online_count,
    get_online_users,
    set_username,
    get_username,
    is_username_taken,
)
from storage import (
    load_history,
    save_event,
    create_chat_message,
    create_system_message,
)

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

app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

message_id_counter = 1


def next_message_id():
    global message_id_counter
    current = message_id_counter
    message_id_counter += 1
    return current


def build_online_payload():
    return {
        "type": "online_users",
        "online_count": get_online_count(),
        "users": get_online_users(),
    }


@app.get("/")
async def home():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await connect(websocket)

    try:
        history = load_history(50)
        await send_to_one(
            websocket,
            json.dumps(
                {
                    "type": "history",
                    "messages": history,
                    "online_count": get_online_count(),
                    "users": get_online_users(),
                },
                ensure_ascii=False,
            ),
        )

        await broadcast(json.dumps(build_online_payload(), ensure_ascii=False))

        while True:
            raw_data = await websocket.receive_text()
            data = json.loads(raw_data)

            msg_type = data.get("type")

            if msg_type == "join":
                username = data.get("username", "").strip()

                if not username:
                    await send_to_one(
                        websocket,
                        json.dumps(
                            {
                                "type": "error",
                                "message": "Нэр хоосон байж болохгүй.",
                            },
                            ensure_ascii=False,
                        ),
                    )
                    continue

                if is_username_taken(username):
                    await send_to_one(
                        websocket,
                        json.dumps(
                            {
                                "type": "error",
                                "message": "Энэ нэр ашиглагдаж байна. Өөр нэр сонгоно уу.",
                            },
                            ensure_ascii=False,
                        ),
                    )
                    continue

                set_username(websocket, username)

                system_event = create_system_message(
                    next_message_id(), f"{username} чатад нэгдлээ."
                )
                save_event(system_event)

                await broadcast(json.dumps(system_event, ensure_ascii=False))
                await broadcast(json.dumps(build_online_payload(), ensure_ascii=False))

            elif msg_type == "chat":
                username = get_username(websocket)
                message = data.get("message", "").strip()

                if not username:
                    await send_to_one(
                        websocket,
                        json.dumps(
                            {
                                "type": "error",
                                "message": "Эхлээд чатад нэгдэнэ үү.",
                            },
                            ensure_ascii=False,
                        ),
                    )
                    continue

                if not message:
                    await send_to_one(
                        websocket,
                        json.dumps(
                            {
                                "type": "error",
                                "message": "Хоосон мессеж илгээж болохгүй.",
                            },
                            ensure_ascii=False,
                        ),
                    )
                    continue

                chat_event = create_chat_message(
                    next_message_id(), username, message
                )
                save_event(chat_event)
                await broadcast(json.dumps(chat_event, ensure_ascii=False))

    except WebSocketDisconnect:
        username = get_username(websocket)
        await disconnect(websocket)

        if username:
            system_event = create_system_message(
                next_message_id(), f"{username} чатнаас гарлаа."
            )
            save_event(system_event)
            await broadcast(json.dumps(system_event, ensure_ascii=False))

        await broadcast(json.dumps(build_online_payload(), ensure_ascii=False))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)