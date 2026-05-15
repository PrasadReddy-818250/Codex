from pathlib import Path

from assistant.rag import KnowledgeBase


def test_loads_sample_knowledge_and_retrieves_postgres() -> None:
    kb = KnowledgeBase.load_jsonl(Path("data/samples/knowledge.jsonl"))
    results = kb.search("PostgreSQL SQLAlchemy upsert on conflict", limit=2)
    assert results
    assert results[0].chunk.dialect == "postgresql"


def test_missing_knowledge_file_is_empty() -> None:
    kb = KnowledgeBase.load_jsonl(Path("does-not-exist.jsonl"))
    assert kb.search("anything") == []
