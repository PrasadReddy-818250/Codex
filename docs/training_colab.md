# Colab Custom Training Plan

The local app can already run a base Qwen coder GGUF model. Custom training means producing a LoRA adapter from curated examples, then either testing it in Colab or merging/converting it to GGUF for local `llama-server`.

Workflow:

1. Curate records in `training/seed_records.jsonl`, `training/batch1_records.jsonl`, or a larger private JSONL file.
2. Validate records:

```powershell
.\.venv\Scripts\python.exe -m training.validate_dataset training\seed_records.jsonl training\batch1_records.jsonl
```

3. Build chat-format SFT data:

```powershell
.\.venv\Scripts\python.exe -m training.build_sft_dataset training\seed_records.jsonl training\batch1_records.jsonl data\generated\sft_train.jsonl
```

Or prepare Batch 1 artifacts in one command:

```powershell
.\scripts\prepare_batch1_training.ps1
```

For the remediation dataset after the rejected Batch 1 adapter, prepare Batch 2 artifacts:

```powershell
.\scripts\prepare_batch2_training.ps1
```

4. Upload the SFT JSONL and combined eval JSONL to Colab. For Batch 2, use:

```text
data\generated\sft_train_batch2.jsonl
data\generated\golden_prompts_batch2_combined.jsonl
```
5. Run `notebooks/colab_qwen_lora_training.ipynb`.
6. Save adapter artifacts and manifest.
7. Evaluate the adapter against the matching combined eval file from `data\generated`.
8. Merge and convert to GGUF only if evals improve over the base model.

Do not train on private data, credentials, proprietary vendor manuals, or customer code unless explicitly approved.

## Training Target

Start with:

```text
Qwen/Qwen2.5-Coder-3B-Instruct
```

Use 4-bit QLoRA on Colab T4. Keep context length at 1024 or 2048 for the first run.

On T4, load the model with `torch_dtype=torch.float16`, but disable Trainer mixed precision with `fp16=False` and `bf16=False`. This avoids the AMP grad-scaler path that can fail with `NotImplementedError ... BFloat16`. If PEFT warns that an adapter was applied twice, delete the runtime and rerun from a clean session.

If Colab fails with `module 'sympy' has no attribute 'core'`, delete the runtime and rerun from the top. The notebook force-reinstalls a stable `sympy` before importing Torch/Transformers.

## TRL Version Note

Recent TRL versions use `SFTConfig(max_length=...)`; older versions used `max_seq_length`. The notebook detects the installed `SFTConfig` and `SFTTrainer` signatures and maps arguments accordingly. If Colab errors on a TRL argument, restart the runtime and rerun the notebook after pulling the latest repo version.

## Output Artifacts

The notebook should produce:

```text
adapter_config.json
adapter_model.safetensors
training_manifest.json
```

Model weights and adapters must stay out of git. Store local copies under ignored `artifacts/adapters/`.
