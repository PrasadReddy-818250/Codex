from __future__ import annotations

from dataclasses import dataclass


SYSTEM_POLICY = """You are a local SQL/Python data engineering assistant.
Answer in English only. Be direct, technical, and concise. Avoid corporate filler.
State assumptions clearly when requirements are incomplete.
Prioritize correctness over speed. Do not invent facts, command output, files, test results, package versions, or database behavior.
For vendor-specific claims, use retrieved context when available and cite source URLs.

Hard boundaries:
- Do not help steal credentials, secrets, tokens, private keys, or session cookies.
- Do not provide malware, persistence, evasion, credential theft, or unauthorized access instructions.
- Do not execute or instruct unconfirmed destructive actions against filesystems, databases, or infrastructure.
- For destructive SQL or filesystem actions, explain risk and provide review guidance instead of execution steps unless the user explicitly confirms execution.
"""


BLOCKED_PATTERNS = (
    "dump credentials",
    "steal password",
    "exfiltrate",
    "browser cookies",
    "private key",
    "ransomware",
    "keylogger",
    "bypass authentication",
    "disable audit",
    "cover tracks",
)

DESTRUCTIVE_PATTERNS = (
    "drop database",
    "drop table",
    "truncate table",
    "delete from",
    "remove-item",
    "rm -rf",
    "format c:",
    "wipe",
)


@dataclass(frozen=True)
class SafetyDecision:
    allowed: bool
    reason: str | None = None
    needs_confirmation: bool = False


def assess_user_message(message: str) -> SafetyDecision:
    normalized = " ".join(message.lower().split())
    if any(pattern in normalized for pattern in BLOCKED_PATTERNS):
        return SafetyDecision(
            allowed=False,
            reason="I cannot help with credential theft, malware, evasion, or unauthorized access.",
        )
    if any(pattern in normalized for pattern in DESTRUCTIVE_PATTERNS):
        return SafetyDecision(
            allowed=True,
            reason="This appears destructive. I can explain and help review it, but execution needs explicit confirmation.",
            needs_confirmation=True,
        )
    return SafetyDecision(allowed=True)
