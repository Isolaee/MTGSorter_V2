# Import GUI (JarAPp)
from appJar import gui
from DeckParser import DeckParser
import re

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
        app.addListItem("DeckPreview", currentDeck.getAllCardNames())


def formatChanged():
    """Show or hide the Commander Name field based on the selected format."""
    format = app.getOptionBox("Deck Format")
    if format == "Commander":
        app.showLabel("Commander Name")
        app.showEntry("Commander Name")
    else:
        app.hideLabel("Commander Name")
        app.hideEntry("Commander Name")


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
app = gui("MTG Sorter", "800x600")
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

# Deck Preview window.
app.addListBox("DeckPreview")

# Graphs
app.addCanvas("GraphCanvas")
