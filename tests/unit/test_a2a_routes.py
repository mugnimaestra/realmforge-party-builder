"""Check that the locked A2A SDK can serve the local agent card."""

import httpx
import pytest
from a2a.server.tasks import InMemoryTaskStore
from fastapi import FastAPI
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

from app.app_utils.a2a import attach_a2a_routes


@pytest.mark.asyncio
async def test_local_card_uses_the_locked_sdk():
    server = FastAPI()
    agent = Agent(name="test_agent", model="gemini-3.8-flash")
    runner = Runner(agent=agent, app_name="test_app", session_service=InMemorySessionService())
    await attach_a2a_routes(
        server, agent=agent, runner=runner, task_store=InMemoryTaskStore(),
        rpc_path="/a2a/app", app_url="http://localhost:8000",
    )
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=server), base_url="http://test") as client:
        response = await client.get("/a2a/app/.well-known/agent-card.json")
    assert response.status_code == 200
    assert response.json()["url"] == "http://localhost:8000/a2a/app"
