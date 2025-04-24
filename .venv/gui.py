import streamlit as st
import booster
import time

# Initialize session state
if "pack" not in st.session_state:
    st.session_state.pack = []
if "current_card" not in st.session_state:
    st.session_state.current_card = 0
if "show_summary" not in st.session_state:
    st.session_state.show_summary = False

collection = booster.load_collection()

# Set the title of the app
st.title("🧙 MTG Booster Pack Simulator")

# === Open Pack Action ===
def open_pack():
    st.session_state.pack = booster.open_booster()  # Get the booster pack
    st.session_state.current_card = 0  # Reset the current card index
    st.session_state.show_summary = False  # Hide the summary initially

# === Proceed to next card ===
def next_card():
    st.session_state.current_card += 1
    if st.session_state.current_card >= len(st.session_state.pack):
        st.session_state.show_summary = True
        booster.save_to_collection(st.session_state.pack, collection)

# === Reset to Homepage ===
def reset_app():
    st.session_state.pack = []
    st.session_state.current_card = 0
    st.session_state.show_summary = False

# === Homepage ===
if not st.session_state.pack and not st.session_state.show_summary:
    # If no pack is opened yet, show the button to open the pack
    if st.button("🎁 Open Booster Pack"):
        open_pack()

# === Drawing Cards One-by-One ===
elif st.session_state.pack and not st.session_state.show_summary:
    # Show the card one by one as the user clicks "Next"
    card = st.session_state.pack[st.session_state.current_card]
    placeholder = st.empty()
    placeholder.text("✨ Drawing your card...")
    time.sleep(0.8)  # Simulate suspense

    card_name = card["name"]
    image_url = card.get("image_uris", {}).get("normal", None)
    foil = "✨ FOIL " if card.get("is_foil", False) else ""

    if image_url:
        placeholder.image(image_url, caption=f"{foil}{card_name}", width=250, use_container_width=False)
    else:
        placeholder.markdown(f"{foil}**{card_name}**")

    # Next card button
    st.button("🃏 Next", on_click=next_card)

# === Full Pack Summary View ===
elif st.session_state.show_summary:
    st.subheader("📦 Full Pack Contents")
    for card in st.session_state.pack:
        name = card["name"]
        image_url = card.get("image_uris", {}).get("normal", None)
        foil = "✨ FOIL " if card.get("is_foil", False) else ""
        if image_url:
            st.image(image_url, caption=f"{foil}{name}", width=250, use_container_width=False)
        else:
            st.markdown(f"{foil}**{name}**")

    # Button to reset and go back to the homepage
    st.button("🔁 Back to Homepage", on_click=reset_app)

# === View Collection ===
if st.checkbox("📚 Show My Collection"):
    st.subheader("📚 Your Collection")
    if not collection:
        st.info("No cards collected yet.")
    else:
        # Sort the collection alphabetically
        collection = sorted(collection, key=lambda x: x['name'])

        # Create a grid layout for displaying cards
        cols = st.columns(3)  # 3 cards per row
        for idx, card in enumerate(collection):
            with cols[idx % 3]:
                name = card["name"]
                foil = "✨" if card.get("is_foil", False) else ""
                count = card["count"]
                set_code = card["set"].upper()
                number = card["collector_number"]
                image_url = card.get("image_uris", {}).get("normal", None)

                # Display the image or card name
                if image_url:
                    st.image(image_url, caption=f"{foil} {name}", width=160, use_container_width=False)
                else:
                    st.markdown(f"{foil}**{name}**")

                # Display additional card info (count, set, number)
                st.markdown(f"**Count:** {count}")
                st.markdown(f"**Set:** {set_code} • #{number}")

# === Raw JSON Debug (optional) ===
with st.expander("🔧 See Raw Collection Data"):
    st.json(collection)
