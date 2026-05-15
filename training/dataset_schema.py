from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


VALID_RECORD_TYPES = {"instruction_response", "rag_grounded_answer"}
ALLOWED_LICENSE_CLASSES = {"synthetic", "green"}


DEFAULT_SYSTEM_PROMPT = (
    "You are a direct SQL/Python data engineering assistant. "
    "Answer in English. Be concise, correct, and explicit about assumptions. "
    "Prefer safe, parameterized SQL and runnable Python. "
    "Do not invent APIs, imports, files, test results, or database behavior."
)


@dataclass(frozen=True)
class TrainingRecord:
    id: str
    record_type: str
    instruction: str
    expected_response: dict[str, Any] | str
    domain: list[str] = field(default_factory=list)
    license_class: str = "synthetic"
    input_context: dict[str, Any] = field(default_factory=dict)
    system_prompt: str = DEFAULT_SYSTEM_PROMPT

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "TrainingRecord":
        record_type = str(raw.get("record_type", ""))
        if record_type not in VALID_RECORD_TYPES:
            raise ValueError(f"Unsupported record_type: {record_type}")
        return cls(
            id=str(raw["id"]),
            record_type=record_type,
            instruction=str(raw.get("instruction") or raw.get("question") or ""),
            expected_response=raw.get("expected_response") or "",
            domain=list(raw.get("domain") or []),
            license_class=str(raw.get("license_class", "synthetic")),
            input_context=dict(raw.get("input_context") or {}),
            system_prompt=str(raw.get("system_prompt") or DEFAULT_SYSTEM_PROMPT),
        )

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.id:
            errors.append("id is required")
        if not self.instruction:
            errors.append("instruction or question is required")
        if not self.expected_answer_text():
            errors.append("expected_response.answer or expected_response string is required")
        if self.license_class.lower() in {"yellow", "red"}:
            errors.append("training records must not use yellow/red retrieval-only source text")
        if self.license_class.lower() not in ALLOWED_LICENSE_CLASSES:
            errors.append(f"unsupported license_class for training: {self.license_class}")
        return errors

    def expected_answer_text(self) -> str:
        if isinstance(self.expected_response, str):
            return self.expected_response.strip()
        answer = self.expected_response.get("answer")
        if isinstance(answer, str):
            return answer.strip()
        code = self.expected_response.get("code")
        if isinstance(code, str):
            return code.strip()
        return ""

    def user_content(self) -> str:
        if not self.input_context:
            return self.instruction
        return f"{self.instruction}\n\nContext:\n{self.input_context}"

    def to_chat_messages(self) -> list[dict[str, str]]:
        return [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": self.user_content()},
            {"role": "assistant", "content": self.expected_answer_text()},
        ]
