# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
import json
import random
import re
import urllib.parse
import urllib.request
import uuid
from zoneinfo import ZoneInfo

from google import genai
from google.cloud import firestore, storage
from a2ui.basic_catalog.provider import BasicCatalog
from a2ui.schema.manager import A2uiSchemaManager
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.apps import App
from google.adk.code_executors.agent_engine_sandbox_code_executor import (
    AgentEngineSandboxCodeExecutor,
)
from google.adk.models import Gemini
from google.adk.tools import ToolContext
from google.adk.tools.preload_memory_tool import PreloadMemoryTool
from google.genai import types

from app.a2ui_utils import a2ui_callback

load_dotenv()

MODEL = "gemini-3.8-flash"

# Hardcoded project ID and bucket name as required for Agent Platform compatibility
PROJECT_ID = "qwiklabs-gcp-04-858b990e3059"
COLLECTION_NAME = "heroes"
BUCKET_NAME = "realmforge-assets-qwiklabs-gcp-04-858b990e3059"
SANDBOX_RESOURCE_NAME = "projects/1074897687982/locations/us-east1/reasoningEngines/865793938617794560/sandboxEnvironments/683636747732516864"

_db = None
_genai_client = None
_storage_client = None


def get_firestore_client() -> firestore.Client:
    """Returns a singleton Firestore client configured with the hardcoded project ID."""
    global _db
    if _db is None:
        _db = firestore.Client(project=PROJECT_ID)
    return _db


def get_genai_client() -> genai.Client:
    """Returns a singleton GenAI client in the global region for image generation."""
    global _genai_client
    if _genai_client is None:
        _genai_client = genai.Client(vertexai=True, project=PROJECT_ID, location="global")
    return _genai_client


def get_storage_client() -> storage.Client:
    """Returns a singleton Cloud Storage client."""
    global _storage_client
    if _storage_client is None:
        _storage_client = storage.Client(project=PROJECT_ID)
    return _storage_client


def list_heroes() -> list[dict]:
    """Retrieves all heroes and party members from the Firestore database.

    Returns:
        A list of hero dictionaries containing id, name, class_name, level, hp,
        max_hp, attack, defense, abilities, backstory, and status.
    """
    db = get_firestore_client()
    docs = db.collection(COLLECTION_NAME).stream()
    heroes = [doc.to_dict() for doc in docs]
    return heroes


def get_hero(hero_id: str) -> dict:
    """Retrieves details for a specific hero by their hero ID.

    Args:
        hero_id: The unique identifier of the hero (e.g., 'valen-ironclad', 'lyra-spellweaver').

    Returns:
        The hero data dictionary, or an error message if not found.
    """
    db = get_firestore_client()
    doc_ref = db.collection(COLLECTION_NAME).document(hero_id)
    doc = doc_ref.get()
    if not doc.exists:
        return {"error": f"Hero with ID '{hero_id}' not found."}
    return doc.to_dict()


def create_or_update_hero(
    hero_id: str,
    name: str,
    class_name: str,
    level: int = 1,
    hp: int = 100,
    max_hp: int = 100,
    attack: int = 15,
    defense: int = 12,
    abilities: list[str] | None = None,
    backstory: str = "",
    status: str = "In Party",
) -> dict:
    """Creates a new hero or updates an existing hero in Firestore.

    Args:
        hero_id: Unique string ID for the hero (e.g., 'thorin-shieldbearer').
        name: Full display name of the hero.
        class_name: RPG class (e.g., 'Warrior', 'Mage', 'Rogue', 'Cleric', 'Paladin').
        level: Character level (default 1).
        hp: Current health points (default 100).
        max_hp: Maximum health points (default 100).
        attack: Attack power stat (default 15).
        defense: Defense armor stat (default 12).
        abilities: List of special skill or spell names.
        backstory: Brief lore or character background.
        status: Current status (e.g., 'In Party', 'Bench', 'Fallen').

    Returns:
        The saved hero dictionary.
    """
    db = get_firestore_client()
    if abilities is None:
        abilities = ["Basic Attack"]

    hero_data = {
        "id": hero_id,
        "name": name,
        "class_name": class_name,
        "level": level,
        "hp": hp,
        "max_hp": max_hp,
        "attack": attack,
        "defense": defense,
        "abilities": abilities,
        "backstory": backstory,
        "status": status,
    }

    db.collection(COLLECTION_NAME).document(hero_id).set(hero_data)
    return hero_data


