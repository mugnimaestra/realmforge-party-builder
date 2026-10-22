"""Run browser checks without capturing test data as demo footage.

Run with both local servers ready:
    uv run --with patchright python scripts/check_frontend.py
"""

import logging
import re

from patchright.sync_api import sync_playwright

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def contrast_ratio(first: str, second: str) -> float:
    def luminance(color: str) -> float:
        values = [int(value) / 255 for value in re.findall(r"\d+", color)[:3]]
        linear = [value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4 for value in values]
        return sum(value * weight for value, weight in zip(linear, (0.2126, 0.7152, 0.0722), strict=True))

    light, dark = sorted((luminance(first), luminance(second)), reverse=True)
    return (light + 0.05) / (dark + 0.05)


def check_frontend() -> None:
    with sync_playwright() as browser_api:
        browser = browser_api.chromium.launch(channel="chrome", headless=True)
        page = browser.new_page()
        errors: list[str] = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        for width, height in [(1440, 1000), (375, 812)]:
            page.set_viewport_size({"width": width, "height": height})
            page.goto("http://localhost:8080/", wait_until="domcontentloaded")
            assert page.title().startswith("RealmForge")
            assert page.locator(".welcome [data-prompt]").count() == 5
            assert page.locator("label[for=input]").count() == 1
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.locator("#input").focus()
            assert page.locator("#input").evaluate("e => getComputedStyle(e).outlineStyle") != "none"
            logger.info("Layout and focus checks passed at %s px", width)

        # These are test fixtures only. Never use them for product captures.
        page.evaluate("""() => {
          const components = [
            {id:'root',component:{Card:{child:'column'}}},
            {id:'column',component:{Column:{children:{explicitList:['name','hp','row','divider','list','image','icon','unsafe','caption']}}}},
            {id:'name',component:{Text:{text:{literalString:'Renderer test'},usageHint:'h2'}}},
            {id:'hp',component:{Text:{text:{literalString:'HP 23/30'}}}},
            {id:'row',component:{Row:{children:{explicitList:['attack']}}}},
            {id:'attack',component:{Text:{text:{literalString:'Attack 18'}}}},
            {id:'divider',component:{Divider:{}}},
            {id:'list',component:{List:{children:{explicitList:['note']}}}},
            {id:'note',component:{Text:{text:{literalString:'<script>unsafe()</script>'}}}},
            {id:'image',component:{Image:{url:{literalString:'https://example.invalid/image.png'}}}},
            {id:'icon',component:{Icon:{name:{literalString:'shield'}}}},
            {id:'unsafe',component:{Image:{url:{literalString:'http://example.invalid/unsafe.png'}}}},
            {id:'caption',component:{Text:{text:{literalString:'Test caption'},usageHint:'caption'}}},
          ];
          renderReply(bubble('agent'), [
            {kind:'tool',name:'roll_dice',data:{dice:'1d20',rolls:[17],modifier:3,total:20}},
            {kind:'a2ui',data:{surfaceUpdate:{surfaceId:'test',components}}},
            {kind:'a2ui',data:{beginRendering:{surfaceId:'test',root:'root'}}},
          ]);
        }""", isolated_context=False)
        for selector in [".a2card", ".a2col", ".a2row", ".a2divider", ".a2img", ".material-symbols-outlined", ".stat-pill"]:
            assert page.locator(selector).count() > 0, selector
        assert page.locator("progress").get_attribute("value") == "23"
        assert page.locator(".a2img").count() == 1
        assert page.locator(".die").inner_text() == "17"
        assert "Natural 20" not in page.locator(".dice-panel").inner_text()
        assert "<script>unsafe()</script>" in page.locator(".a2card").inner_text()
        assert page.locator(".a2card script").count() == 0
        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
        colors = page.evaluate("""selectors => selectors.map(selector => {
          const node = document.querySelector(selector);
          let parent = node;
          while (parent && ['rgba(0, 0, 0, 0)', 'transparent'].includes(getComputedStyle(parent).backgroundColor)) parent = parent.parentElement;
          return [selector, getComputedStyle(node).color, getComputedStyle(parent || document.body).backgroundColor];
        })""", [".brand-note", ".eyebrow", ".welcome p", ".prompt strong", ".prompt small", ".speaker", ".a2text", ".a2-caption", ".stat-pill", ".tool-chip", ".dice-panel strong", ".dice-panel small", ".send", ".composer-note"])
        for selector, foreground, background in colors:
            assert contrast_ratio(foreground, background) >= 4.5, (selector, foreground, background)
        logger.info("Text contrast checks passed at 4.5:1 or higher")
        page.emulate_media(reduced_motion="reduce")
        assert page.locator(".die").evaluate("e => getComputedStyle(e).animationName") == "none"

        page.evaluate("""() => {
          const output = document.createElement('div'); output.id = 'media-test'; document.body.append(output);
          appendText(output, 'Forged: https://storage.googleapis.com/test/video.mp4');
        }""", isolated_context=False)
        assert page.locator("#media-test video[controls]").count() == 1
        assert "storage.googleapis.com" not in page.locator("#media-test").inner_text()
        assert not errors, errors
        browser.close()
        logger.info("A2UI, media, dice, text safety, and reduced motion checks passed")


if __name__ == "__main__":
    check_frontend()
