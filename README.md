# RealmForge

**Your party, at the table.** A conversational RPG companion built with Google
ADK, Gemini, Firestore, and A2UI. Manage heroes, roll dice, open the bestiary,
simulate encounters, and forge fantasy portraits and video from one chat.

[![RealmForge demo: hero sheets, dice, and the bestiary](docs/demo.gif)](docs/demo.mp4)

**[Watch the demo with music](docs/demo.mp4)** · [SFX-only version](docs/demo-nobgm.mp4) · [Editable video source](demo/README.md)

50 seconds · 1080p · 60 fps · 120 BPM. The 12-second preview and full reel use
real agent responses and generated media. Waiting time is edited. The shown
roll is **12 + 3 = 15**; the encounter result is from a simplified simulation
whose assumptions appear on screen.

## Current state

Verified on **2026-10-22**: all five core prompts called their real tools through
the local frontend in one conversation, and passed again after the final agent
changes. Portrait generation and optional video generation both succeeded.
The unit suite passed **18 tests**. These checks used live cloud tools through
the local agent; the deployed runtime has not been revalidated.

The frontend has a dark fantasy tabletop theme, five quick prompts, hero HP
bars and stat pills, dice animation driven by the actual result, inline images
and video, and a thinking state. Browser checks covered **1440 px and 375 px**,
keyboard focus, reduced motion, and selected text contrast of at least 4.5:1.
It remains one vanilla HTML/JS file with no frontend build step.

[Desktop screenshot](docs/screenshots/after-1440.png) · [Mobile screenshot](docs/screenshots/after-375.png) · [Verification record](demo/QA.md) · [Independent review](demo/REVIEW.md)

## What you can do

| Capability | Implementation |
| --- | --- |
| Manage a persistent party | Firestore `heroes` collection; `list_heroes`, `get_hero`, `create_or_update_hero`, `update_hero_hp`, and `delete_hero`. |
| Roll dice | `roll_dice` supports polyhedral dice and modifiers; the UI animates the returned roll. |
| Look up monsters | `lookup_monster` retrieves 5e SRD statistics, traits, and actions from the public bestiary API. |
| Test encounters | Python runs in the Vertex AI Agent Engine sandbox and returns its actual output and stated assumptions. |
| Forge images and video | `generate_item_image` uses `gemini-3.1-flash-lite-image`; `generate_item_video` uses `gemini-omni-flash-preview`. Media is uploaded to Cloud Storage and displayed inline. |
| View rich responses | A2UI v0.8 cards, rows, columns, text, lists, dividers, images, and icons; the frontend also handles inline video. |

The root agent uses `gemini-3.8-flash`. The browser talks to a same-origin
FastAPI proxy, which forwards A2A requests to the local or deployed agent.
Cloud credentials stay on the server. Tool results pass through the proxy so
dice and sandbox displays can use the actual result.

### Known limits

- **Memory depends on identity.** Stable ADK playground user IDs can use Vertex
  AI Memory Bank across sessions. A new chapter in the custom A2A frontend gets
  a new anonymous identity and skips Memory Bank reads/writes. Conversation
  history works within that chapter; hero records persist separately in Firestore.
- **Cloud latency varies.** A verified party request took over four minutes.
  The UI shows a still-working notice after 30 seconds and allows up to six
  minutes for a reply.
- **A successful simulation can have no model summary.** In that case the UI
  shows a “Verified sandbox result” card with the verbatim output and explains
  that no summary was returned. The demo's 1,000/1,000 wins apply only to its
  printed simplified rules, not a general encounter prediction.
- **Local verification does not deploy the agent.** No deployment was performed
  for this update. Deployment requires explicit approval under [GEMINI.md](GEMINI.md).

## Run locally

### Prerequisites

