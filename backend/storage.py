import json
from datetime import datetime
from pathlib import Path


CHAT_TEXT_FILE = Path(__file__).with_name("chat.txt")
CHAT_HISTORY_FILE = Path(__file__).with_name("chat_history.json")


def _read_history() -> list[dict]:
    if not CHAT_HISTORY_FILE.exists():
        return []

    try:
        with CHAT_HISTORY_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, OSError):
        return []

    if isinstance(data, list):
        return data

    return []


def load_history() -> list[dict]:
    return _read_history()


def _write_history(history: list[dict]) -> None:
    with CHAT_HISTORY_FILE.open("w", encoding="utf-8") as file:
        json.dump(history, file, ensure_ascii=False, indent=2)


def _append_text_line(line: str) -> None:
    with CHAT_TEXT_FILE.open("a", encoding="utf-8") as file:
        file.write(line + "\n")


def _build_entry(entry_type: str, message: str, username: str | None = None) -> dict:
    history = _read_history()
    now = datetime.now()

    entry = {
        "id": len(history) + 1,
        "type": entry_type,
        "message": message,
        "time": now.strftime("%H:%M:%S"),
        "created_at": now.strftime("%Y-%m-%d %H:%M:%S"),
    }

    if username:
        entry["username"] = username

    history.append(entry)
    _write_history(history)
    return entry


def save_system_message(message: str) -> dict:
    entry = _build_entry("system", message)
    _append_text_line(f"[{entry['time']}] {message}")
    return entry


def save_chat_message(username: str, message: str) -> dict:
    entry = _build_entry("chat", message, username=username)
    _append_text_line(f"[{entry['time']}] {username}: {message}")
    return entry
