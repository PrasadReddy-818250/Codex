from assistant.config import AppConfig
from assistant.runtime_manager import RuntimeManager


def test_runtime_status_reports_stopped_on_unused_port(tmp_path) -> None:
    config = AppConfig(
        host="127.0.0.1",
        port=8000,
        model_endpoint="http://127.0.0.1:65534/v1/chat/completions",
        model_name="test",
        rag_path=tmp_path / "missing.jsonl",
        mock_model=True,
        max_retrieved_chunks=4,
        llama_server_path=tmp_path / "llama-server.exe",
        llama_model_path=tmp_path / "model.gguf",
        llama_host="127.0.0.1",
        llama_port=65534,
        llama_context_size=2048,
        llama_threads=4,
    )

    status = RuntimeManager(config).status()
    assert not status.running
    assert status.port == 65534
