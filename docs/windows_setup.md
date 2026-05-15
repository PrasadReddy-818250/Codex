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
