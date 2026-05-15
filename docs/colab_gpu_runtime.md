# Google Colab GPU Runtime

Colab can run the model on GPU and expose an OpenAI-compatible HTTP endpoint to the local Windows app.

This is not offline local inference. Prompts and retrieved context are sent from your local app to the Colab runtime endpoint.

## Recommended Use

Use Colab GPU for:

- testing larger models than the 8 GB Windows system can run;
- LoRA/QLoRA experiments;
- temporary higher-quality inference while local CPU setup is limited.

Use local CPU for:

- offline private runtime;
- predictable availability;
- no dependency on Colab session lifetime.

## Colab Server Pattern

In Colab, run an OpenAI-compatible server. A practical option is vLLM when the selected model fits the available GPU.

Example Colab cells:

```python
!pip install -U vllm pyngrok
```

```python
from pyngrok import ngrok

public_url = ngrok.connect(8000, "http")
print(public_url)
```

```python
!python -m vllm.entrypoints.openai.api_server \
  --host 0.0.0.0 \
  --port 8000 \
  --model Qwen/Qwen2.5-Coder-3B-Instruct \
  --dtype half \
  --max-model-len 4096
```

The printed ngrok URL becomes your endpoint:

```text
https://<your-ngrok-host>/v1/chat/completions
```

Then start the local Windows app:

```powershell
.\scripts\run_web_colab_endpoint.ps1 -Endpoint "https://<your-ngrok-host>/v1/chat/completions" -ModelName "Qwen/Qwen2.5-Coder-3B-Instruct"
```

## Security Notes

- Colab is remote runtime, not local-only.
- Do not send private credentials, production secrets, or customer data to Colab.
- Free/pro GPU availability changes by session.
- ngrok URLs are temporary unless your account config says otherwise.
