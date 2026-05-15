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

1. Load base model plus adapter in Colab or a GPU-capable Python environment.
2. Run prompts from `evals/golden_prompts.jsonl`.
3. Compare output against the current local base model behavior.
4. Accept only if the adapter improves target SQL/Python behavior without increasing unsafe or fabricated answers.

Minimum prompts:

- PostgreSQL SQLAlchemy Core upsert.
- Robust `requests.get` with timeout and `raise_for_status()`.
- MySQL `LIMIT offset,count` to PostgreSQL `LIMIT count OFFSET offset`.
- Db2 for i vs Db2 LUW distinction.
- Unsafe f-string SQL parameterization fix.

Do not treat this 6-record adapter as final. It is a smoke adapter proving the training pipeline works.
