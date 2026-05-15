from __future__ import annotations

import argparse
import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import httpx


@dataclass(frozen=True)
class EvalCase:
    id: str
    prompt: str
    required: list[str]
    forbidden: list[str]

    @classmethod
    def from_json(cls, raw: dict[str, Any]) -> "EvalCase":
        return cls(
            id=str(raw["id"]),
            prompt=str(raw["prompt"]),
            required=[str(item) for item in raw.get("required", [])],
            forbidden=[str(item) for item in raw.get("forbidden", [])],
        )


def load_cases(path: Path) -> list[EvalCase]:
    cases: list[EvalCase] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                cases.append(EvalCase.from_json(json.loads(line)))
    return cases


def check_case(case: EvalCase, answer: str) -> dict[str, Any]:
    normalized = answer.lower()
    missing = [item for item in case.required if item.lower() not in normalized]
    present_forbidden = [item for item in case.forbidden if item.lower() in normalized]
    return {
        "id": case.id,
        "passed": not missing and not present_forbidden,
        "missing_required": missing,
        "present_forbidden": present_forbidden,
        "answer": answer,
    }


def run_eval(endpoint: str, cases: list[EvalCase], timeout: float) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    with httpx.Client(timeout=timeout) as client:
        for case in cases:
            started = time.perf_counter()
            elapsed = time.perf_counter() - started
            try:
                response = client.post(
                    endpoint,
                    json={"message": case.prompt, "history": []},
                )
                elapsed = time.perf_counter() - started
                response.raise_for_status()
                payload = response.json()
                result = check_case(case, str(payload.get("answer", "")))
                result["elapsed_seconds"] = round(elapsed, 3)
                result["citations"] = payload.get("citations", [])
            except Exception as exc:
                elapsed = time.perf_counter() - started
                result = {
                    "id": case.id,
                    "passed": False,
                    "missing_required": case.required,
                    "present_forbidden": [],
                    "answer": "",
                    "elapsed_seconds": round(elapsed, 3),
                    "citations": [],
                    "error": str(exc),
                }
            results.append(result)
            print(f"{case.id}: {'PASS' if result['passed'] else 'FAIL'} ({elapsed:.1f}s)")
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Run local app evals.")
    parser.add_argument("--cases", default="evals/golden_prompts.jsonl")
    parser.add_argument("--endpoint", default="http://127.0.0.1:8000/api/chat")
    parser.add_argument("--output", default="data/generated/app_eval_results.json")
    parser.add_argument("--timeout", type=float, default=240.0)
    args = parser.parse_args()

    cases = load_cases(Path(args.cases))
    results = run_eval(args.endpoint, cases, args.timeout)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    passed = sum(1 for result in results if result["passed"])
    print(f"passed {passed}/{len(results)}")
    print(f"wrote {output_path}")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
