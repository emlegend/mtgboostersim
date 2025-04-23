import streamlit as st
import booster  # Corrected import statement
import json
import os

# Load collection
collection = booster.load_collection()

# Title
st.title("🧙 MTG Booster Pack Simulator")

# === Booster Opening ===
if st.button("🎁 Open a Booster"):
    pack = booster.open_booster()  # Using booster (not booster_sim)
    booster.save_to_collection(pack, collection)

    st.subheader("📦 You opened:")
    for card in pack:
        foil = "✨ FOIL " if card.get("is_foil", False) else ""
        rarity = card["rarity"].capitalize()
        st.markdown(f"- {foil}**{card['name']}** ({rarity})")

# === View Collection ===
if st.checkbox("📚 Show My Collection"):
    st.subheader("📚 Your Collection")
    if not collection:
        st.info("No cards collected yet.")
    else:
        for card in sorted(collection, key=lambda x: x['name']):
            foil = "✨ FOIL " if card.get("is_foil", False) else ""
            st.markdown(f"- {card['count']}x {foil}**{card['name']}** ({card['set'].upper()} #{card['collector_number']})")

# === Debug / Raw Data (optional)
with st.expander("🔧 See Raw Collection Data"):
    st.json(collection)
