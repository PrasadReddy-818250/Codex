$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")
Set-Location $repoRoot

.\.venv\Scripts\python.exe -m training.generate_batch1_dataset
.\.venv\Scripts\python.exe -m training.validate_dataset training\seed_records.jsonl training\batch1_records.jsonl
.\.venv\Scripts\python.exe -m training.build_sft_dataset training\seed_records.jsonl training\batch1_records.jsonl data\generated\sft_train.jsonl

$combinedEval = "data\generated\golden_prompts_batch1_combined.jsonl"
$combinedEvalPath = Join-Path $repoRoot $combinedEval
$combinedEvalLines = Get-Content -LiteralPath "evals\golden_prompts.jsonl", "evals\batch1_golden_prompts.jsonl"
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllLines($combinedEvalPath, $combinedEvalLines, $utf8NoBom)

Write-Host "Prepared training file: data\generated\sft_train.jsonl"
Write-Host "Prepared eval file: $combinedEval"
