from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _bool_env(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class AppConfig:
    host: str
    port: int
    model_endpoint: str
    model_name: str
    rag_path: Path
    mock_model: bool
    max_retrieved_chunks: int

    @classmethod
    def from_env(cls) -> "AppConfig":
        return cls(
            host=os.getenv("ASSISTANT_HOST", "127.0.0.1"),
            port=int(os.getenv("ASSISTANT_PORT", "8000")),
            model_endpoint=os.getenv(
                "ASSISTANT_MODEL_ENDPOINT",
                "http://127.0.0.1:8080/v1/chat/completions",
            ),
            model_name=os.getenv("ASSISTANT_MODEL_NAME", "qwen2.5-coder-3b-instruct-q4_k_m"),
            rag_path=Path(os.getenv("ASSISTANT_RAG_PATH", "data/samples/knowledge.jsonl")),
            mock_model=_bool_env("ASSISTANT_MOCK_MODEL", False),
            max_retrieved_chunks=int(os.getenv("ASSISTANT_MAX_RETRIEVED_CHUNKS", "4")),
        )
