"""Capture the real renderer with frozen responses from the successful live gate.

uv run --with patchright python demo/capture.py [--styleframe]
No fixture data is generated. Raw cloud responses stay in ignored .local-demo/.
"""

import argparse
import hashlib
import json
import re
import subprocess
import urllib.request
from pathlib import Path

from patchright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "demo/public/textures"


def settled(page):
    page.evaluate("document.fonts.ready")
    page.wait_for_timeout(600)


def replay(page, turn):
    page.goto("http://localhost:8080/", wait_until="domcontentloaded")
    page.emulate_media(reduced_motion="reduce")
    page.evaluate("""turn => {
      document.querySelector('#welcome')?.remove();
      bubble('user').textContent = turn.prompt;
      renderReply(bubble('agent'), turn.parts);
      log.scrollTop = 0;
    }""", turn, isolated_context=False)
    settled(page)
    page.wait_for_function("Array.from(document.images).every(i => i.complete && i.naturalWidth > 0)", timeout=60000)
    text = page.locator("body").inner_text()
    assert not re.search(r"qwiklabs|storage\.googleapis|@|1074897687982", text, re.I), "Sensitive text in capture"


def bbox(locator):
    box = locator.bounding_box()
    assert box
    return {"x": box["x"], "y": box["y"], "w": box["width"], "h": box["height"]}


def main(styleframe=False):
    with sync_playwright() as api:
        browser = api.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=2)
        if styleframe:
            page.goto((ROOT / "demo/styleframe.html").as_uri())
            settled(page)
            out = ROOT / ".local-demo/styleframes"
            out.mkdir(parents=True, exist_ok=True)
            for index, section in enumerate(page.locator(".frame").all()):
                section.screenshot(path=str(out / f"{index}.png"))
            browser.close()
            print("Three styleframes captured for visual review")
            return

        turns = json.loads((ROOT / ".local-demo/gate-results.json").read_text())
        assert [t["case"] for t in turns] == ["party", "dice", "bestiary", "combat", "portrait"]
        DEST.mkdir(parents=True, exist_ok=True)
        page.goto("http://localhost:8080/")
        settled(page)
        page.screenshot(path=str(DEST / "welcome.png"))
        layout = {}
        manifest = {"sourceVersion": 1, "date": "2026-10-22", "source": "one verified frontend conversation", "turns": []}
        for turn in turns:
            name = turn["case"]
            replay(page, turn)
            page.screenshot(path=str(DEST / f"{name}-full.png"))
            card = page.locator(".msg.agent .a2card").last
            card.screenshot(path=str(DEST / f"{name}-card.png"))
            layout[name] = {"pageH": 1080, "card": bbox(card), "rows": []}
            for row in card.locator(".a2text, .a2row").all():
                layout[name]["rows"].append(bbox(row))
            tools = [p for p in turn["parts"] if p.get("kind") == "tool"]
            manifest["turns"].append({"case": name, "prompt": turn["prompt"], "tools": [p["name"] for p in tools]})
            if name == "dice":
                result = next(p["data"] for p in tools if p["name"] == "roll_dice")
                manifest["dice"] = result.get("result", result)
                page.locator(".dice-panel").screenshot(path=str(DEST / "dice-panel.png"))
                macro = browser.new_page(viewport={"width": 375, "height": 812}, device_scale_factor=8)
                replay(macro, turn)
                macro.locator(".die").screenshot(path=str(DEST / "die.png"), omit_background=True)
                macro.close()
            if name == "combat":
                result = next(p["data"] for p in tools if p["name"] == "code_execution")
                assert result["outcome"] == "OUTCOME_OK"
                manifest["combat"] = {"outcome": result["outcome"], "output": result["output"]}
            if name == "portrait":
                page.locator(".msg.agent .media-frame").first.screenshot(path=str(DEST / "portrait-frame.png"))
                page.locator(".msg.agent img").first.screenshot(path=str(DEST / "portrait.png"))
            if name == "party":
                heads = card.locator(".a2-h2").all()
                names = [h.inner_text() for h in heads]
                index = next(i for i, value in enumerate(names) if "Elena" in value)
                start = bbox(heads[index])
                end = bbox(heads[index + 1])
                rect = {"x": layout[name]["card"]["x"] + 24, "y": start["y"], "width": layout[name]["card"]["w"] - 48, "height": end["y"] - start["y"]}
                layout[name]["hero"] = {"x": rect["x"], "y": rect["y"], "w": rect["width"], "h": rect["height"]}
                hires = browser.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=4)
                replay(hires, turn)
                hires.screenshot(path=str(DEST / "hero-hires.png"), clip=rect)
                hires.close()

        optional_path = ROOT / ".local-demo/video-result.json"
        if optional_path.exists():
            parts = json.loads(optional_path.read_text())["parts"]
            tool = next(p for p in parts if p.get("name") == "generate_item_video")
            data = tool["data"].get("result", tool["data"])
            url = data["public_url"]
            assert url.startswith("https://storage.googleapis.com/")
            media = ROOT / "demo/public/video/valen.mp4"
            media.parent.mkdir(parents=True, exist_ok=True)
            urllib.request.urlretrieve(url, media)
            replay(page, {"prompt": "Generate a short cinematic video of Valen Ironclad raising his runic shield", "parts": parts})
            page.wait_for_function("document.querySelector('video')?.readyState >= 1", timeout=60000)
            page.locator("video").evaluate("video => {video.preload = 'auto'; video.load();}")
            page.wait_for_function("document.querySelector('video')?.readyState >= 2", timeout=60000)
            page.locator("video").evaluate("video => {video.pause(); video.currentTime = 1;}")
            page.wait_for_timeout(600)
            page.screenshot(path=str(DEST / "video-full.png"))
            manifest["video"] = {"tool": "generate_item_video", "inlinePlayback": True, "sha256": hashlib.sha256(media.read_bytes()).hexdigest()}

        screenshots = ROOT / "docs/screenshots"
        screenshots.mkdir(parents=True, exist_ok=True)
        baseline = subprocess.check_output(["git", "show", "5af210a:frontend/static/index.html"], cwd=ROOT, text=True)
        for label, html in [("before", baseline), ("after", None)]:
            for width, height in [(1440, 1000), (375, 812)]:
                page.set_viewport_size({"width": width, "height": height})
                if html:
                    page.goto("http://localhost:8080/")
                    page.set_content(html)
                    page.evaluate("turn => {bubble('user').textContent=turn.prompt;renderReply(bubble('agent'),turn.parts)}", turns[0], isolated_context=False)
                    settled(page)
                else:
                    replay(page, turns[0])
                page.screenshot(path=str(screenshots / f"{label}-{width}.png"))
        browser.close()
    (DEST / "layout.json").write_text(json.dumps(layout, indent=2) + "\n")
    manifest["textures"] = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(DEST.glob("*.png"))}
    (ROOT / "demo/src/evidence.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print("Verified captures, coordinates, and source hashes saved; no cloud URLs exported")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--styleframe", action="store_true")
    main(parser.parse_args().styleframe)
