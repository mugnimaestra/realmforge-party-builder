"""Keep the regional Memory Bank separate from the global model endpoint."""

from unittest.mock import Mock

from google.adk import memory

from app.app_utils import services


def test_memory_bank_uses_its_region(monkeypatch):
    monkeypatch.setenv("GOOGLE_CLOUD_LOCATION", "global")
    monkeypatch.delenv("GOOGLE_CLOUD_AGENT_ENGINE_LOCATION", raising=False)
    factory = Mock()
    monkeypatch.setattr(memory, "VertexAiMemoryBankService", factory)
    services.get_memory_service.cache_clear()
    try:
        services.get_memory_service()
        assert factory.call_args.kwargs["location"] == "us-east1"
    finally:
        services.get_memory_service.cache_clear()
