# Notebooks

Place Colab notebooks here.

Use `colab_qwen_lora_training.ipynb` for the first custom-training run. It expects chat-format JSONL produced by:

```powershell
.\.venv\Scripts\python.exe -m training.build_sft_dataset training\seed_records.jsonl data\generated\sft_train.jsonl
```

Generated notebook outputs and model artifacts should not be committed.
