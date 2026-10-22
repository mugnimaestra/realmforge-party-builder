"""Anonymous A2A contexts must not depend on cross-session Memory Bank."""

from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from google.adk.tools.preload_memory_tool import PreloadMemoryTool

from app import agent


@pytest.mark.asyncio
@pytest.mark.parametrize("user_id,expected", [("A2A_USER_chapter", False), ("playground-user", True)])
async def test_memory_preload_requires_a_stable_identity(monkeypatch, user_id, expected):
    preload = AsyncMock()
    monkeypatch.setattr(PreloadMemoryTool, "process_llm_request", preload)
    context = SimpleNamespace(user_id=user_id)
    request = object()
    await agent.StableUserMemoryTool().process_llm_request(tool_context=context, llm_request=request)
    assert bool(preload.await_count) is expected


@pytest.mark.asyncio
@pytest.mark.parametrize("user_id,expected", [("A2A_USER_chapter", False), ("playground-user", True)])
async def test_memory_write_requires_a_stable_identity(user_id, expected):
    context = SimpleNamespace(user_id=user_id, add_session_to_memory=AsyncMock())
    await agent.generate_memories_callback(context)
    assert bool(context.add_session_to_memory.await_count) is expected
