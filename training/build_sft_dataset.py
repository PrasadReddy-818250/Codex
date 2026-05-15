from __future__ import annotations

import json
import sys
from pathlib import Path

from training.dataset_schema import TrainingRecord


def build_sft_jsonl(input_path: Path, output_path: Path) -> int:
    return build_sft_jsonl_many([input_path], output_path)


def build_sft_jsonl_many(input_paths: list[Path], output_path: Path) -> int:
    count = 0
    seen_ids: set[str] = set()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as target:
        for input_path in input_paths:
            with input_path.open("r", encoding="utf-8") as source:
                for line_number, line in enumerate(source, start=1):
                    if not line.strip():
                        continue
                    record = TrainingRecord.from_dict(json.loads(line))
                    errors = record.validate()
                    if errors:
                        joined = "; ".join(errors)
                        raise ValueError(f"{input_path}:{line_number}: {joined}")
                    if record.id in seen_ids:
                        raise ValueError(f"{input_path}:{line_number}: duplicate id: {record.id}")
                    seen_ids.add(record.id)
                    target.write(
                        json.dumps({"id": record.id, "messages": record.to_chat_messages()}, ensure_ascii=False)
                        + "\n"
                    )
                    count += 1
    return count


def main() -> int:
    if len(sys.argv) < 3:
        print("Usage: python -m training.build_sft_dataset input_records.jsonl [more_records.jsonl ...] output_sft.jsonl")
        return 2
    input_paths = [Path(arg) for arg in sys.argv[1:-1]]
    count = build_sft_jsonl_many(input_paths, Path(sys.argv[-1]))
    print(f"wrote {count} records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
