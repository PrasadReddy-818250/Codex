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
