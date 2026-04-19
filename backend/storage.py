from datetime import datetime

CHAT_LOG_FILE = "chat_history.txt"


def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def save_message(username: str, message: str):
    timestamp = get_timestamp()
    with open(CHAT_LOG_FILE, "a", encoding="utf-8") as file:
        file.write(f"[{timestamp}] {username}: {message}\n")


def save_system_message(message: str):
    timestamp = get_timestamp()
    with open(CHAT_LOG_FILE, "a", encoding="utf-8") as file:
        file.write(f"[{timestamp}] SYSTEM: {message}\n")