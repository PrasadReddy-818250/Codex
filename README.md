# Local Frank SQL/Python GPT

Local Windows-first assistant for SQL and Python data engineering work. The runtime target is an 8 GB RAM CPU-only machine with local inference through `llama.cpp` `llama-server`.

This project is intentionally RAG-first. Fine-tuning is a later measured improvement path, not the first source of correctness.

## V1 Goals

- Local web UI.
- Local `llama-server` backend on `127.0.0.1`.
- Direct, technical assistant behavior with narrow hard safety boundaries.
- Hybrid local retrieval over approved JSONL knowledge chunks.
- Evaluation hooks for SQL, Python, frankness, safety, and local performance.

## Quick Start

```powershell
.\scripts\setup_windows.ps1
.\scripts\run_web.ps1
```

Open `http://127.0.0.1:8000`.

By default, the app expects a local OpenAI-compatible model endpoint at `http://127.0.0.1:8080/v1/chat/completions`. For UI and wiring tests without a model, set:

```powershell
$env:ASSISTANT_MOCK_MODEL="true"
.\scripts\run_web.ps1
```

## Model Runtime

Recommended local runtime: `llama.cpp` `llama-server`.

Recommended first model class: 3B to 4B GGUF Q4 with context capped at 2048 to 4096 tokens.

Model files and adapters must stay outside git-tracked content. Use `artifacts/models/` and `artifacts/adapters/` locally.
