# Chat App

Энэ бол Python, FastAPI, WebSocket ашигласан энгийн real-time chat application юм. Олон хэрэглэгч нэгэн зэрэг холбогдож, мессежээ шууд солилцоно. Мөн chat history нь файлд хадгалагдана.

## Ашигласан технологи

- Python
- FastAPI
- Uvicorn
- WebSocket
- HTML
- CSS
- JavaScript

## Төслийн бүтэц

```text
backend/
  server.py
  client_handler.py
  storage.py
  requirements.txt

frontend/
  index.html
  style.css
  script.js
```

## Үндсэн боломжууд

- Real-time chat
- Олон хэрэглэгч зэрэг холбогдоно
- Join/leave мэдээлэл харагдана
- Chat history хадгалагдана
- Өөрийн мессеж баруун талд, бусдынх зүүн талд харагдана

## History хадгалах файлууд

- `backend/chat.txt`
- `backend/chat_history.json`

## Шаардлага хангаж байгаа эсэх

- OOP: `client_handler.py` дотор `ConnectionManager` class ашигласан
- TCP/IP: WebSocket нь TCP/IP дээр ажилладаг
- Chat history: мессежүүд локал файлд хадгалагддаг

## Суулгах

```powershell
cd backend
python -m pip install -r requirements.txt
```

## Ажиллуулах

1. Backend асаах:

```powershell
cd backend
python server.py
```

2. Frontend нээх:

`frontend/index.html` файлаа browser-оор нээнэ.

Эсвэл:

```powershell
cd frontend
python -m http.server 5500
```

Дараа нь:

```text
http://127.0.0.1:5500/index.html
```

## Ашиглах

1. Нэрээ оруулна
2. `Join` дарна
3. Мессежээ бичээд `Send` дарна
4. Олон tab нээгээд олон хэрэглэгч шиг туршиж болно

## Товч дүгнэлт

Энэ төсөл нь OOP бүтэцтэй, TCP/IP дээр ажилладаг, chat history хадгалдаг энгийн real-time chat app юм.
