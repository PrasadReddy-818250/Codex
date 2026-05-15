from training.dataset_schema import TrainingRecord


def test_training_record_rejects_yellow_source_text() -> None:
    record = TrainingRecord.from_dict(
        {
            "id": "x",
            "record_type": "instruction_response",
            "instruction": "answer",
            "expected_response": {"answer": "text"},
            "license_class": "yellow",
        }
    )
    assert record.validate()


def test_training_record_accepts_synthetic() -> None:
    record = TrainingRecord.from_dict(
        {
            "id": "x",
            "record_type": "instruction_response",
            "instruction": "answer",
            "expected_response": {"answer": "text"},
            "license_class": "synthetic",
        }
    )
    assert record.validate() == []


def test_training_record_exports_chat_messages() -> None:
    record = TrainingRecord.from_dict(
        {
            "id": "x",
            "record_type": "instruction_response",
            "instruction": "Say hi",
            "expected_response": {"answer": "Hi"},
            "license_class": "synthetic",
        }
    )
    messages = record.to_chat_messages()
    assert messages[0]["role"] == "system"
    assert messages[1] == {"role": "user", "content": "Say hi"}
    assert messages[2] == {"role": "assistant", "content": "Hi"}