def update_hero_hp(hero_id: str, hp_change: int) -> dict:
    """Modifies a hero's current HP by a specified amount (positive for healing, negative for damage).

    Args:
        hero_id: The ID of the hero to modify.
        hp_change: Integer amount to adjust HP by (e.g., -25 for damage, +30 for heal).

    Returns:
        Updated hero data dictionary or error message if not found.
    """
    db = get_firestore_client()
    doc_ref = db.collection(COLLECTION_NAME).document(hero_id)
    doc = doc_ref.get()
    if not doc.exists:
        return {"error": f"Hero with ID '{hero_id}' not found."}

    data = doc.to_dict()
    current_hp = data.get("hp", 100)
    max_hp = data.get("max_hp", 100)
    new_hp = max(0, min(max_hp, current_hp + hp_change))
    data["hp"] = new_hp
    if new_hp == 0:
        data["status"] = "Fallen"
    elif data.get("status") == "Fallen" and new_hp > 0:
        data["status"] = "In Party"

    doc_ref.set(data)
    return {
        "hero_id": hero_id,
        "name": data.get("name"),
        "previous_hp": current_hp,
        "current_hp": new_hp,
        "max_hp": max_hp,
        "status": data.get("status"),
    }


def delete_hero(hero_id: str) -> dict:
    """Deletes a hero from the Firestore database.

    Args:
        hero_id: The ID of the hero to delete.

    Returns:
        Status confirmation dictionary.
    """
    db = get_firestore_client()
    doc_ref = db.collection(COLLECTION_NAME).document(hero_id)
    if not doc_ref.get().exists:
        return {"error": f"Hero with ID '{hero_id}' not found."}
    doc_ref.delete()
    return {"message": f"Hero '{hero_id}' has been successfully deleted."}


def roll_dice(dice_notation: str = "1d20", modifier: int = 0) -> dict:
    """Rolls polyhedral RPG dice using standard notation (e.g., '1d20', '2d6', '1d8', '3d10').

    Args:
        dice_notation: Standard dice string like '1d20', '2d6', '1d8', or 'd20' (default: '1d20').
        modifier: Integer modifier added to the total (e.g., +3 for attack bonus, -2 for debuff).

    Returns:
        A dictionary with individual rolls, subtotal, modifier, final total, and crit flags.
    """
    clean = dice_notation.strip().lower()
    match = re.match(r"^(\d*)d(\d+)$", clean)
    if not match:
        count, sides = 1, 20
    else:
        count_str, sides_str = match.groups()
        count = int(count_str) if count_str else 1
        sides = int(sides_str)

    count = max(1, min(count, 20))
    sides = max(2, min(sides, 100))

    rolls = [random.randint(1, sides) for _ in range(count)]
    subtotal = sum(rolls)
    total = subtotal + modifier

    is_crit_success = sides == 20 and count == 1 and rolls[0] == 20
    is_crit_fumble = sides == 20 and count == 1 and rolls[0] == 1

    return {
        "dice": f"{count}d{sides}",
        "rolls": rolls,
        "subtotal": subtotal,
        "modifier": modifier,
        "total": total,
        "is_crit_success": is_crit_success,
        "is_crit_fumble": is_crit_fumble,
    }


