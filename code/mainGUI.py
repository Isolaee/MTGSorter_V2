# Import GUI (JarAPp)
from appJar import gui

# import filefun
# import matplotlib.pyplot as plt
# import numpy as np
# From here below are for histogram
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from matplotlib.figure import Figure


def press(btn):
    """
    Load Button function

    Args:
        Button title
    Returns:
        Nothing.
    """


# Start GUI func
def startGUI():
    """
    Starts GUI (JarApp)

    Args:
        None
    returns:
        Nothing.
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
app = gui("MTGDeckStats", "800x600")
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


## File Entry
app.addFileEntry("DeckUpload")

# Add Load button
app.addButton("Load", press)

# Deck Preview window.
app.addListBox("DeckPreview")

# Graphs
app.addCanvas("GraphCanvas")
