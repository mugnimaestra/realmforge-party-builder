"""Check real tool calls through the chat frontend before recording a demo.

Requires the local agent and proxy, with lab credentials set on the agent.
Run: uv run --with patchright python scripts/check_live_agent.py
"""

import argparse
import json
import logging
import os
import re
import time
from pathlib import Path

import httpx
from patchright.sync_api import sync_playwright

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CASES = [
    ("party", "List my heroes in the party", "list_heroes"),
    ("dice", "Roll 1d20+3 for initiative", "roll_dice"),
    ("bestiary", "Look up a Goblin", "lookup_monster"),
    ("combat", "Simulate my party against an Owlbear using the Python sandbox. State the combat assumptions and report the win percentage.", "code_execution"),
    ("portrait", "Forge a portrait of Valen Ironclad with his runic shield in a dark fantasy style", "generate_item_image"),
]


def safe_text(value: object) -> str:
    text = str(value)
    text = re.sub(r"https?://\S+", "[URL]", text)
    return re.sub(r"[\w.+-]+@[\w.-]+", "[account]", text)[:700]


def check_live_agent(case_names: list[str] | None = None) -> None:
    deadline = time.monotonic() + 30
    while True:
        try:
            httpx.get("http://localhost:8000/a2a/app/.well-known/agent-card.json", timeout=2).raise_for_status()
            break
        except httpx.HTTPError:
            if time.monotonic() >= deadline:
                raise RuntimeError("The local agent is not ready on port 8000") from None
            time.sleep(0.25)
    output = Path(".local-demo")
    output.mkdir(mode=0o700, exist_ok=True)
    turns: list[dict] = []
    with sync_playwright() as browser_api:
        browser = browser_api.chromium.launch(channel="chrome", headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 1000})
        page.goto("http://localhost:8080/", wait_until="domcontentloaded")
        selected = [case for case in CASES if not case_names or case[0] in case_names]
        for name, prompt, expected_tool in selected:
            start = time.monotonic()
            logger.info("Starting %s", name)
            page.locator("#input").fill(prompt)
            with page.expect_response(lambda response: response.url.endswith("/chat"), timeout=390000) as pending:
                page.locator("#form button").click()
            response = pending.value
            parts = response.json().get("parts", [])
            tools = [part for part in parts if part.get("kind") == "tool"]
            names = [part.get("name") for part in tools]
            turns.append({"case": name, "prompt": prompt, "parts": parts})
            path = output / "gate-results.json"
            path.write_text(json.dumps(turns, indent=2), encoding="utf-8")
            os.chmod(path, 0o600)
            case_path = output / f"{name}-result.json"
            case_path.write_text(json.dumps(turns[-1], indent=2), encoding="utf-8")
            os.chmod(case_path, 0o600)
            for part in parts:
                text = part.get("text", "")
                if part.get("kind") == "text" and (text.startswith("Error:") or "error occurred during processing" in text.lower()):
                    raise RuntimeError(f"{name}: {safe_text(text)}")
            if expected_tool not in names:
                notes = [part.get("text", "") for part in parts if part.get("kind") == "text"]
                raise RuntimeError(f"{name}: expected {expected_tool}; got {names}. {safe_text(notes)}")
            for tool in tools:
                data = tool.get("data", {})
                data = data.get("result", data) if isinstance(data, dict) else data
                if isinstance(data, dict) and data.get("error"):
                    raise RuntimeError(f"{name}: {tool['name']} failed: {safe_text(data['error'])}")
                if tool.get("name") == "code_execution" and data.get("outcome") != "OUTCOME_OK":
                    raise RuntimeError(f"{name}: sandbox execution failed: {safe_text(data.get('output'))}")
                if name == "dice" and tool.get("name") == "roll_dice":
                    assert data["modifier"] == 3 and data["total"] == sum(data["rolls"]) + 3
                if name == "portrait" and tool.get("name") == "generate_item_image":
                    assert data.get("public_url", "").startswith("https://")
            page.wait_for_function("document.querySelector('#form button').disabled === false")
            assert page.locator(".msg.agent").last.locator(".a2card").count() > 0
            if name == "portrait":
                page.wait_for_function("Array.from(document.querySelectorAll('.msg.agent:last-child img')).some(image => image.complete && image.naturalWidth > 0)")
            logger.info("%s passed in %.1fs; real tools: %s", name, time.monotonic() - start, ", ".join(names))
        browser.close()
    logger.info("%s live checks passed in one frontend conversation", len(selected))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", action="append", choices=[case[0] for case in CASES])
    check_live_agent(parser.parse_args().case)
