from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from assistant.chat import ChatService
from assistant.config import AppConfig
from assistant.model_client import ModelClientError


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str = Field(min_length=1)
    history: list[ChatMessage] = Field(default_factory=list)


class Citation(BaseModel):
    title: str
    source_url: str
    product: str
    dialect: str
    score: float


class ChatResponse(BaseModel):
    answer: str
    citations: list[Citation]
    needs_confirmation: bool


config = AppConfig.from_env()
chat_service = ChatService(config)
app = FastAPI(title="Local Frank SQL/Python GPT", version="0.1.0")


@app.get("/", response_class=HTMLResponse)
async def index() -> str:
    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Local Frank SQL/Python GPT</title>
  <style>
    :root { color-scheme: light; font-family: Segoe UI, Arial, sans-serif; }
    body { margin: 0; background: #f6f7f9; color: #17191c; }
    main { max-width: 1040px; margin: 0 auto; padding: 24px; }
    header { display: flex; justify-content: space-between; gap: 16px; align-items: center; margin-bottom: 18px; }
    h1 { font-size: 22px; margin: 0; }
    .status { font-size: 13px; color: #515a66; }
    #chat { background: #fff; border: 1px solid #d8dde5; border-radius: 8px; min-height: 58vh; padding: 16px; overflow-y: auto; }
    .msg { padding: 12px 14px; border-radius: 8px; margin: 0 0 12px; white-space: pre-wrap; line-height: 1.45; }
    .user { background: #e8f0fe; margin-left: 10%; }
    .assistant { background: #f1f3f5; margin-right: 10%; }
    .meta { font-size: 12px; color: #5f6875; margin-top: 8px; }
    form { display: grid; grid-template-columns: 1fr auto; gap: 10px; margin-top: 14px; }
    textarea { min-height: 76px; resize: vertical; border: 1px solid #cbd3df; border-radius: 8px; padding: 12px; font: inherit; }
    button { border: 0; border-radius: 8px; padding: 0 18px; background: #1f6feb; color: white; font-weight: 600; cursor: pointer; }
    button:disabled { background: #8aaee8; cursor: wait; }
  </style>
</head>
<body>
<main>
  <header>
    <h1>Local Frank SQL/Python GPT</h1>
    <div class="status">Local web UI. Model endpoint must run separately.</div>
  </header>
  <section id="chat" aria-live="polite"></section>
  <form id="form">
    <textarea id="message" placeholder="Ask SQL, Db2, AS400, Python, pandas, PySpark, Airflow, or connector questions."></textarea>
    <button id="send" type="submit">Send</button>
  </form>
</main>
<script>
const chat = document.getElementById("chat");
const form = document.getElementById("form");
const input = document.getElementById("message");
const send = document.getElementById("send");
const history = [];

function addMessage(role, content, meta) {
  const div = document.createElement("div");
  div.className = `msg ${role}`;
  div.textContent = content;
  if (meta) {
    const small = document.createElement("div");
    small.className = "meta";
    small.textContent = meta;
    div.appendChild(small);
  }
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const message = input.value.trim();
  if (!message) return;
  input.value = "";
  send.disabled = true;
  addMessage("user", message);
  history.push({ role: "user", content: message });
  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, history: history.slice(-8) })
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "Request failed");
    const citationText = data.citations.length ? `Sources: ${data.citations.map(c => c.source_url || c.title).join(", ")}` : "";
    addMessage("assistant", data.answer, citationText);
    history.push({ role: "assistant", content: data.answer });
  } catch (error) {
    addMessage("assistant", `Local app error: ${error.message}`);
  } finally {
    send.disabled = false;
    input.focus();
  }
});
</script>
</body>
</html>"""


@app.get("/health")
async def health() -> dict[str, object]:
    return {
        "status": "ok",
        "mock_model": config.mock_model,
        "rag_path": str(config.rag_path),
    }


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    try:
        result = await chat_service.answer(
            request.message,
            history=[message.model_dump() for message in request.history],
        )
    except ModelClientError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    return ChatResponse(
        answer=result.answer,
        needs_confirmation=result.safety.needs_confirmation,
        citations=[
            Citation(
                title=item.chunk.title,
                source_url=item.chunk.source_url,
                product=item.chunk.product,
                dialect=item.chunk.dialect,
                score=round(item.score, 4),
            )
            for item in result.retrieved
        ],
    )
