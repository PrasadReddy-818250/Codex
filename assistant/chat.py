from __future__ import annotations

from dataclasses import dataclass

from assistant.config import AppConfig
from assistant.model_client import LocalModelClient, MockModelClient
from assistant.policy import SYSTEM_POLICY, SafetyDecision, assess_user_message
from assistant.rag import KnowledgeBase, RetrievalResult, format_context


@dataclass(frozen=True)
class ChatResponse:
    answer: str
    retrieved: list[RetrievalResult]
    safety: SafetyDecision


class ChatService:
    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self.knowledge_base = KnowledgeBase.load_jsonl(config.rag_path)
        if config.mock_model:
            self.model_client = MockModelClient()
        else:
            self.model_client = LocalModelClient(
                config.model_endpoint,
                config.model_name,
                timeout_seconds=config.model_timeout_seconds,
                max_tokens=config.model_max_tokens,
            )

    async def answer(self, message: str, history: list[dict[str, str]] | None = None) -> ChatResponse:
        safety = assess_user_message(message)
        if not safety.allowed:
            return ChatResponse(answer=safety.reason or "Request blocked.", retrieved=[], safety=safety)

        retrieved = self.knowledge_base.search(message, limit=self.config.max_retrieved_chunks)
        context = format_context(retrieved)
        confirmation_note = ""
        if safety.needs_confirmation:
            confirmation_note = (
                "\nThe user request appears destructive. Explain risk, provide review-safe guidance, "
                "and do not provide execution instructions unless explicit confirmation is present."
            )

        messages = [
            {"role": "system", "content": SYSTEM_POLICY + confirmation_note},
            {
                "role": "system",
                "content": (
                    "Retrieved context follows. Use it when relevant and cite source URLs. "
                    "For code-generation tasks, follow any retrieved API usage constraints exactly. "
                    "Do not invent imports, functions, or success claims beyond the retrieved context.\n\n"
                    + context
                ),
            },
        ]
        for item in history or []:
            if item.get("role") in {"user", "assistant"} and item.get("content"):
                messages.append({"role": item["role"], "content": item["content"]})
        messages.append({"role": "user", "content": message})

        answer = await self.model_client.chat(messages)
        return ChatResponse(answer=answer, retrieved=retrieved, safety=safety)
