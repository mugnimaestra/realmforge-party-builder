"""Do not let final-response formatting remove a sandbox request."""

import json

import pytest
from google.adk.models.llm_response import LlmResponse
from google.genai import types

from app.a2ui_utils import a2ui_callback

SURFACE = [
    {"beginRendering": {"surfaceId": "test", "root": "root"}},
    {"surfaceUpdate": {"surfaceId": "test", "components": [
        {"id": "root", "component": {"Text": {"text": {"literalString": "Result"}}}},
    ]}},
]


@pytest.mark.parametrize("language", ["python", "tool_code"])
def test_python_requests_reach_the_code_executor(language):
    text = f"```{language}\nprint({json.dumps(SURFACE)})\n```"
    response = LlmResponse(content=types.Content(role="model", parts=[types.Part(text=text)]))
    assert a2ui_callback(None, response) is None


def test_executable_parts_are_not_removed_by_ui_text():
    response = LlmResponse(content=types.Content(role="model", parts=[
        types.Part.from_executable_code(code="print(2)", language="PYTHON"),
        types.Part(text=json.dumps(SURFACE)),
    ]))
    assert a2ui_callback(None, response) is None


def test_final_ui_response_still_renders():
    response = LlmResponse(content=types.Content(role="model", parts=[types.Part(text=json.dumps(SURFACE))]))
    result = a2ui_callback(None, response)
    assert result is not None
    assert result.content.parts[0].inline_data.mime_type == "text/plain"
