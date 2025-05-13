Sure! Here's a clean and detailed `README.md` for your app:

---

# 🧙 MTG Booster Pack Simulator

Welcome to the **MTG Booster Pack Simulator**! This app allows you to simulate opening Magic: The Gathering booster packs. You can draw random cards of various rarities (Common, Uncommon, Rare, and Mythic), collect them, and view your collection at any time.

## Features

- **Simulate Booster Packs**: Open random packs and draw cards of different rarities.
- **Foil Cards**: You may draw foil versions of cards in addition to regular ones.
- **Collection Tracking**: Keep track of all your collected cards, including foil and non-foil versions.
- **Streamlined UI**: A clean interface built using [Streamlit](https://streamlit.io/) to make it easy to interact with the app.
- **Customizable**: The app supports easy modifications and improvements for expanding functionality (e.g., adding more sets).

## Requirements

Before running the app, ensure you have Python 3.7+ and the necessary dependencies installed.

### Install Python Dependencies

To get started, you'll need to install the required dependencies.

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/mtg-booster-pack-simulator.git
   cd mtg-booster-pack-simulator
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```

4. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

### Install Additional Dependencies

If you're using the app to interact with external APIs (like Scryfall), ensure that you have an internet connection.

## Running the App

Once you have all the dependencies set up, you can run the app locally using the following steps.

1. In the terminal, navigate to the directory where the app is located.

2. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

3. After a few moments, the app will start, and it will open in your default web browser. The interface will show up where you can start interacting with the booster packs!

## How to Use the App

### 1. **Opening a Booster Pack**
Click the "🎁 Open Booster Pack" button to simulate opening a booster pack. The app will display random cards, starting with the rarest ones, and give you a chance to draw foil versions.

### 2. **Viewing Cards**
Click "🃏 Next" to reveal the next card in the pack. The app will simulate opening the pack one card at a time with suspenseful animation.

### 3. **Full Pack Summary**
Once you've revealed all the cards in the booster pack, you'll have the option to view a summary of the entire pack's contents.

### 4. **Collection**
You can view your collection by checking the "📚 Show My Collection" checkbox. This will display all the cards you've collected so far, along with their count, set, and image.

### 5. **Collection Management**
The app will automatically save your collection after each pack is opened. Your collection is saved in a local JSON file (`collection.json`), so the next time you launch the app, it will load the cards you've already collected.

## File Structure

- `app.py` - The main file that runs the Streamlit app and handles the app's logic.
- `booster.py` - Contains the functions that simulate opening booster packs and handling the collection.
- `collection.json` - Stores your card collection in JSON format (this file is automatically created and updated as you collect cards).

## Customization

The app can be customized in several ways:

- **Rarity Configurations**: Modify the `PACK_STRUCTURE` dictionary in `booster.py` to adjust how many cards of each rarity are included in the booster packs.
- **Card Data Source**: Currently, the app fetches cards from Scryfall via their API. You can modify this to use other sources if needed.
- **UI Customization**: Streamlit offers a variety of customization options for the UI. You can adjust the appearance, layout, and elements to your liking.

## Troubleshooting

If you encounter any issues, consider the following:

- Ensure that your Python environment is correctly set up and that all dependencies are installed.
- Make sure your `collection.json` file is not corrupted. If needed, you can delete it, and the app will create a fresh one.
- If the app crashes when trying to fetch card data, check the API connection or try again later, as it may be a temporary issue with the Scryfall API.

## Contributing

If you'd like to contribute to this project, feel free to fork the repository and submit a pull request. You can help by:

- Fixing bugs
- Adding new features
- Improving the UI
- Writing better documentation

## License

This project is open source and available under the [MIT License](LICENSE).

