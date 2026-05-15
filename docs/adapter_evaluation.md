# Adapter Evaluation

The first custom adapter is available locally but is not yet merged into the CPU GGUF runtime.

Local artifact metadata:

- Zip: `E:\projects\artifacts\adapters\qwen25-coder-3b-sql-python-lora.zip`
- Extracted adapter: `E:\projects\artifacts\adapters\qwen25-coder-3b-sql-python-lora`
- SHA-256: `266A1E5F387EA0942E272531E08B1AAD831F57C3AE8F66D55AE3C7D181345841`
- Base model: `Qwen/Qwen2.5-Coder-3B-Instruct`
- Training method: QLoRA
- Seed records: 6

Evaluate before accepting it:

1. Run the local base-model app eval:

```powershell
.\.venv\Scripts\python.exe -m evals.run_app_eval
```

2. Load base model plus adapter in Colab or a GPU-capable Python environment.
3. Run prompts from `evals/golden_prompts.jsonl`.
4. Compare output against `data/generated/app_eval_results.json`.
5. Accept only if the adapter improves target SQL/Python behavior without increasing unsafe or fabricated answers.

Colab helper notebook:

```text
notebooks/colab_adapter_eval.ipynb
```

The notebook reads these Google Drive paths directly:

```text
My Drive/colab Notebooks/codex-artifacts/adapters/qwen25-coder-3b-sql-python-lora.zip
My Drive/colab Notebooks/codex-artifacts/evals/golden_prompts.jsonl
```

If Colab fails with `module 'sympy' has no attribute 'core'`, delete the runtime and rerun the notebook from the top. The notebook force-reinstalls a stable `sympy` before importing Torch/Transformers.

Current base-model baseline:

```text
3/3 passed through the local app after setting max output to 256 tokens.
```

Minimum prompts:

- PostgreSQL SQLAlchemy Core upsert.
- Robust `requests.get` with timeout and `raise_for_status()`.
- MySQL `LIMIT offset,count` to PostgreSQL `LIMIT count OFFSET offset`.
- Db2 for i vs Db2 LUW distinction.
- Unsafe f-string SQL parameterization fix.

Do not treat this 6-record adapter as final. It is a smoke adapter proving the training pipeline works.
