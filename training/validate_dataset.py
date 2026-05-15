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
    if len(sys.argv) != 2:
        print("Usage: python -m training.validate_dataset path/to/data.jsonl")
        return 2
    return 1 if validate_jsonl(Path(sys.argv[1])) else 0


if __name__ == "__main__":
    raise SystemExit(main())