def lookup_monster(monster_name: str) -> dict:
    """Fetches real monster stats, actions, HP, AC, and CR from the free public D&D 5e Bestiary API.

    Args:
        monster_name: The name or query for the monster (e.g., 'goblin', 'skeleton', 'adult-red-dragon', 'beholder').

    Returns:
        A dictionary containing real monster data including name, type, size, alignment, hit_points,
        armor_class, challenge_rating, xp, special abilities, and combat actions.
    """
    clean_name = monster_name.strip().lower().replace(" ", "-")
    url = f"https://www.dnd5eapi.co/api/2014/monsters/{urllib.parse.quote(clean_name)}"

    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "RealmForge/1.0", "Accept": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode())
                ac = (
                    data.get("armor_class", [{}])[0].get("value")
                    if isinstance(data.get("armor_class"), list) and data.get("armor_class")
                    else data.get("armor_class")
                )
                actions = [
                    {"name": a.get("name"), "desc": a.get("desc")}
                    for a in data.get("actions", [])
                ]
                special_abilities = [
                    {"name": a.get("name"), "desc": a.get("desc")}
                    for a in data.get("special_abilities", [])
                ]
                return {
                    "name": data.get("name"),
                    "type": data.get("type"),
                    "size": data.get("size"),
                    "alignment": data.get("alignment"),
                    "hit_points": data.get("hit_points"),
                    "armor_class": ac,
                    "challenge_rating": data.get("challenge_rating"),
                    "xp": data.get("xp"),
                    "actions": actions,
                    "special_abilities": special_abilities,
                }
    except Exception:
        # Fallback to search endpoint if exact slug doesn't match
        search_url = f"https://www.dnd5eapi.co/api/2014/monsters?name={urllib.parse.quote(monster_name)}"
        try:
            req = urllib.request.Request(
                search_url,
                headers={"User-Agent": "RealmForge/1.0", "Accept": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                search_data = json.loads(response.read().decode())
                results = search_data.get("results", [])
                if results:
                    first_match = results[0]["index"]
                    return lookup_monster(first_match)
        except Exception as e:
            return {"error": f"Failed to fetch monster '{monster_name}': {str(e)}"}

    return {"error": f"Monster '{monster_name}' not found in the public bestiary database."}


async def generate_item_image(
    item_name: str,
    description: str,
    tool_context: ToolContext,
) -> dict:
    """Generates an image for a hero, monster, weapon, spell, or item using gemini-3.1-flash-lite-image in the global region.

    Saves the image into the Playground Artifacts panel and uploads it directly to the public Cloud Storage bucket without saving to a local file.

    Args:
        item_name: Name of the hero, monster, weapon, spell, or item (e.g., 'Valen Ironclad', 'Shadow Dragon', 'Flaming Longsword').
        description: Visual description or style guidance (e.g., 'Epic armored knight with glowing runic shield, dramatic lighting').
        tool_context: ToolContext used to save the artifact for the ADK Playground.

    Returns:
        A dictionary containing the item_name, artifact_filename, and the public HTTPS URL.
    """
    client = get_genai_client()
    prompt = f"Fantasy RPG concept art illustration of {item_name}: {description}, highly detailed, digital art"

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite-image",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=[types.Modality.TEXT, types.Modality.IMAGE],
        ),
    )

    image_bytes = None
    mime_type = "image/png"
    for candidate in response.candidates:
        if candidate.content and candidate.content.parts:
            for part in candidate.content.parts:
                if part.inline_data and part.inline_data.data:
                    image_bytes = part.inline_data.data
                    mime_type = part.inline_data.mime_type or "image/png"
                    break

    if not image_bytes:
        return {"error": f"Failed to generate image for '{item_name}'."}

    safe_name = re.sub(r"[^a-zA-Z0-9_\-]", "_", item_name.strip().lower())
    ext = "jpg" if "jpeg" in mime_type else "png"
    artifact_filename = f"{safe_name}.{ext}"

    # (1) Save artifact so it shows up in Playground's Artifacts panel
    if tool_context:
        try:
            artifact_part = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
            await tool_context.save_artifact(filename=artifact_filename, artifact=artifact_part)
        except Exception:
            pass

    # (2) Upload image bytes directly to GCS bucket without writing to local file
    storage_client = get_storage_client()
    bucket = storage_client.bucket(BUCKET_NAME)
    object_name = f"images/{safe_name}_{uuid.uuid4().hex[:8]}.{ext}"
    blob = bucket.blob(object_name)
    blob.upload_from_string(image_bytes, content_type=mime_type)

    public_url = f"https://storage.googleapis.com/{BUCKET_NAME}/{object_name}"

    return {
        "item_name": item_name,
        "artifact_filename": artifact_filename,
        "public_url": public_url,
    }


