$ErrorActionPreference = "Stop"

$inputPath = "training\seed_records.jsonl"
$outputPath = "data\generated\sft_train.jsonl"

if (-not (Test-Path -LiteralPath ".venv\Scripts\python.exe")) {
    throw "Virtual environment not found. Run .\scripts\setup_windows.ps1 first."
}

.\.venv\Scripts\python.exe -m training.validate_dataset $inputPath
.\.venv\Scripts\python.exe -m training.build_sft_dataset $inputPath $outputPath

Write-Host "Custom training data ready: $outputPath"
Write-Host "Upload this JSONL file in notebooks/colab_qwen_lora_training.ipynb"
