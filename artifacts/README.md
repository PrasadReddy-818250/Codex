# Artifact Directory

This directory documents local artifact layout. Actual model files are ignored by git.

Expected local layout:

```text
artifacts/
  models/
    model-name/
      model.gguf
      manifest.json
  adapters/
    experiment-name/
      adapter_config.json
      adapter_model.safetensors
      manifest.json
```

Each manifest should include base model, source URL, license, checksum, quantization, context limit, and test result summary.
