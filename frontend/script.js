const messages = document.getElementById("messages");
const usernameInput = document.getElementById("usernameInput");
const joinButton = document.getElementById("joinButton");
const messageInput = document.getElementById("messageInput");
const sendButton = document.getElementById("sendButton");

const socket = new WebSocket("ws://localhost:8000/ws");

let joined = false;
let currentUsername = "";

function getInitials(name) {
  const parts = name.trim().split(/\s+/).filter(Boolean);

  if (parts.length === 0) {
    return "?";
  }

  return parts
    .slice(0, 2)
    .map(function (part) {
      return part[0].toUpperCase();
    })
    .join("");
}

function appendEntry(entry) {
  if (entry.type === "system") {
    const element = document.createElement("div");
    element.className = "system-message";
    element.textContent = `[${entry.time}] ${entry.message}`;
    messages.appendChild(element);
  } else if (entry.type === "chat") {
    const row = document.createElement("div");
    const isMine = entry.username === currentUsername;

    row.className = isMine ? "message-row my-message" : "message-row other-message";

    const avatar = document.createElement("div");
    avatar.className = "message-avatar";
    avatar.textContent = getInitials(entry.username);

    const element = document.createElement("div");
    element.className = "message";

    const meta = document.createElement("div");
    meta.className = "message-meta";
    meta.textContent = `${entry.username} | ${entry.time}`;

    const text = document.createElement("div");
    text.textContent = entry.message;

    element.appendChild(meta);
    element.appendChild(text);

    if (isMine) {
      row.appendChild(element);
    } else {
      row.appendChild(avatar);
      row.appendChild(element);
    }

    messages.appendChild(row);
  } else {
    return;
  }

  messages.scrollTop = messages.scrollHeight;
}

socket.onerror = function () {
  console.error("WebSocket connection failed. Make sure the backend server is running on port 8000.");
};

socket.onclose = function () {
  console.error("WebSocket connection closed.");
};

socket.onmessage = function (event) {
  const data = JSON.parse(event.data);

  if (data.type === "history") {
    messages.innerHTML = "";
    data.messages.forEach(appendEntry);
    return;
  }

  appendEntry(data);
};

function joinChat() {
  const username = usernameInput.value.trim();

  if (username === "") {
    return;
  }

  if (socket.readyState !== WebSocket.OPEN) {
    console.error("WebSocket is not connected yet.");
    return;
  }

  socket.send(
    JSON.stringify({
      action: "join",
      username: username,
    })
  );

  currentUsername = username;
  joined = true;
  usernameInput.disabled = true;
  joinButton.disabled = true;
  messageInput.disabled = false;
  sendButton.disabled = false;
  messageInput.focus();
}

function sendMessage() {
  const message = messageInput.value.trim();

  if (!joined || message === "") {
    return;
  }

  if (socket.readyState !== WebSocket.OPEN) {
    console.error("WebSocket is not connected yet.");
    return;
  }

  socket.send(
    JSON.stringify({
      action: "message",
      message: message,
    })
  );

  messageInput.value = "";
  messageInput.focus();
}

joinButton.addEventListener("click", joinChat);
sendButton.addEventListener("click", sendMessage);

usernameInput.addEventListener("keydown", function (event) {
  if (event.key === "Enter") {
    joinChat();
  }
});

messageInput.addEventListener("keydown", function (event) {
  if (event.key === "Enter") {
    sendMessage();
  }
});
