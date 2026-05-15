$ErrorActionPreference = "Stop"

$llamaDir = "E:\projects\artifacts\tools\llama.cpp"
$modelDir = "E:\projects\artifacts\models\qwen2.5-coder-1.5b-instruct-q4_k_m"
$llamaZip = Join-Path $llamaDir "llama-b9159-bin-win-cpu-x64.zip"
$llamaExtractDir = Join-Path $llamaDir "b9159-win-cpu-x64"
$modelPath = Join-Path $modelDir "model.gguf"

New-Item -ItemType Directory -Force -Path $llamaDir, $modelDir | Out-Null

if (-not (Test-Path -LiteralPath (Join-Path $llamaExtractDir "llama-server.exe"))) {
    curl.exe -L --fail --retry 3 `
        -o $llamaZip `
        "https://github.com/ggml-org/llama.cpp/releases/download/b9159/llama-b9159-bin-win-cpu-x64.zip"
    Expand-Archive -LiteralPath $llamaZip -DestinationPath $llamaExtractDir -Force
}

if (-not (Test-Path -LiteralPath $modelPath)) {
    curl.exe -L --fail --retry 3 -C - `
        -o $modelPath `
        "https://huggingface.co/Qwen/Qwen2.5-Coder-1.5B-Instruct-GGUF/resolve/main/qwen2.5-coder-1.5b-instruct-q4_k_m.gguf"
}

Write-Host "Runtime ready."
Write-Host "Start model server with: .\scripts\start_qwen15b_llama_server.ps1"
