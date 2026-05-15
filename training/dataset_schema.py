from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


VALID_RECORD_TYPES = {"instruction_response", "rag_grounded_answer"}


@dataclass(frozen=True)
class TrainingRecord:
    id: str
    record_type: str
    instruction: str
    expected_response: dict[str, Any]
    domain: list[str] = field(default_factory=list)
    license_class: str = "synthetic"

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "TrainingRecord":
        record_type = str(raw.get("record_type", ""))
        if record_type not in VALID_RECORD_TYPES:
            raise ValueError(f"Unsupported record_type: {record_type}")
        return cls(
            id=str(raw["id"]),
            record_type=record_type,
            instruction=str(raw.get("instruction") or raw.get("question") or ""),
            expected_response=dict(raw.get("expected_response") or {}),
            domain=list(raw.get("domain") or []),
            license_class=str(raw.get("license_class", "synthetic")),
        )

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.id:
            errors.append("id is required")
        if not self.instruction:
            errors.append("instruction or question is required")
        if self.license_class.lower() in {"yellow", "red"}:
            errors.append("training records must not use yellow/red retrieval-only source text")
        return errors
