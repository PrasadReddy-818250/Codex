# Local LLM Runtime

The web app is not the model. It talks to a local OpenAI-compatible endpoint.

For an 8 GB Windows CPU-only system, use a small quantized GGUF model through `llama.cpp`.

Recommended shape:

- Runtime: `llama-server`
- Model size: 1.5B to 4B
- Quantization: Q4_K_M or Q5_K_M
- Context: 2048 to 4096 tokens
- Endpoint: `http://127.0.0.1:8080/v1/chat/completions`

## Steps

1. Download or build `llama.cpp` for Windows.
2. Download a GGUF model into:

```text
E:\projects\artifacts\models\local-code-model\model.gguf
```

3. Start the model server:

```powershell
.\scripts\start_llama_server.example.ps1
```

4. Start the app in real-model mode:

```powershell
.\scripts\run_web_real.ps1
```

## Working 3B Local Model Path

This is the current default local model path:

```powershell
.\scripts\download_qwen3b_runtime.ps1
.\scripts\start_qwen3b_llama_server.ps1
.\scripts\run_web_real.ps1
```

The downloaded files are stored under ignored `artifacts/` paths:

```text
artifacts/tools/llama.cpp/b9159-win-cpu-x64/llama-server.exe
artifacts/models/qwen2.5-coder-3b-instruct-q4_k_m/model.gguf
```

The model endpoint is:

```text
http://127.0.0.1:8080/v1/chat/completions
```

The browser UI also has Start Model and Stop Model buttons. They manage the configured local `llama-server.exe` and model path only.

## Lower-RAM 1.5B Fallback

If the 3B model is too slow or memory pressure is too high, use:

```powershell
.\scripts\download_qwen15b_runtime.ps1
.\scripts\start_qwen15b_llama_server.ps1
.\scripts\run_web_real.ps1
```

The downloaded files are stored under ignored `artifacts/` paths:

```text
artifacts/tools/llama.cpp/b9159-win-cpu-x64/llama-server.exe
artifacts/models/qwen2.5-coder-1.5b-instruct-q4_k_m/model.gguf
```

5. Open:

```text
http://127.0.0.1:8000
```

## Model Candidates

Use license-reviewed GGUF releases only.

- IBM Granite Code/Instruct 3B class: safer first commercial candidate if quality is acceptable.
- Qwen2.5-Coder 1.5B/3B Instruct: strong personal-use accuracy candidate after license review.

Do not use 7B/8B as the default on 8 GB RAM. It may load in some cases, but Windows, browser, Python, retrieval, and KV cache leave little headroom.
