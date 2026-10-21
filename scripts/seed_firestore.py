"""Seed Firestore with initial heroes for RealmForge Turn-Based Party Builder."""

from google.cloud import firestore

# Project ID hardcoded as required for Agent Platform compatibility
PROJECT_ID = "qwiklabs-gcp-04-858b990e3059"
COLLECTION_NAME = "heroes"

SEED_HEROES = [
    {
        "id": "valen-ironclad",
        "name": "Valen Ironclad",
        "class_name": "Warrior",
        "level": 1,
        "hp": 120,
        "max_hp": 120,
        "attack": 18,
        "defense": 16,
        "abilities": ["Shield Bash", "Taunt", "Heavy Strike"],
        "backstory": "A stalwart knight who protects allies with an impenetrable tower shield.",
        "status": "In Party",
    },
    {
        "id": "lyra-spellweaver",
        "name": "Lyra Spellweaver",
        "class_name": "Mage",
        "level": 1,
        "hp": 70,
        "max_hp": 70,
        "attack": 22,
        "defense": 8,
        "abilities": ["Fireball", "Arcane Missiles", "Frost Nova"],
        "backstory": "A prodigy from the High Academy capable of channeling raw elemental fury.",
        "status": "In Party",
    },
    {
        "id": "kael-shadowblade",
        "name": "Kael Shadowblade",
        "class_name": "Rogue",
        "level": 1,
        "hp": 85,
        "max_hp": 85,
        "attack": 20,
        "defense": 11,
        "abilities": ["Backstab", "Shadow Step", "Poison Blade"],
        "backstory": "A silent scout who strikes from the dark with lethal precision.",
        "status": "In Party",
    },
    {
        "id": "elena-dawnlight",
        "name": "Elena Dawnlight",
        "class_name": "Cleric",
        "level": 1,
        "hp": 95,
        "max_hp": 95,
        "attack": 12,
        "defense": 14,
        "abilities": ["Radiant Heal", "Holy Smite", "Blessing of Protection"],
        "backstory": "A devoted priestess of the Sun Order dedicated to mending wounds and banishing darkness.",
        "status": "In Party",
    },
]


def seed_database():
    print(f"Connecting to Firestore in project '{PROJECT_ID}'...")
    db = firestore.Client(project=PROJECT_ID)
    heroes_ref = db.collection(COLLECTION_NAME)

    for hero in SEED_HEROES:
        doc_ref = heroes_ref.document(hero["id"])
        doc_ref.set(hero)
        print(f"✓ Seeded hero: {hero['name']} ({hero['class_name']}) -> doc ID: {hero['id']}")

    print("\nDatabase seeding completed successfully!")


if __name__ == "__main__":
    seed_database()