async def generate_memories_callback(callback_context: CallbackContext):
    """WRITE: after each turn, send the session events to Memory Bank for durable fact extraction."""
    await callback_context.add_session_to_memory()
    return None


schema_manager = A2uiSchemaManager(
    version="0.8",
    catalogs=[BasicCatalog.get_config("0.8")],
)

instruction = schema_manager.generate_system_prompt(
    role_description=(
        "You are RealmForge, an interactive RPG party builder and encounter assistant. "
        "You manage heroes stored in Firestore, display their stats and abilities, and help the player "
        "form and manage their adventuring team for turn-based encounters. "
        "You remember the player's preferences, favorite party comps, strategy notes, and past adventures across conversations. "
        "Use the Firestore tools to list, inspect, recruit, update, or heal heroes. "
        "Use the roll_dice tool whenever rolling dice for attacks, checks, or damage. "
        "Use the lookup_monster tool to fetch real stats and abilities for any monster or boss from the public bestiary database. "
        "Use the generate_item_image tool whenever the player wants an illustration or portrait for a hero, monster, spell, or item. "
        "You have access to a secure Python sandbox via code execution to perform complex combat math, probability analyses, simulation runs, or stat calculations."
    ),
    workflow_description="Analyze the request, call the appropriate tools (Firestore, dice roller, monster bestiary, image generator, Python sandbox, or memory), and return structured UI when appropriate.",
    ui_description=(
        "Keep every surface tiny and flat: ONE Card > ONE Column > a few Text rows. "
        "Never nest a Card inside a Card. "
        "Use ONLY these components: Card, Column, Row, Text, and Image. Do not use "
        "Table or Heading (unsupported), or Buttons, actions, or forms (they do "
        "nothing in adk web). "
        "You may include one Image component, but only when you have a public https "
        "URL for the image (for example the URL an image tool returns after uploading "
        "to a public bucket). Set the Image url to that exact https link, for example "
        '{"Image": {"url": {"literalString": "https://..."}}}. Never point an '
        "Image at a bare filename, an artifact name, or a non-http(s) path. If you do "
        "not have a public URL, add a short Text line noting the image instead. "
        "No markdown in text; use the usageHint property ('h1', 'h2', 'body') for "
        "headings and emphasis. "
        "Output ONLY the raw A2UI JSON array — no prose, and never wrap it in "
        "<a2a_datapart_json> tags or 'kind'/'data'/'metadata' objects."
    ),
    include_schema=True,
    include_examples=True,
)


root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model=MODEL,
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=instruction,
    tools=[
        PreloadMemoryTool(),
        list_heroes,
        get_hero,
        create_or_update_hero,
        update_hero_hp,
        delete_hero,
        roll_dice,
        lookup_monster,
        generate_item_image,
    ],
    code_executor=AgentEngineSandboxCodeExecutor(
        sandbox_resource_name=SANDBOX_RESOURCE_NAME,
    ),
    after_model_callback=a2ui_callback,
    after_agent_callback=generate_memories_callback,
)

app = App(
    root_agent=root_agent,
    name="app",
)
