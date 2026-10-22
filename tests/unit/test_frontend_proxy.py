"""Check local routing and preserve real A2A tool results."""

import importlib
import sys
from pathlib import Path
from unittest.mock import AsyncMock, Mock

import google.auth
import pytest
from a2a.types import (
    Artifact,
    DataPart,
    Message,
    Part,
    Role,
    Task,
    TaskState,
    TaskStatus,
    TextPart,
)
from fastapi.testclient import TestClient


@pytest.fixture
def proxy(monkeypatch):
    monkeypatch.delenv("AGENT_ENGINE_RESOURCE_NAME", raising=False)
    monkeypatch.chdir(Path(__file__).resolve().parents[2] / "frontend")
    monkeypatch.setattr(google.auth, "default", Mock(side_effect=AssertionError("Local mode must not load ADC")))
    sys.modules.pop("frontend.main", None)
    return importlib.import_module("frontend.main")


def test_local_mode_needs_no_cloud_credentials(proxy):
    assert proxy.A2A_BASE == "http://localhost:8000/a2a/app"
    assert proxy._auth_headers() == {}


def test_deployed_mode_keeps_adc_auth(proxy, monkeypatch):
    resource = "projects/example/locations/us-east1/reasoningEngines/123"
    creds = Mock(token="test-token")
    monkeypatch.setenv("AGENT_ENGINE_RESOURCE_NAME", resource)
    monkeypatch.setattr(google.auth, "default", Mock(return_value=(creds, None)))
    importlib.reload(proxy)
    assert proxy.A2A_BASE.endswith(f"{resource}/api/a2a/app")
    assert proxy._auth_headers()["Authorization"] == "Bearer test-token"
    creds.refresh.assert_called_once()


def test_extract_parts_keeps_tool_results_and_existing_ui(proxy):
    result = {"name": "roll_dice", "response": {"dice": "1d20", "rolls": [17], "modifier": 3, "total": 20}}
    surface = {"beginRendering": {"surfaceId": "party", "root": "card"}}
    parts = [
        Part(root=TextPart(text="Initiative")),
        Part(root=DataPart(data=result, metadata={"adk_type": "function_response"})),
        Part(root=DataPart(data=surface, metadata={"mimeType": "application/json+a2ui"})),
        Part(root=DataPart(data={"name": "roll_dice"}, metadata={"adk_type": "function_call"})),
    ]
    assert proxy._extract_parts(parts) == [
        {"kind": "text", "text": "Initiative"},
        {"kind": "tool", "name": "roll_dice", "data": result["response"]},
        {"kind": "a2ui", "data": surface},
    ]


def test_direct_agent_message_reaches_the_browser(proxy, monkeypatch):
    reply = Message(message_id="reply", role=Role.agent, context_id="chapter-one", parts=[Part(root=TextPart(text="Ready"))])

    async def send_message(message):
        yield reply

    client = Mock(send_message=send_message)
    monkeypatch.setattr(proxy, "_get_card", AsyncMock())
    monkeypatch.setattr(proxy, "ClientFactory", Mock(return_value=Mock(create=Mock(return_value=client))))
    response = TestClient(proxy.app).post("/chat", json={"message": "Hello", "user_id": "test-reader"})
    assert response.json() == {"parts": [{"kind": "text", "text": "Ready"}]}
    assert proxy._contexts["test-reader"] == "chapter-one"


def test_tool_results_do_not_hide_a_failed_turn(proxy, monkeypatch):
    failure = Message(message_id="failure", role=Role.agent, parts=[Part(root=TextPart(text="Sandbox unavailable"))])
    task = Task(
        id="task", context_id="chapter", status=TaskStatus(state=TaskState.failed, message=failure),
        artifacts=[Artifact(artifact_id="tool", parts=[Part(root=DataPart(
            data={"name": "list_heroes", "response": {"result": []}}, metadata={"adk_type": "function_response"},
        ))])],
    )

    async def send_message(message):
        yield task, None

    monkeypatch.setattr(proxy, "_get_card", AsyncMock())
    monkeypatch.setattr(proxy, "ClientFactory", Mock(return_value=Mock(create=Mock(return_value=Mock(send_message=send_message)))))
    response = TestClient(proxy.app).post("/chat", json={"message": "Run a simulation"})
    assert response.json()["parts"] == [
        {"kind": "tool", "name": "list_heroes", "data": {"result": []}},
        {"kind": "text", "text": "Sandbox unavailable"},
    ]
