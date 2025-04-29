# Import GUI (JarAPp)
from appJar import gui
from .DeckParser import DeckParser
import re
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MaxNLocator
import requests
import os
from PIL import Image, ImageTk
import sqlite3


regex_engine_card = re.compile(r"(?P<amount>\d+)x?,?\s+(?P<name>.+)")
regex_engine_type = re.compile(r"^(?P<CardType>\w+?)\s*(-|—|$)\s*(?P<CreatureType>.+)?")
saved_decks_path = "./Decks"  # Path to the folder containing saved decks
draft_deck = []  # Placeholder for the draft deck


def press(btn):
    """
    Handle button presses.

    Args:
        btn (str): The button that was pressed.
    """
    global currentDeck

    if btn == "Load":
        # Get the file path from the file entry widget
        file_path = app.getEntry("DeckUpload")

        # Get the selected format from the drop-down menu
        format = app.getOptionBox("Deck Format")

        # Get the deck name from the entry field
        deck_name = app.getEntry(name="Deck Name")
        if not deck_name:
            deck_name = "My Deck"

        # Get the commander name if the format is Commander
        commander_name = None
        if format == "Commander":
            commander_name = app.getEntry("Commander Name")

        # Pass the regex engine to the DeckParser ### Testing CreateEDHDeck
        currentDeck = DeckParser.CreateEDHDeckFromDB(
            file_path,
            deck_name,
            format,
            commander_name,
            regex_engine_card,
            # regex_engine_type,
        )

        # Update the DeckPreview list box
        app.clearListBox("DeckPreview", callFunction=False)
        app.addListItem("DeckPreview", unPackCardNames())


def unPackCardNames():
    deck = currentDeck.getCardNamesAndAmounts()
    for card_name, amount in deck.items():
        app.addListItem("DeckPreview", f"{amount}x {card_name}")


def formatChanged():
    """Show or hide the Commander Name field based on the selected format."""
    format = app.getOptionBox("Deck Format")
    if format == "Commander":
        app.showLabel("Commander Name")
        app.showEntry("Commander Name")
    else:
        app.hideLabel("Commander Name")
        app.hideEntry("Commander Name")


def dataMenuControls(item):
    """
    DataMenuControl function

    Args:
        Item that was clicked
    Returns:
        Nothing.
    """
    if item == "Type Search":
        pass  # Implement type search functionality here
    elif item == "Mana Curve":
        data = currentDeck.getHistogramData("CMC")
        updateGraphCanvas(data)
    elif item == "Permanents":
        pass  # Implement permanents functionality here
    elif item == "Spells":
        pass  # Implement spells functionality here
    elif item == "Card Distribution":
        data = currentDeck.getHistogramData("CardType")
        updateGraphCanvas(data)


def updateGraphCanvas(data):
    """
    Update the GraphCanvas with a graph based on the provided data.

    Args:
        data (dict): A dictionary containing the data for the graph.
    """
    # Get the tkinter Canvas object from appJar
    canvas = app.getCanvas("GraphCanvas")

    # Clear the canvas before adding a new graph
    canvas.delete("all")

    # Create a Matplotlib figure
    fig, ax = plt.subplots(figsize=(5, 4))

    # Plot the data
    ax.bar(data.keys(), data.values(), color="skyblue")
    ax.set_title("Card Data")
    ax.set_xlabel("Categories")
    ax.set_ylabel("Counts")

    # Ensure Y-axis ticks are whole numbers
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    # Embed the figure into the AppJar canvas
    canvas_widget = FigureCanvasTkAgg(fig, canvas)
    canvas_widget.draw()
    canvas_widget.get_tk_widget().pack()


# Start GUI func
def startGUI():
    """
    Start the GUI application.

    Args:
        regex_engine: The compiled regex engine to be used in the app.
    """
    app.go()


def menuControls(item):
    """
    MenuControl function

    Args:
        Item that was clicked
    Returns:
        Nothing.
    """
    if item == "Close":
        app.stop()


