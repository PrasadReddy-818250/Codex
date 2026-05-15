$ErrorActionPreference = "Stop"

$serverPath = "E:\projects\artifacts\tools\llama.cpp\b9159-win-cpu-x64\llama-server.exe"
$modelPath = "E:\projects\artifacts\models\qwen2.5-coder-1.5b-instruct-q4_k_m\model.gguf"

if (-not (Test-Path -LiteralPath $serverPath)) {
    throw "llama-server.exe not found: $serverPath"
}

if (-not (Test-Path -LiteralPath $modelPath)) {
    throw "Model file not found: $modelPath"
}

& $serverPath `
    -m $modelPath `
    --host 127.0.0.1 `
    --port 8080 `
    -c 2048 `
    -t 4
