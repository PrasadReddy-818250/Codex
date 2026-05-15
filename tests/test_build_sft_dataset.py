import json
from pathlib import Path

from training.build_sft_dataset import build_sft_jsonl


def test_build_sft_dataset(tmp_path: Path) -> None:
    source = tmp_path / "records.jsonl"
    output = tmp_path / "sft.jsonl"
    source.write_text(
        json.dumps(
            {
                "id": "x",
                "record_type": "instruction_response",
                "instruction": "Say hi",
                "expected_response": {"answer": "Hi"},
                "license_class": "synthetic",
            }
        )
        + "\n",
        encoding="utf-8",
    )

    assert build_sft_jsonl(source, output) == 1
    row = json.loads(output.read_text(encoding="utf-8"))
    assert row["id"] == "x"
    assert [message["role"] for message in row["messages"]] == ["system", "user", "assistant"]
    assert row["messages"][2]["content"] == "Hi"
