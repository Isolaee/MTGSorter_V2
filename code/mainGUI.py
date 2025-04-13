# Import GUI (JarAPp)
from appJar import gui
from DeckParser import DeckParser
import re
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MaxNLocator

# import filefun
# import matplotlib.pyplot as plt
# import numpy as np
# From here below are for histogram
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from matplotlib.figure import Figure

regex_engine = re.compile(r"(?P<amount>\d+)x?,?\s+(?P<name>.+)")


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

        # Pass the regex engine to the DeckParser
        currentDeck = DeckParser.CreateDeck(
            file_path, deck_name, format, commander_name, regex_engine
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
        pass  # Implement card distribution functionality here


def updateGraphCanvas(data):
    """
    Update the GraphCanvas with a graph based on the provided data.

    Args:
        data (dict): A dictionary containing the data for the graph.
    """

    # Ensure keys and values are integers
    data = {int(key): int(value) for key, value in data.items()}

    # Create a Matplotlib figure
    fig, ax = plt.subplots(figsize=(5, 4))

    # Example: Create a bar chart from the data
    ax.bar(data.keys(), data.values(), color="skyblue")
    ax.set_title("Card Data")
    ax.set_xlabel("Categories")
    ax.set_ylabel("Counts")

    # Ensure Y-axis ticks are whole numbers
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    # Embed the figure into the AppJar canvas
    canvas = FigureCanvasTkAgg(fig, app.getCanvas("GraphCanvas"))
    canvas.draw()
    canvas.get_tk_widget().pack()


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


### GUI
app = gui("MTGDeckStats", "1000x1000")
# Stickiness and strechiness
app.setSticky("new")  # North, East, West
app.setStretch("column")
# add & configure widgets - widgets get a name, to help referencing them later
app.addLabel("title", "Welcome to MTGDeckStats")
app.setBg("lightblue")
app.setFont(20)

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

### Right window
app.startPanedFrame("Graphs")
# Graphs
app.addCanvas("GraphCanvas")
# # DataMenu
dataMenu = ["Type Search", "Mana Curve", "Permanents", "Spells", "Card Distribution"]
app.addMenuList("Data", dataMenu, dataMenuControls)

app.stopPanedFrame()
app.stopPanedFrame()