- Python 3.11–3.13
- [`uv`](https://docs.astral.sh/uv/) package manager
- Google Cloud SDK (`gcloud`) and Application Default Credentials (ADC) with
  access to the configured Firestore, Vertex AI models, Memory Bank, sandbox,
  and asset bucket

Use existing ADC or authenticate with the account that has project access:

```bash
gcloud auth application-default login
```

The repository currently references existing Google Cloud resources in
[`app/agent.py`](app/agent.py), [`app/app_utils/services.py`](app/app_utils/services.py),
and [`scripts/seed_firestore.py`](scripts/seed_firestore.py). Installing
dependencies does not provision those resources. Node.js and FFmpeg are only
needed to rebuild the [demo](demo/README.md).

### Installation

```bash
git clone https://github.com/mugnimaestra/realmforge-party-builder.git
cd realmforge-party-builder
uv sync
```

### Run the themed frontend locally

In the repository root, configure the Vertex AI backend:

```bash
export GOOGLE_GENAI_USE_VERTEXAI=true
export GOOGLE_CLOUD_PROJECT=qwiklabs-gcp-04-858b990e3059
export GOOGLE_CLOUD_LOCATION=global
```

Optionally seed the four example heroes. **This replaces those four records**;
skip it to keep edits to the example party:

```bash
uv run python scripts/seed_firestore.py
```

Start the agent in that terminal:

```bash
APP_URL=http://localhost:8000 uv run python -m app.fast_api_app
```

From the repository root in a second terminal, start the proxy from `frontend/`:

```bash
cd frontend
unset AGENT_ENGINE_RESOURCE_NAME
uv run python main.py
```

Open [localhost:8080](http://localhost:8080). Without `AGENT_ENGINE_RESOURCE_NAME`, the proxy sends A2A requests to `http://localhost:8000/a2a/app` without authentication headers. The local agent uses server-side ADC for its cloud tools. To connect to a deployed agent, set `AGENT_ENGINE_RESOURCE_NAME` before starting the proxy; that mode uses ADC authentication.

Gemini uses the global endpoint. Memory Bank and the sandbox use their configured
region, `us-east1`; setting the model endpoint to `global` does not move them.

### Try the five core prompts

The welcome screen and sidebar provide these actions:

1. “List my heroes in the party”
2. “Roll 1d20+3 for initiative”
3. “Look up a Goblin”
4. “Simulate my party against an Owlbear using the Python sandbox. State your combat assumptions and report the win percentage.”
5. “Forge a portrait of Valen Ironclad with his runic shield in a dark fantasy style”

### ADK playground

The same agent server also provides the ADK playground at
[localhost:8000](http://localhost:8000). Create a **New Session** and turn
**Token Streaming off** in settings to view the rendered A2UI cards.

### Checks

```bash
uv run pytest tests/unit
# Browser checks with the local frontend running (Chrome required):
uv run --with patchright python scripts/check_frontend.py
# Five real tool calls with both servers running; uses cloud quota:
uv run --with patchright python scripts/check_live_agent.py
```

The live check stores raw responses in ignored `.local-demo/`. See the
[verification record](demo/QA.md) for the recorded results and scope.

## Demo source and license

The editable [demo project](demo/README.md) uses Remotion, with video-shotcraft
camera recipes and the hyperframes-motion-reel reference's beat grid and kinetic
type. Remotion is free for individuals and companies with three or fewer
employees; this is a personal hackathon project. See the [Remotion license](https://www.remotion.dev/license).
The project includes an original 120 BPM score and attributed cinematic sound
effects. The SFX-only delivery shares the same picture track as the music
version. Both MP4s are below 10 MB; the GIF is below 5 MB. Rebuild instructions
are in [demo/README.md](demo/README.md), creative decisions in
[demo/DESIGN.md](demo/DESIGN.md), and asset licenses in
[demo/ATTRIBUTION.md](demo/ATTRIBUTION.md).

## Project structure

```
realmforge-party-builder/
├── app/
│   ├── agent.py               # Gemini agent, tools, A2UI instructions, sandbox
│   ├── a2ui_utils.py          # A2UI response callback
│   ├── fast_api_app.py        # ADK playground and local A2A server
│   └── app_utils/             # Shared services and A2A routing
├── frontend/
│   ├── main.py                # Local/deployed A2A proxy
│   └── static/index.html      # Tabletop chat UI; no build step
├── demo/                      # Editable Remotion reel, assets, and QA records
├── docs/                      # MP4s, preview GIF, and desktop/mobile screenshots
├── scripts/
│   ├── seed_firestore.py      # Example party seeder
│   ├── check_frontend.py      # Browser rendering/accessibility checks
│   └── check_live_agent.py    # Real frontend-to-tool verification
├── tests/                     # Unit tests and evaluation datasets
├── pyproject.toml             # Python dependencies
└── uv.lock                    # Locked Python environment
```

## Backlog

- [ ] Turn-by-turn combat log tables in A2UI.
- [ ] Loot and reward generation based on monster challenge rating.
- [ ] In-app ambient music and sound effects generated with Lyria. The demo's
  existing score and SFX are part of the video project, not a runtime agent tool.
