# RealmForge: Turn-Based RPG Party Builder

**RealmForge** is an interactive, conversational RPG companion built on Google's Agent Development Kit (ADK) and Gemini. It enables players to recruit and manage a party of adventurers in Google Cloud Firestore, roll polyhedral dice, query monsters from the D&D 5e Bestiary, run complex combat simulations in a secure Vertex AI Agent Engine code sandbox, generate custom fantasy portraits via Gemini (`gemini-3.1-flash-lite-image`), generate cinematic animations via Google Omni (`gemini-omni-flash-preview`), and render rich turn-based UI cards with **A2UI**.

![RealmForge Demo Walkthrough](docs/demo.gif)

---

## ⚔️ Implemented Features & Architecture

- **🧠 Cross-Session Long-Term Memory (Vertex AI Memory Bank)**:
  - Automatically loads and recalls user party preferences, hero history, and combat notes across sessions using `PreloadMemoryTool` and post-turn `generate_memories_callback`.
- **🛡️ Hero Party Management (Google Cloud Firestore)**:
  - Real-time persistent state stored in a dedicated Firestore `heroes` collection.
  - Tools: `list_heroes`, `get_hero`, `create_or_update_hero`, `update_hero_hp`, and `delete_hero`.
- **🎲 Polyhedral Dice Engine**:
  - Deterministic random dice evaluation (`d4`, `d6`, `d8`, `d10`, `d12`, `d20`, `d100`) with modifiers for initiative, attack rolls, and healing (`roll_dice`).
- **🐉 5e SRD Monster Bestiary API**:
  - Free public live API integration querying creature statistics, armor class, challenge ratings, traits, and actions (`lookup_monster`).
- **🎨 Fantasy Character & Item Generation**:
  - Generates character portraits and item illustrations using Gemini image models (`gemini-3.1-flash-lite-image`), saves them as local ADK artifacts, and uploads them to a public Cloud Storage bucket for direct inline rendering (`generate_item_image`).
- **🎬 Cinematic Video Animations**:
  - Generates short animation clips using Google Omni (`gemini-omni-flash-preview`), saves them as artifacts, and uploads them to Cloud Storage for persistent streaming (`generate_item_video`).
- **💻 Vertex AI Sandboxed Code Execution**:
  - Securely executes Python in an isolated `AgentEngineSandboxCodeExecutor` environment to compute complex damage distributions, win percentages, and turn-based battle simulations.
- **🃏 A2UI Rich Card Display (v0.8)**:
  - Emits schema-compliant A2UI data payloads rewrapped by `a2ui_callback` to render responsive visual cards, hero sheets, and combat summaries in the dev UI.

---

## 📋 Roadmap & Backlog

The following features from the initial design brief are planned for future iterations:

- [ ] **Turn-by-Turn Combat Log Table**: Multi-round automated battle runner formatted into interactive A2UI tabular rows.
- [ ] **Loot & Reward Generator**: Dynamic loot table drops based on defeated monster Challenge Rating (CR).
- [ ] **Custom Audio Soundtrack**: Ambient battle themes and sound effects generated with Lyria.

---

## 🚀 Local Setup & Development

### Prerequisites

- Python 3.11+
- [`uv`](https://docs.astral.sh/uv/) package manager
- Google Cloud SDK (`gcloud`) with Application Default Credentials (ADC) configured:
  ```bash
  gcloud auth application-default login
  ```

### Installation

```bash
# Clone repository
git clone https://github.com/mugnimaestra/realmforge-party-builder.git
cd realmforge-party-builder

# Install dependencies
uv sync
```

### Running the Agent Playground Locally

Start the local ADK web interface:

```bash
uv run adk web . --port 8080 --reload_agents --memory_service_uri=agentengine://865793938617794560
```

> **Tip:** In the web UI, create a **New Session** and turn **Token Streaming** **OFF** in settings ⚙️ to view the rendered A2UI cards.

---

## 📦 Project Structure

```
realmforge-party-builder/
├── app/
│   ├── agent.py               # Root ADK agent, tools, schema, & sandbox configuration
│   ├── a2ui_utils.py          # A2UI v0.8 response unwrapping callback
│   ├── fast_api_app.py        # FastAPI server & A2A protocol router
│   └── app_utils/             # Service registries, session, and artifact managers
├── frontend/                  # Minimal FastAPI proxy and A2A chat web UI
├── scripts/
│   └── seed_firestore.py      # Firestore initial hero party seeder
├── tests/                     # Unit and evaluation datasets
├── pyproject.toml             # Dependencies & UV lock specifications
└── README.md                  # Project documentation & backlog
```
