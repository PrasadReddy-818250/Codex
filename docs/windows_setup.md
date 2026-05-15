# Windows Setup

1. Install Python 3.11 or newer.
2. Install `llama.cpp` Windows binaries or build it separately.
3. Download a compatible GGUF model into `artifacts/models/<name>/model.gguf`.
4. Start the model endpoint:

```powershell
.\scripts\start_llama_server.example.ps1
```

5. In a second terminal, start the web app:

```powershell
.\scripts\setup_windows.ps1
.\scripts\run_web.ps1
```

For wiring tests without a model:

```powershell
.\scripts\run_web_mock.ps1
```

For real local inference, start `llama-server` first and then run:

```powershell
.\scripts\run_web_real.ps1
```

For a temporary Colab GPU-backed model, expose an OpenAI-compatible endpoint from Colab and run:

```powershell
.\scripts\run_web_colab_endpoint.ps1 -Endpoint "https://<your-colab-tunnel>/v1/chat/completions"
```
