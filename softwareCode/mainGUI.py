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


regex_engine_card = re.compile(r"(?P<amount>\d+)x?,?\s+(?P<name>.+)")
regex_engine_type = re.compile(r"^(?P<CardType>\w+?)\s*(-|—|$)\s*(?P<CreatureType>.+)?")
saved_decks_path = "./Decks"  # Path to the folder containing saved decks


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
        currentDeck = DeckParser.CreateEDHDeck(
            file_path,
            deck_name,
            format,
            commander_name,
            regex_engine_card,
            regex_engine_type,
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


def showCardIMG(clickedCard):
    """
    Show the card image in the DeckPreview list box.

    Args:
        card_name (str): The name of the card to show.
    """
    # selected_items = app.getListBox(clickedCard)
    # print(f"Selected items: {selected_items}")
    ### Find the card and show its image in grpah canvas
    # TODO: Implement the logic to show the card image in the graph canvas
    # Problem: Scryfall provides a static URL for the card image, but we need to find a way to display it in the app.


def loadDeckByClick(clickedDeck):
    """
    Load the deck by clicking on the list box.

    Args:
        clickedDeck (str): The name of the clicked deck.
    """
    selected_deck = app.getListBox(clickedDeck)
    if selected_deck:
        file_path = f"Decks/{selected_deck[0]}"  # Construct the full file path
        try:
            global currentDeck
            currentDeck = DeckParser.deserializeDeck(file_path)
            # Update the DeckPreview list box
            app.clearListBox("DeckPreview", callFunction=False)
            unPackCardNames()
        except Exception as e:
            print(f"Error loading deck: {e}")


def getSelectedItemFromDeck(clickedItem):
    """Get the selected item from the DeckPreview list box."""
    selected_item = app.getListBox(clickedItem)
    selected_card_name = selected_item[0].split("x ", 1)[
        -1
    ]  # Extract card name, it has 1, x, [, ], '

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
    Populate the Saved Decks list box with the contents of the saved decks folder
    and adjust its size to fit the content.
    """
    app.clearListBox("SavedDecks")
    saved_decks = list(
        DeckParser.read_folder_contents(saved_decks_path)
    )  # Convert generator to list
    app.addListItems("SavedDecks", saved_decks)

    # Dynamically adjust the size of the listbox
    num_rows = len(saved_decks)
    app.setListBoxRows("SavedDecks", num_rows if num_rows > 0 else 1)  # At least 1 row


## Save deck
def saveCurrentDeck():
    """Save the current deck to a file."""
    cond = None
    if currentDeck != cond:
        DeckParser.serializeDeck(currentDeck)
    populateSavedDecks()


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
# Page 1: Welcome Page
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
app.stopFrame()

### --------------------------------------------------------------------------------
app.hideFrame("LoadDeckPage")  # Hide the LoadDeckPage by default
app.hideFrame("CreateDeckPage")  # Hide the CreateDeckPage by default
