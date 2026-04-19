import json
import os
from datetime import datetime

CHAT_LOG_FILE = "chat_history.json"


def _ensure_file():
    if not os.path.exists(CHAT_LOG_FILE):
        with open(CHAT_LOG_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)


def now_full():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def now_time():
    return datetime.now().strftime("%H:%M:%S")


def load_history(limit=50):
    _ensure_file()
    with open(CHAT_LOG_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data[-limit:]


def save_event(event: dict):
    _ensure_file()
    with open(CHAT_LOG_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    data.append(event)

    with open(CHAT_LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def create_chat_message(message_id: int, username: str, message: str):
    return {
        "id": message_id,
        "type": "chat",
        "username": username,
        "message": message,
        "time": now_time(),
        "created_at": now_full(),
    }


def create_system_message(message_id: int, message: str):
    return {
        "id": message_id,
        "type": "system",
        "message": message,
        "time": now_time(),
        "created_at": now_full(),
    }