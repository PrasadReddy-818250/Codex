from __future__ import annotations

import hashlib
import json
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


TOKEN_RE = re.compile(r"[A-Za-z0-9_.$:-]+")
VECTOR_SIZE = 256


@dataclass(frozen=True)
class KnowledgeChunk:
    chunk_id: str
    title: str
    content: str
    source_url: str
    product: str
    version: str
    dialect: str
    license_class: str
    retrieval_only: bool

    @classmethod
    def from_json(cls, raw: dict) -> "KnowledgeChunk":
        return cls(
            chunk_id=str(raw["chunk_id"]),
            title=str(raw.get("title", "")),
            content=str(raw["content"]),
            source_url=str(raw.get("source_url", "")),
            product=str(raw.get("product", "unknown")),
            version=str(raw.get("version", "unknown")),
            dialect=str(raw.get("dialect", "general")),
            license_class=str(raw.get("license_class", "unknown")),
            retrieval_only=bool(raw.get("retrieval_only", True)),
        )


@dataclass(frozen=True)
class RetrievalResult:
    chunk: KnowledgeChunk
    score: float


def tokenize(text: str) -> list[str]:
    return [match.group(0).lower() for match in TOKEN_RE.finditer(text)]


def _hashed_vector(tokens: Iterable[str]) -> list[float]:
    vector = [0.0] * VECTOR_SIZE
    for token in tokens:
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        index = int.from_bytes(digest[:2], "big") % VECTOR_SIZE
        sign = 1.0 if digest[2] % 2 == 0 else -1.0
        vector[index] += sign
    norm = math.sqrt(sum(value * value for value in vector))
    if norm == 0:
        return vector
    return [value / norm for value in vector]


def _cosine(left: list[float], right: list[float]) -> float:
    return sum(a * b for a, b in zip(left, right))


class KnowledgeBase:
    def __init__(self, chunks: list[KnowledgeChunk]) -> None:
        self._chunks = chunks
        self._token_sets = [set(tokenize(chunk.title + " " + chunk.content)) for chunk in chunks]
        self._vectors = [_hashed_vector(tokens) for tokens in self._token_sets]

    @classmethod
    def load_jsonl(cls, path: Path) -> "KnowledgeBase":
        if not path.exists():
            return cls([])
        chunks: list[KnowledgeChunk] = []
        with path.open("r", encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                if not line.strip():
                    continue
                try:
                    chunks.append(KnowledgeChunk.from_json(json.loads(line)))
                except (KeyError, TypeError, json.JSONDecodeError) as exc:
                    raise ValueError(f"Invalid knowledge JSONL at {path}:{line_number}: {exc}") from exc
        return cls(chunks)

    def search(
        self,
        query: str,
        *,
        limit: int = 4,
        dialect: str | None = None,
        product: str | None = None,
    ) -> list[RetrievalResult]:
        query_tokens = tokenize(query)
        if not query_tokens:
            return []
        query_set = set(query_tokens)
        query_vector = _hashed_vector(query_tokens)
        results: list[RetrievalResult] = []

        for chunk, token_set, vector in zip(self._chunks, self._token_sets, self._vectors):
            if dialect and chunk.dialect not in {dialect, "general"}:
                continue
            if product and chunk.product != product:
                continue
            overlap = len(query_set & token_set) / max(len(query_set), 1)
            semantic = max(_cosine(query_vector, vector), 0.0)
            score = (0.65 * overlap) + (0.35 * semantic)
            if score > 0:
                results.append(RetrievalResult(chunk=chunk, score=score))

        results.sort(key=lambda result: result.score, reverse=True)
        return results[:limit]


def format_context(results: list[RetrievalResult]) -> str:
    if not results:
        return "No retrieved context."
    lines: list[str] = []
    for index, result in enumerate(results, start=1):
        chunk = result.chunk
        lines.append(
            "\n".join(
                [
                    f"[{index}] {chunk.title}",
                    f"Source: {chunk.source_url or 'local'}",
                    f"Product: {chunk.product} {chunk.version}; Dialect: {chunk.dialect}; License: {chunk.license_class}",
                    chunk.content,
                ]
            )
        )
    return "\n\n".join(lines)
