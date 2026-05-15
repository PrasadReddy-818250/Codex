# Colab Training Plan

Training is optional and must be measured against the RAG-only baseline.

Workflow:

1. Prepare JSONL records with `training/dataset_schema.py`.
2. Validate records before upload.
3. Fine-tune with LoRA or QLoRA in Google Colab T4.
4. Export adapter files and a manifest.
5. Optionally merge and convert to GGUF for local CPU inference.
6. Run evals before accepting the adapter.

Do not train on private data, credentials, proprietary vendor manuals, or customer code unless explicitly approved.
