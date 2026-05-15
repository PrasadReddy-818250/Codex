from __future__ import annotations

import json
import sys
from pathlib import Path

from training.dataset_schema import TrainingRecord


def validate_jsonl(path: Path) -> int:
    failures = 0
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                record = TrainingRecord.from_dict(json.loads(line))
                errors = record.validate()
            except Exception as exc:
                errors = [str(exc)]
            for error in errors:
                failures += 1
                print(f"{path}:{line_number}: {error}")
    return failures


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python -m training.validate_dataset path/to/data.jsonl [more_data.jsonl ...]")
        return 2
    failures = 0
    seen_ids: dict[str, str] = {}
    for arg in sys.argv[1:]:
        path = Path(arg)
        failures += validate_jsonl(path)
        with path.open("r", encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                if not line.strip():
                    continue
                try:
                    item_id = str(json.loads(line)["id"])
                except Exception:
                    continue
                location = f"{path}:{line_number}"
                if item_id in seen_ids:
                    failures += 1
                    print(f"{location}: duplicate id also seen at {seen_ids[item_id]}: {item_id}")
                else:
                    seen_ids[item_id] = location
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