def loadDeckByClick(clickedDeck):
    """
    Load the deck by clicking on the list box.

    Args:
        clickedDeck (str): The name of the clicked deck.
    """
    selected_deck = app.getListBox(clickedDeck)
    if selected_deck:
        file_path = selected_deck[0]  # Construct the full file path
        try:
            global currentDeck
            currentDeck = DeckParser.loadDeckFromDB(file_path)
            # Update the DeckPreview list box
            app.clearListBox("DeckPreview", callFunction=False)
            unPackCardNames()
        except Exception as e:
            print(f"Error loading deck: {e}")


def getSelectedItemFromListBox(clickedItem):
    """
    Get the selected item from the list box.

    Args:
        clickedItem (str): The name of the clicked item.
    Returns:

    """
    selected_item = app.getListBox(clickedItem)
    if selected_item:
        selected_card_name = selected_item[0].split("x ", 1)[-1]
        return selected_card_name
    return None


def showCardImage(card_name, canvas):
    """
    Show the image of the selected card to Selected Canvas.

    Args:
        card_name (str): The name of the card.
        canvas (tkinter.Canvas): The canvas to display the image on.
    Returns:
        None
    """

    for i in draft_deck:
        if i.getName() == card_name:
            draft_card = i
            image_url = draft_card.getImage()
            break

    response = requests.get(image_url)

    if response.status_code == 200:
        # Construct the path to the TempImg folder inside softwareCode
        temp_img_dir = os.path.join(os.path.dirname(__file__), "TempImg")
        os.makedirs(temp_img_dir, exist_ok=True)  # Create the folder if it doesn't exist

        # Save the image as a temporary .JPG file
        jpg_image_path = os.path.join(temp_img_dir, "selected_card.jpg")
        with open(jpg_image_path, "wb") as file:
            file.write(response.content)

        # Get the tkinter Canvas object from appJar
        canvas = app.getCanvas("ImageCanvas")

        # Get the canvas size
        canvas.update_idletasks()  # Ensure the canvas size is updated
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()

        # Convert the .JPG image to a format compatible with tkinter
        with Image.open(jpg_image_path) as img:
            # Calculate the new width to maintain the aspect ratio
            aspect_ratio = img.width / img.height
            new_height = canvas_height
            new_width = int(new_height * aspect_ratio)

            # Resize the image
            img = img.resize((new_width, new_height))
            tk_image = ImageTk.PhotoImage(img)

        # Clear the canvas before adding a new image
        canvas.delete("all")

        # Add the image to the canvas, centered
        canvas.create_image(
            canvas_width // 2, canvas_height // 2, image=tk_image, anchor="center"
        )
        canvas.image = tk_image  # Keep a reference to avoid garbage collection
    else:
        print(
            f"Failed to retrieve image from {image_url}. Status code: {response.status_code}"
        )


def updateSearchResultsList():
    """
    Update the SearchResultsList with the found card.

    Args:
        None
    Returns:
        None
    """
    selected_card = getSelectedItemFromListBox("SearchResultsList")
    if selected_card:
        app.addListItem("DraftDeckList", selected_card)
        showCardImage(selected_card, "ImageCanvas")


