const statusText = document.getElementById("status");
const usernameInput = document.getElementById("username");
const joinBtn = document.getElementById("join-btn");
const onlineCount = document.getElementById("online-count");
const userList = document.getElementById("user-list");
const chatBox = document.getElementById("chat-box");
const messageInput = document.getElementById("message-input");
const sendBtn = document.getElementById("send-btn");

const socket = new WebSocket("ws://localhost:8000/ws");

let currentUser = "";
let joined = false;
let renderedIds = new Set();

socket.onopen = () => {
  statusText.textContent = "Сервертэй холбогдлоо ";
};

socket.onclose = () => {
  statusText.textContent = "Серверээс саллаа ❌";
};

socket.onerror = () => {
  statusText.textContent = "Холболтын алдаа ⚠️";
};

socket.onmessage = (event) => {
  const data = JSON.parse(event.data);

  if (data.type === "history") {
    onlineCount.textContent = data.online_count ?? 0;
    renderUserList(data.users || []);
    (data.messages || []).forEach(renderIncomingMessage);
    return;
  }

  if (data.type === "online_users") {
    onlineCount.textContent = data.online_count ?? 0;
    renderUserList(data.users || []);
    return;
  }

  if (data.type === "error") {
    addErrorMessage(data.message);
    return;
  }

  renderIncomingMessage(data);
};

function renderIncomingMessage(data) {
  if (data.id && renderedIds.has(data.id)) return;
  if (data.id) renderedIds.add(data.id);

  if (data.type === "system") {
    addSystemMessage(`${data.message} (${data.time})`);
    return;
  }

  if (data.type === "chat") {
    const messageType = data.username === currentUser ? "me" : "other";
    addMessage(data.username, data.message, data.time, messageType);
  }
}

function joinChat() {
  const username = usernameInput.value.trim();

  if (!username) {
    addErrorMessage("Нэрээ оруулна уу.");
    return;
  }

  if (joined) return;

  currentUser = username;
  socket.send(
    JSON.stringify({
      type: "join",
      username: username,
    })
  );

  joined = true;
  usernameInput.disabled = true;
  joinBtn.disabled = true;
  joinBtn.textContent = "Нэгдсэн";
}

function sendMessage() {
  const message = messageInput.value.trim();

  if (!joined) {
    addErrorMessage("Эхлээд чатад нэгдэнэ үү.");
    return;
  }

  if (!message) return;

  socket.send(
    JSON.stringify({
      type: "chat",
      message: message,
    })
  );

  messageInput.value = "";
  messageInput.focus();
}

function addMessage(username, message, time, type) {
  const div = document.createElement("div");
  div.className = `message ${type}`;
  div.innerHTML = `
    <div class="meta">${escapeHtml(username)}</div>
    <div>${escapeHtml(message)}</div>
    <div class="time">${escapeHtml(time || "")}</div>
  `;
  chatBox.appendChild(div);
  scrollToBottom();
}

function addSystemMessage(message) {
  const div = document.createElement("div");
  div.className = "system-message";
  div.textContent = message;
  chatBox.appendChild(div);
  scrollToBottom();
}

function addErrorMessage(message) {
  const div = document.createElement("div");
  div.className = "error-message";
  div.textContent = message;
  chatBox.appendChild(div);
  scrollToBottom();
}

function renderUserList(users) {
  userList.innerHTML = "";

  users.forEach((user) => {
    const li = document.createElement("li");
    li.textContent = user;
    userList.appendChild(li);
  });
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

usernameInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") joinChat();
});

messageInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") sendMessage();
});