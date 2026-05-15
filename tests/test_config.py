from assistant.config import AppConfig


def test_config_defaults(monkeypatch) -> None:
    for key in [
        "ASSISTANT_HOST",
        "ASSISTANT_PORT",
        "ASSISTANT_MODEL_ENDPOINT",
        "ASSISTANT_MODEL_NAME",
        "ASSISTANT_RAG_PATH",
        "ASSISTANT_MOCK_MODEL",
        "ASSISTANT_MAX_RETRIEVED_CHUNKS",
    ]:
        monkeypatch.delenv(key, raising=False)

    config = AppConfig.from_env()
    assert config.host == "127.0.0.1"
    assert config.port == 8000
    assert not config.mock_model
    assert config.model_timeout_seconds == 300
    assert config.model_max_tokens == 256
    assert config.llama_port == 8080
    assert config.llama_context_size == 2048