def getSelectedItemFromDeck(clickedItem):
    """Get the selected item from the DeckPreview list box."""
    selected_item = app.getListBox(clickedItem)
    if not selected_item:  # Check if the list box is empty
        print(f"No item selected in {clickedItem}.")
        return

    selected_card_name = selected_item[0].split("x ", 1)[-1]  # Extract card name

    selected_card = None
    for card in currentDeck.cards:
        if card.getName() == selected_card_name:
            selected_card = card
            break

    # Just in case the card is not found in the deck. This should not happen.
    if not selected_card:
        print(f"Card '{selected_card_name}' not found in the deck.")
        return

    image_url = selected_card.getImage()
    response = requests.get(image_url)

    if response.status_code == 200:
        # Construct the path to the TempImg folder inside softwareCode
        temp_img_dir = os.path.join(os.path.dirname(__file__), "TempImg")
        os.makedirs(temp_img_dir, exist_ok=True)  # Create the folder if it doesn't exist

        # Save the image as a temporary .JPG file
        jpg_image_path = os.path.join(temp_img_dir, "selected_card.jpg")
        with open(jpg_image_path, "wb") as file:
            file.write(response.content)

        # Get the tkinter Canvas object from appJar
        canvas = app.getCanvas("GraphCanvas")

        # Get the canvas size
        canvas.update_idletasks()  # Ensure the canvas size is updated
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()

        # Convert the .JPG image to a format compatible with tkinter
        with Image.open(jpg_image_path) as img:
            # Calculate the new width to maintain the aspect ratio
            aspect_ratio = img.width / img.height
            new_height = canvas_height
            new_width = int(new_height * aspect_ratio)

            # Resize the image
            img = img.resize((new_width, new_height))
            tk_image = ImageTk.PhotoImage(img)

        # Clear the canvas before adding a new image
        canvas.delete("all")

        # Add the image to the canvas, centered
        canvas.create_image(
            canvas_width // 2, canvas_height // 2, image=tk_image, anchor="center"
        )
        canvas.image = tk_image  # Keep a reference to avoid garbage collection
    else:
        print(
            f"Failed to retrieve image from {image_url}. Status code: {response.status_code}"
        )


def populateSavedDecks():
    """
    Populate the Saved Decks list box with the names of all decks in the database.
    """
    app.clearListBox("SavedDecks")  # Clear the list box first

    # Query the database for all saved decks
    conn = sqlite3.connect("mtg_card_db.db")
    cursor = conn.cursor()

    try:
        # Assuming there is a table `decks` with a column `name` for deck names
        cursor.execute("SELECT name FROM decks")
        saved_decks = [row[0] for row in cursor.fetchall()]  # Fetch all deck names

        # Add the deck names to the list box
        app.addListItems("SavedDecks", saved_decks)

        # Dynamically adjust the size of the list box
        num_rows = len(saved_decks)
        app.setListBoxRows(
            "SavedDecks", num_rows if num_rows > 0 else 1
        )  # At least 1 row
    except sqlite3.Error as e:
        print(f"Error querying database: {e}")
    finally:
        conn.close()  # Ensure the database connection is closed


## Save deck
def saveCurrentDeck():
    """Save the current deck to a file."""
    global currentDeck
    cond = None
    if currentDeck != cond:
        DeckParser.saveDeckToDB(currentDeck)
    populateSavedDecks()


def searchCard():
    """
    Search for a card by its name.
    """
    card_name = app.getEntry("SearchField")
    card = DeckParser.CreateSingleMTGCardFromDB(card_name)
    draft_deck.append(card)
    app.clearListBox("SearchResultsList")
    app.addListItem("SearchResultsList", card.getName())


def updateDraftDeckList():
    item = getSelectedItemFromListBox("DraftDeckList")
    showCardImage(item, "ImageCanvas")


def goToPage(page):
    """Switch to the specified page."""
    app.hideFrame("WelcomePage")
    app.hideFrame("LoadDeckPage")
    app.hideFrame("CreateDeckPage")
    app.showFrame(page)


### --------------------------------------------------------------------------------
### Global variables
### GUI
app = gui("MTGDeckStats")
app.setResizable(canResize=True)
# Stickiness and strechiness
app.setSticky("new")  # North, East, West
app.setStretch("column")
# add & configure widgets - widgets get a name, to help referencing them later
app.addLabel("title", "Welcome to MTGDeckStats")
app.setBg("lightblue")
app.setFont(20)

