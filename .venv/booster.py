import requests
import json
import time
import os
import random

# Booster config
PACK_STRUCTURE = {
    "rare": 1,
    "uncommon": 3,
    "common": 6
}

COLLECTION_FILE = "collection.json"

def get_random_card(rarity=None, is_foil=False, set_code=None):
    """Fetch a random card from Scryfall by rarity and set."""
    time.sleep(0.1)  # Respect Scryfall rate limits

    query_parts = ["is:booster", "game:paper"]
    if set_code:
        query_parts.append(f"s:{set_code}")
    if is_foil:
        query_parts.append("is:foil")
    elif rarity:
        query_parts.append(f"r:{rarity}")

    query = " ".join(query_parts)
    url = f"https://api.scryfall.com/cards/random?q={query}"

    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Error fetching card: {response.status_code}")
        return None

def open_booster(set_code=None):
    """Simulate opening a booster pack."""
    print("\n📦 Opening booster pack...")
    pack = []

    # Rare (or mythic 1/8)
    for _ in range(PACK_STRUCTURE["rare"]):
        rarity = "mythic" if random.randint(1, 8) == 1 else "rare"
        card = get_random_card(rarity, set_code=set_code)
        if card:
            print(f"🟣 {card['name']} ({rarity})")
            card['is_foil'] = False
            pack.append(card)

    # Uncommons
    for _ in range(PACK_STRUCTURE["uncommon"]):
        card = get_random_card("uncommon", set_code=set_code)
        if card:
            print(f"🔶 {card['name']} (uncommon)")
            card['is_foil'] = False
            pack.append(card)

    # Chance for foil
    has_foil = random.randint(1, 3) == 1
    commons_needed = PACK_STRUCTURE["common"] - (1 if has_foil else 0)

    for _ in range(commons_needed):
        card = get_random_card("common", set_code=set_code)
        if card:
            print(f"⚪ {card['name']} (common)")
            card['is_foil'] = False
            pack.append(card)

    if has_foil:
        foil_card = get_random_card(is_foil=True, set_code=set_code)
        if foil_card:
            foil_card['is_foil'] = True
            print(f"✨ {foil_card['name']} (FOIL!)")
            pack.append(foil_card)

    return pack

def load_collection():
    """Load your collection from file, handle empty file gracefully."""
    if os.path.exists(COLLECTION_FILE):
        try:
            with open(COLLECTION_FILE, "r", encoding="utf-8") as f:
                data = f.read().strip()
                if not data:
                    return []
                return json.loads(data)
        except json.JSONDecodeError:
            return []
    else:
        return []

def save_to_collection(pack, collection):
    """Update collection with new cards."""
    for card in pack:
        name = card['name']
        set_code = card['set']
        number = card['collector_number']
        is_foil = card.get('is_foil', False)
        image_url = card.get('image_uris', {}).get('normal', '')

        # Check if card already exists
        found = False
        for entry in collection:
            if (entry["name"] == name and entry["set"] == set_code
                and entry["collector_number"] == number
                and entry.get("is_foil", False) == is_foil):
                entry["count"] += 1
                found = True
                break

        if not found:
            collection.append({
                "name": name,
                "set": set_code,
                "collector_number": number,
                "count": 1,
                "is_foil": is_foil,
                "image_url": image_url
            })

    with open(COLLECTION_FILE, "w", encoding="utf-8") as f:
        json.dump(collection, f, indent=2, ensure_ascii=False)
