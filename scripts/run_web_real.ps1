$ErrorActionPreference = "Stop"

if (-not (Test-Path -LiteralPath ".venv\Scripts\python.exe")) {
    throw "Virtual environment not found. Run .\scripts\setup_windows.ps1 first."
}

$env:ASSISTANT_MOCK_MODEL = "false"

if (-not $env:ASSISTANT_MODEL_ENDPOINT) {
    $env:ASSISTANT_MODEL_ENDPOINT = "http://127.0.0.1:8080/v1/chat/completions"
}

.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
