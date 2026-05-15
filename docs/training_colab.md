# Colab Custom Training Plan

The local app can already run a base Qwen coder GGUF model. Custom training means producing a LoRA adapter from curated examples, then either testing it in Colab or merging/converting it to GGUF for local `llama-server`.

Workflow:

1. Curate records in `training/seed_records.jsonl` or a larger private JSONL file.
2. Validate records:

```powershell
.\.venv\Scripts\python.exe -m training.validate_dataset training\seed_records.jsonl
```

3. Build chat-format SFT data:

```powershell
.\.venv\Scripts\python.exe -m training.build_sft_dataset training\seed_records.jsonl data\generated\sft_train.jsonl
```

4. Upload the SFT JSONL to Colab.
5. Run `notebooks/colab_qwen_lora_training.ipynb`.
6. Save adapter artifacts and manifest.
7. Evaluate the adapter against `evals/golden_prompts.jsonl`.
8. Merge and convert to GGUF only if evals improve over the base model.

Do not train on private data, credentials, proprietary vendor manuals, or customer code unless explicitly approved.

## Training Target

Start with:

```text
Qwen/Qwen2.5-Coder-3B-Instruct
```

Use 4-bit QLoRA on Colab T4. Keep context length at 1024 or 2048 for the first run.

## Output Artifacts

The notebook should produce:

```text
adapter_config.json
adapter_model.safetensors
training_manifest.json
```

Model weights and adapters must stay out of git. Store local copies under ignored `artifacts/adapters/`.