### --------------------------------------------------------------------------------
# Welcome Page
app.startFrame("WelcomePage", row=0, column=0)
app.addLabel("welcomeLabel", "Welcome to the MTGDeckStats", colspan=2)
app.addButton("Load Deck", lambda: goToPage("LoadDeckPage"), row=1, column=0)
app.addButton("Create Deck", lambda: goToPage("CreateDeckPage"), row=1, column=1)
app.stopFrame()

### --------------------------------------------------------------------------------
# Load Deck Page
app.startFrame("LoadDeckPage", row=0, column=0)
app.addLabel("page2Label", "Load Deck")
app.addButton(
    "BackToWelcomeFromLoadDeck", lambda: goToPage("WelcomePage"), row=1, column=0
)
app.setButton("BackToWelcomeFromLoadDeck", "Back")

# Menu
fileMenus = ["Close"]
app.addMenuList("Menu", fileMenus, menuControls)

# Add widgets for format selection
formats = ["Commander", "Pioneer"]
app.addLabelOptionBox("Deck Format", formats, change=formatChanged)
app.addLabelEntry("Deck Name")
app.addLabelEntry("Commander Name")
# app.hideLabel("Commander Name")  # Hide by default
# app.hideEntry("Commander Name")   # hide and show is not working

## File Entry
app.addFileEntry("DeckUpload")

# Add Load button
app.addButton("Load", press)


### Left window
app.startPanedFrame("Data")
# Deck Preview window.
app.addListBox("DeckPreview")
app.setListBoxChangeFunction("DeckPreview", getSelectedItemFromDeck)

### Right window
app.startPanedFrame("Graphs")
# Graphs
app.addCanvas("GraphCanvas")
# # DataMenu
dataMenu = ["Mana Curve", "Card Distribution"]
app.addMenuList("Data", dataMenu, dataMenuControls)

app.stopPanedFrame()
app.stopPanedFrame()

# Add Saved Decks section
app.addLabel("SavedDecksLabel", "Saved Decks")
app.addListBox("SavedDecks", [])
app.setListBoxChangeFunction("SavedDecks", loadDeckByClick)
populateSavedDecks()

app.addButton("Save Deck", saveCurrentDeck)
app.stopFrame()

### --------------------------------------------------------------------------------
# Create Deck Page
app.startFrame("CreateDeckPage", row=0, column=0)
app.addLabel("page3Label", "Create Deck")
app.addButton(
    "BackToWelcomeFromCreateDeck", lambda: goToPage("WelcomePage"), row=1, column=0
)
app.setButton("BackToWelcomeFromCreateDeck", "Back")

app.addLabel("FormatLabel", "Select Deck Format:", row=2, column=0)
app.addLabelOptionBox("Select Format", ["Commander", "Pioneer"], row=3, column=0)


app.addLabel("SearchLabel", "Search for a card:", row=2, column=0)
app.addEntry("SearchField", row=3, column=0)  # Search field
app.addButton("Search", lambda: searchCard(), row=3, column=1)  # Search button

app.startPanedFrame("SearchResults", row=4, column=0)
app.addLabel("SearchResultsLabel", "Search Results")
app.addListBox("SearchResultsList", [])  # List box for search results
app.setListBoxChangeFunction("SearchResultsList", updateSearchResultsList)
app.startPanedFrame("DeckBuilding", row=4, column=0)
app.addLabel("DeckBuildingLabel", "Deck Building")
app.addListBox("DraftDeckList", [])
app.setListBoxChangeFunction("DraftDeckList", updateDraftDeckList)

app.startPanedFrame("Canvas", row=4, column=0)
app.addCanvas("ImageCanvas", row=4, column=0)  # Canvas for card image

app.stopPanedFrame()
app.stopPanedFrame()
app.stopPanedFrame()
app.stopFrame()

### --------------------------------------------------------------------------------
app.hideFrame("LoadDeckPage")  # Hide the LoadDeckPage by default
app.hideFrame("CreateDeckPage")  # Hide the CreateDeckPage by default
