# Dataset V2 Plan

The first LoRA adapter trained on 6 records is rejected. It proved the Colab and adapter workflow, but it did not produce a usable SQL/Python expert.

The next milestone is a real dataset batch, not another smoke adapter.

## Target

First serious adapter target:

- Training records: 1,200
- Held-out eval prompts: 180
- License classes: `synthetic` or `green` only
- Base model: `Qwen/Qwen2.5-Coder-3B-Instruct`
- Training method: QLoRA in Colab T4 unless a more reliable GPU runner is added

## Record Allocation

| Topic | Train records | Eval prompts |
|---|---:|---:|
| PostgreSQL SQL + SQLAlchemy | 180 | 25 |
| MySQL and MySQL/PostgreSQL translation | 120 | 18 |
| SQLite practical differences | 60 | 10 |
| Db2 LUW | 90 | 15 |
| Db2 for i / AS400 | 130 | 25 |
| Db2 LUW vs Db2 for i distinction | 60 | 10 |
| Python DB-API and SQLAlchemy safety | 120 | 20 |
| pandas / numpy / CSV / Excel | 140 | 20 |
| requests / httpx / API ingestion | 90 | 15 |
| boto3 / fsspec / object storage | 80 | 12 |
| Airflow DAG patterns | 90 | 15 |
| PySpark | 80 | 10 |
| Kafka | 50 | 8 |
| Safety, frankness, no fabricated state | 100 | 20 |

The numbers can shift, but Db2 for i, PostgreSQL, DB-API safety, and pandas/Excel should not be underrepresented.

## Batch Sequence

### Batch 0: Schema Smoke

Goal: 50 records.

Use this to verify validation, SFT conversion, notebook upload, adapter save, and adapter eval. This is not expected to beat the base model.

### Batch 1: Critical Behavior

Goal: 250 records plus 40 eval prompts.

Must cover:

- PostgreSQL SQLAlchemy Core upsert.
- Robust `requests.get` and HTTPX calls with explicit timeouts.
- SQL parameter binding across psycopg, PyMySQL, mysql-connector, pyodbc, sqlite3.
- MySQL `LIMIT offset,count` to PostgreSQL `LIMIT count OFFSET offset`.
- Db2 for i is not Db2 LUW; do not call it mainframe.
- Airflow top-level side effects.
- No fake “tests passed” or “file exists” claims.
- Confirmation before destructive SQL/filesystem actions.

Train after Batch 1 only if the eval file has at least 40 prompts.

### Batch 2: Remediation

Goal: add 150-250 records focused on Batch 1 adapter failures.

Focus:

- Secret refusal and safe secret handling.
- Destructive SQL confirmation, preview, transaction, row-count, backup, and rollback behavior.
- SQL identifier allowlists for dynamic table/column/order choices.
- Kafka committed offset semantics: commit the next offset after successful processing.
- Uncertainty behavior for schema, files, test results, package versions, and execution claims.
- Missing API habits from Batch 1: `raise_for_status()`, `indicator=True`, `_merge`, `URL.create`, `mappings()`, Airflow parse-time and XCom guidance.

Implemented artifacts:

```text
training/generate_batch2_dataset.py
training/batch2_records.jsonl
evals/batch2_golden_prompts.jsonl
scripts/prepare_batch2_training.ps1
```

Generated ignored outputs:

```text
data/generated/sft_train_batch2.jsonl
data/generated/golden_prompts_batch2_combined.jsonl
```

### Batch 3: Python Data Engineering

Goal: add 300 records.

Focus:

- DB drivers and SQLAlchemy.
- pandas/numpy.
- Excel/CSV/file safety.
- requests/httpx.
- boto3/fsspec.
- Airflow.
- PySpark.
- Kafka.

### Batch 4: RAG-Grounded Behavior

Goal: add 200 records.

Use only approved context snippets. Expected answers must obey supplied context, avoid unsupported vendor claims, and cite source URLs when asked.

### Batch 5: Regression and Adversarial

Goal: add 100 records.

Focus:

- Prompt injection in pasted logs.
- Secret dumping requests.
- Malware requests.
- SQL injection fixes.
- Destructive SQL requiring confirmation.
- Fabricated local state.
- Unsupported exact schema claims.

## Quality Gates

Every record must satisfy:

- Stable unique `id`, topic-prefixed.
- `record_type` is `instruction_response` or `rag_grounded_answer`.
- `license_class` is `synthetic` or `green`.
- The answer is the behavior we want the model to imitate.
- Dialect-specific SQL names the dialect.
- Python code uses explicit timeouts for network calls when relevant.
- SQL with user input uses parameters.
- Destructive operations require confirmation or are presented as dry-run/transactional patterns.
- Db2 for i and Db2 LUW are never conflated.
- No credentials, private data, copied vendor prose, fake citations, or fake test claims.

Reject records containing:

- f-string SQL with user data.
- Unbounded `requests.get(...)`.
- `except Exception: pass`.
- Invented imports or APIs.
- Claims like “I ran this” without context proving execution.
- Vendor text copied into training examples.

## Duplicate Controls

Before training:

- Exact duplicate check: normalized `instruction + expected_response.answer`.
- Near-duplicate check: reject examples that only rename tables or variables.
- Eval leakage check: eval prompts must not be direct paraphrases of training prompts with the same required strings.

ID convention:

```text
<domain>-<library-or-dialect>-<behavior>-NNN
postgres-sqlalchemy-upsert-001
python-requests-timeout-001
db2i-luw-distinction-001
airflow-parse-side-effect-001
```

## Eval Design

`evals/golden_prompts.jsonl` should grow from 3 prompts to at least 180 before accepting a real adapter.

Critical eval categories:

- `sql_postgres_correctness`
- `sql_mysql_postgres_translation`
- `sql_db2i_uncertainty`
- `python_requests_httpx`
- `python_dbapi_security`
- `python_airflow`
- `python_pandas_excel`
- `python_pyspark`
- `python_boto3_fsspec`
- `python_kafka`
- `rag_grounded_answer`
- `safety_destructive_sql`
- `no_fabricated_local_state`
- `style_direct_concise`

String checks catch regressions but do not prove correctness. Manual review is still required.

## Acceptance Criteria

Accept a LoRA adapter only if all are true:

- Dataset validation has 0 failures.
- Training/eval leakage check has 0 known leaks.
- Critical evals pass 100%.
- Overall eval pass rate is at least 95%.
- Adapter beats the base model by at least 10 percentage points overall, or fixes documented critical failures without creating new critical failures.
- No forbidden strings appear in critical categories.
- Manual review of at least 30 sampled outputs finds no invented APIs, unsafe SQL, or unsupported vendor claims.
- Adapter behaves acceptably through local `llama-server`, not only inside Colab.
- Adapter manifest records base model, dataset count, license classes, eval summary, and accept/reject decision.

## Next Work Item

Train Batch 2:

1. Run `.\scripts\prepare_batch2_training.ps1`.
2. Upload `data\generated\sft_train_batch2.jsonl` to Colab training.
3. Evaluate with `data\generated\golden_prompts_batch2_combined.jsonl`.
4. Reject the adapter unless all critical safety and correctness evals pass.
