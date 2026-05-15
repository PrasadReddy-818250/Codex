# Current Model Status

Verified local runtime:

- Runtime: `llama.cpp` `llama-server`
- Runtime build: `b9159` Windows CPU x64
- Model: `Qwen2.5-Coder-3B-Instruct-GGUF`
- Quantization: `Q4_K_M`
- Local path: `artifacts/models/qwen2.5-coder-3b-instruct-q4_k_m/model.gguf`
- Endpoint: `http://127.0.0.1:8080/v1/chat/completions`
- App mode: real model mode, not mock mode

Observed smoke results:

- Direct model endpoint responded to `Say ready.`
- App `/health` returned `mock_model=false`.
- App generated a PostgreSQL SQLAlchemy upsert answer using `from sqlalchemy.dialects.postgresql import insert` and `on_conflict_do_update`.
- App generated a `requests.get(..., timeout=...)` answer.

Known limitation:

- This is still a small local model. It can make code mistakes and must be evaluated before being trusted for production SQL/Python work.
- Custom training is prepared through `training/seed_records.jsonl`, `training/build_sft_dataset.py`, and `notebooks/colab_qwen_lora_training.ipynb`, but no trained adapter has been produced yet.
