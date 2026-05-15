$ErrorActionPreference = "Stop"

# Update this path after downloading a GGUF model.
$modelPath = "E:\projects\artifacts\models\local-code-model\model.gguf"

if (-not (Test-Path -LiteralPath $modelPath)) {
    throw "Model file not found: $modelPath"
}

llama-server -m $modelPath --host 127.0.0.1 --port 8080 -c 4096
