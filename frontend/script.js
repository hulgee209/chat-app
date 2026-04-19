const statusText = document.getElementById("status");
const onlineCount = document.getElementById("online-count");
const usernameInput = document.getElementById("username");
const joinBtn = document.getElementById("join-btn");
const messageInput = document.getElementById("message-input");
const sendBtn = document.getElementById("send-btn");
const chatBox = document.getElementById("chat-box");

const socket = new WebSocket("ws://localhost:8000/ws");

let currentUser = "";
let hasJoined = false;

socket.onopen = () => {
  statusText.textContent = "Сервертэй холбогдлоо ✅";
};

socket.onclose = () => {
  statusText.textContent = "Серверээс саллаа ❌";
};

socket.onerror = () => {
  statusText.textContent = "Холболтын алдаа ⚠️";
};

socket.onmessage = (event) => {
  const data = JSON.parse(event.data);

  if (data.type === "system") {
    addSystemMessage(`${data.message} (${data.time})`);
    if (typeof data.online !== "undefined") {
      onlineCount.textContent = data.online;
    }
    return;
  }

  if (data.type === "error") {
    addErrorMessage(data.message);
    return;
  }

  if (data.type === "chat") {
    const type = data.username === currentUser ? "me" : "other";
    addMessage(data.username, data.message, data.time, type);
  }
};

function joinChat() {
  const username = usernameInput.value.trim();

  if (!username) {
    addErrorMessage("Нэрээ эхлээд оруулна уу.");
    return;
  }

  currentUser = username;
  hasJoined = true;

  socket.send(JSON.stringify({
    type: "join",
    username: currentUser
  }));

  usernameInput.disabled = true;
  joinBtn.disabled = true;
  joinBtn.textContent = "Нэгдсэн";
}

function sendMessage() {
  const message = messageInput.value.trim();

  if (!hasJoined) {
    addErrorMessage("Эхлээд чатад нэгдэнэ үү.");
    return;
  }

  if (!message) return;

  socket.send(JSON.stringify({
    type: "chat",
    username: currentUser,
    message: message
  }));

  messageInput.value = "";
}

function addMessage(username, message, time, type) {
  const messageDiv = document.createElement("div");
  messageDiv.classList.add("message", type);

  messageDiv.innerHTML = `
    <div class="meta">${escapeHtml(username)}</div>
    <div>${escapeHtml(message)}</div>
    <div class="time">${escapeHtml(time)}</div>
  `;

  chatBox.appendChild(messageDiv);
  scrollToBottom();
}

function addSystemMessage(message) {
  const systemDiv = document.createElement("div");
  systemDiv.classList.add("system-message");
  systemDiv.textContent = message;

  chatBox.appendChild(systemDiv);
  scrollToBottom();
}

function addErrorMessage(message) {
  const errorDiv = document.createElement("div");
  errorDiv.classList.add("error-message");
  errorDiv.textContent = message;

  chatBox.appendChild(errorDiv);
  scrollToBottom();
}

function scrollToBottom() {
  chatBox.scrollTop = chatBox.scrollHeight;
}

function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

joinBtn.addEventListener("click", joinChat);
sendBtn.addEventListener("click", sendMessage);

messageInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") {
    sendMessage();
  }
});

usernameInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") {
    joinChat();
  }
});