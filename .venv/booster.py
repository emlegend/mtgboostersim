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

def get_random_card(rarity=None, is_foil=False):
    """Fetch a random card from Scryfall by rarity or any foil."""
    time.sleep(0.1)  # Respect rate limits

    if is_foil:
        query = "is:booster game:paper is:foil"
    elif rarity:
        query = f"r:{rarity} is:booster game:paper"

    url = f"https://api.scryfall.com/cards/random?q={query}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print("❌ Error fetching card:", response.status_code)
        return None

def open_booster():
    """Simulate opening a booster with foil and mythic logic."""
    print("\n📦 Opening booster pack...")
    pack = []

    # 1 in 8 chance to replace rare with mythic
    for _ in range(PACK_STRUCTURE["rare"]):
        rarity = "mythic" if random.randint(1, 8) == 1 else "rare"
        card = get_random_card(rarity)
        if card:
            print(f"🟣 {card['name']} ({rarity})")
            card['is_foil'] = False
            pack.append(card)

    # Add uncommons
    for _ in range(PACK_STRUCTURE["uncommon"]):
        card = get_random_card("uncommon")
        if card:
            print(f"🔶 {card['name']} (uncommon)")
            card['is_foil'] = False
            pack.append(card)

    # Determine if foil will replace a common
    has_foil = random.randint(1, 3) == 1  # ~33% chance

    commons_needed = PACK_STRUCTURE["common"] - (1 if has_foil else 0)

    # Add commons
    for _ in range(commons_needed):
        card = get_random_card("common")
        if card:
            print(f"⚪ {card['name']} (common)")
            card['is_foil'] = False
            pack.append(card)

    # Add foil (any rarity)
    if has_foil:
        foil_card = get_random_card(is_foil=True)
        if foil_card:
            foil_card['is_foil'] = True
            print(f"✨ {foil_card['name']} (FOIL!)")
            pack.append(foil_card)

    return pack

def load_collection():
    """Load your collection from a local file."""
    if os.path.exists(COLLECTION_FILE):
        with open(COLLECTION_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return []

def save_to_collection(pack, collection):
    """Update your collection with new pack cards."""
    for card in pack:
        name = card['name']
        set_code = card['set']
        number = card['collector_number']
        is_foil = card.get('is_foil', False)

        # Ensure we get the image URL safely
        image_url = card.get('image_uris', {}).get('normal', '')  # Get the normal image URI

        # Check if this exact printing is already in collection
        found = False
        for entry in collection:
            if (entry["name"] == name and
                    entry["set"] == set_code and
                    entry["collector_number"] == number and
                    entry.get("is_foil", False) == is_foil):
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
                "image_url": image_url  # Save the image URL in the collection
            })

    with open(COLLECTION_FILE, "w", encoding="utf-8") as f:
        json.dump(collection, f, indent=2, ensure_ascii=False)

def show_collection(collection):
    """Print out the user's card collection nicely."""
    print("\n📚 Your Collection:")
    for card in sorted(collection, key=lambda x: x['name']):
        foil_tag = " (FOIL)" if card.get("is_foil", False) else ""
        print(f"  {card['count']}x {card['name']}{foil_tag} ({card['set'].upper()} #{card['collector_number']})")
