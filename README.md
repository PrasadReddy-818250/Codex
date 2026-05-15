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

The web UI includes Start Model / Stop Model controls for the configured local `llama-server` path.

By default, the app expects a local OpenAI-compatible model endpoint at `http://127.0.0.1:8080/v1/chat/completions`.

For UI and wiring tests without a model, set:

```powershell
$env:ASSISTANT_MOCK_MODEL="true"
.\scripts\run_web.ps1
```

For the tested real local 3B model:

```powershell
.\scripts\download_qwen3b_runtime.ps1
.\scripts\start_qwen3b_llama_server.ps1
.\scripts\run_web_real.ps1
```

For a Colab GPU endpoint:

```powershell
.\scripts\run_web_colab_endpoint.ps1 -Endpoint "https://<your-colab-tunnel>/v1/chat/completions" -ModelName "Qwen/Qwen2.5-Coder-3B-Instruct"
```

## Model Runtime

Recommended local runtime: `llama.cpp` `llama-server`.

Current tested model: `Qwen2.5-Coder-3B-Instruct-GGUF` `Q4_K_M`, served by `llama-server` on CPU with a 2048-token context.

Model files and adapters must stay outside git-tracked content. Use `artifacts/models/` and `artifacts/adapters/` locally.

See [docs/local_llm_runtime.md](docs/local_llm_runtime.md) and [docs/colab_gpu_runtime.md](docs/colab_gpu_runtime.md).

## Custom Training

The custom-trained path is LoRA/QLoRA on top of `Qwen/Qwen2.5-Coder-3B-Instruct`, then adapter export from Colab.

Prepare local SFT data:

```powershell
.\scripts\prepare_custom_training_data.ps1
```

Upload `data\generated\sft_train.jsonl` into [notebooks/colab_qwen_lora_training.ipynb](notebooks/colab_qwen_lora_training.ipynb).

The repo includes only seed data and training code. Generated SFT data, adapters, and model weights are ignored.
