# Google GPU Automation

This project can automate local dataset and eval artifact preparation. Full unattended GPU execution depends on the Google runtime product.

## Current Local Automation

Run this from `E:\projects`:

```powershell
.\scripts\prepare_batch1_training.ps1
```

It creates ignored generated files:

```text
data\generated\sft_train.jsonl
data\generated\golden_prompts_batch1_combined.jsonl
```

Upload those files to Google Drive or a Google Cloud bucket for training/evaluation.

## Colab Pro

Normal Colab Pro is browser/session based. It is suitable for manual or semi-manual training, but an API key alone is not enough to start and supervise an unattended GPU notebook run from this repo.

Use the prepared notebooks:

```text
notebooks/colab_qwen_lora_training.ipynb
notebooks/colab_adapter_eval.ipynb
```

## Colab Enterprise

Google documents Colab Enterprise notebook execution through Vertex AI API resources. That is the supported path for scheduled or API-managed notebook runs.

Useful official docs:

- https://cloud.google.com/colab/docs/introduction
- https://cloud.google.com/colab/docs/reference/rest
- https://cloud.google.com/colab/docs/schedule-notebook-run

An API key should not be committed or pasted into scripts. Use `gcloud auth application-default login`, service-account credentials stored outside git, or a secret manager. Required IAM roles and Cloud Storage bucket setup must be configured in the Google Cloud project before this repo can submit a notebook execution job.

## Project Values

The user-provided Google Cloud project identifier is:

```text
projects/188595204727
```

Do not store raw API keys in this repository.

## Resume Point

When authenticated Google Cloud tooling is available locally, the next automation step is:

1. Upload `data\generated\sft_train.jsonl` and `data\generated\golden_prompts_batch1_combined.jsonl` to a Cloud Storage bucket.
2. Create a Colab Enterprise notebook execution job using the Vertex AI/Colab Enterprise API.
3. Save adapter artifacts to Cloud Storage.
4. Download adapter artifacts into ignored `artifacts\adapters\`.
5. Run adapter evaluation and accept/reject by `docs\dataset_v2_plan.md`.
