# Architecture

The assistant has four local layers:

1. Web UI: FastAPI serves a small browser chat page and `/api/chat`.
2. Core assistant: safety assessment, prompt policy, RAG context assembly, model call.
3. Retrieval: local JSONL chunks searched by lexical overlap and hashed vector scoring.
4. Model runtime: `llama.cpp` `llama-server` on `127.0.0.1`.

Runtime inference is local. Google Colab is only for optional adapter training and export.

The app does not execute SQL, Python, shell commands, or database mutations. It generates reviewable text responses.
