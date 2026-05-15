# Model Artifacts

Do not commit model weights or adapters.

Recommended first candidates:

- IBM Granite 3B Code/Instruct GGUF Q4 if it meets quality needs and license requirements.
- Qwen2.5-Coder 3B Instruct GGUF Q4 for personal accuracy testing after license review.
- Qwen2.5-Coder 1.5B Instruct GGUF Q4 when RAM or latency is too tight.

For each local model, create a manifest with:

- model name and source URL;
- license;
- quantization;
- checksum;
- context size used;
- eval result summary;
- date tested.
