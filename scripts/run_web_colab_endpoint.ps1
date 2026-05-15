$ErrorActionPreference = "Stop"

param(
    [Parameter(Mandatory = $true)]
    [string]$Endpoint,

    [string]$ModelName = "colab-code-model"
)

if (-not (Test-Path -LiteralPath ".venv\Scripts\python.exe")) {
    throw "Virtual environment not found. Run .\scripts\setup_windows.ps1 first."
}

$env:ASSISTANT_MOCK_MODEL = "false"
$env:ASSISTANT_MODEL_ENDPOINT = $Endpoint
$env:ASSISTANT_MODEL_NAME = $ModelName

.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
