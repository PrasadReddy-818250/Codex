$ErrorActionPreference = "Stop"

if (-not (Test-Path -LiteralPath ".venv\Scripts\python.exe")) {
    py -3.11 -m pytest
} else {
    .\.venv\Scripts\python.exe -m pytest
}
