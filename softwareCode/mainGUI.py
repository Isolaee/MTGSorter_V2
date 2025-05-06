from .mainGUILogic import MainLogic
from appJar import gui

### --------------------------------------------------------------------------------
### Global variables
### GUI

jarAppElement = gui("MTGDeckStats")
MainGUIClassElement = MainLogic(jarAppElement)  # Get the app instance from MainLogic
app = MainGUIClassElement.app  # Get the app instance from MainLogic

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
app.addButton(
    "Load Deck", lambda: MainGUIClassElement.goToPage("LoadDeckPage"), row=1, column=0
)
app.addButton(
    "Create Deck", lambda: MainGUIClassElement.goToPage("CreateDeckPage"), row=1, column=1
)
app.stopFrame()

### --------------------------------------------------------------------------------
# Load Deck Page
app.startFrame("LoadDeckPage", row=0, column=0)
app.addLabel("page2Label", "Load Deck")
app.addButton(
    "BackToWelcomeFromLoadDeck",
    lambda: MainGUIClassElement.goToPage("WelcomePage"),
    row=1,
    column=0,
)
app.setButton("BackToWelcomeFromLoadDeck", "Back")

# Menu
fileMenus = ["Close", "Help", "About"]
app.addMenuList("Menu", fileMenus, MainGUIClassElement.menuControls)

# Add widgets for format selection
formats = ["Commander", "Pioneer"]
app.addLabelOptionBox("Deck Format", formats, change=MainGUIClassElement.formatChanged)
app.addLabelEntry("Deck Name")
app.addLabelEntry("Commander Name")
# app.hideLabel("Commander Name")  # Hide by default
# app.hideEntry("Commander Name")   # hide and show is not working

## File Entry
app.addFileEntry("DeckUpload")

# Add Load button
app.addButton("Load", MainGUIClassElement.press)


### Left window
app.startPanedFrame("Data")
# Deck Preview window.
app.addListBox("DeckPreview")
app.setListBoxChangeFunction("DeckPreview", MainGUIClassElement.getSelectedItemFromDeck)

### Right window
app.startPanedFrame("Graphs")
# Graphs
app.addCanvas("GraphCanvas")
# # DataMenu
dataMenu = ["Mana Curve", "Card Distribution"]
app.addMenuList("Data", dataMenu, MainGUIClassElement.dataMenuControls)

app.stopPanedFrame()
app.stopPanedFrame()

# Add Saved Decks section
app.addLabel("SavedDecksLabel", "Saved Decks")
app.addListBox("SavedDecks", [])
app.setListBoxChangeFunction("SavedDecks", MainGUIClassElement.loadDeckByClick)
MainGUIClassElement.populateSavedDecks()

app.addButton("Save Deck", MainGUIClassElement.saveCurrentDeck)
app.stopFrame()

### --------------------------------------------------------------------------------
# Create Deck Page
app.startFrame("CreateDeckPage", row=0, column=0)
app.addLabel("page3Label", "Create Deck")
app.addButton(
    "BackToWelcomeFromCreateDeck",
    lambda: MainGUIClassElement.goToPage("WelcomePage"),
    row=1,
    column=0,
)
app.setButton("BackToWelcomeFromCreateDeck", "Back")

app.addLabel("FormatLabel", "Select Deck Format:", row=2, column=0)
app.addLabelOptionBox("Select Format", ["Commander", "Pioneer"], row=3, column=0)

app.startFrame("SearchContainer", row=3, column=0)
app.addLabel("SearchLabel", "Search for a card:", row=2, column=0)
app.addEntry("SearchField", row=3, column=0)  # Search field
app.addButton(
    "Search", lambda: MainGUIClassElement.searchCard(), row=3, column=1
)  # Search button
app.stopFrame()

app.addButton(
    "Search by properties",
    lambda: MainGUIClassElement.goToPage("SearchByAttributesPage"),
    row=5,
    column=0,
)

app.startPanedFrame("SearchResults", row=4, column=0)
app.addLabel("SearchResultsLabel", "Search Results")
app.addListBox("SearchResultsList", [])  # List box for search results
app.setListBoxChangeFunction(
    "SearchResultsList", MainGUIClassElement.updateSearchResultsList
)
app.startPanedFrame("DeckBuilding", row=4, column=0)
app.addLabel("DeckBuildingLabel", "Deck Building")
app.addListBox("DraftDeckList", [])
app.setListBoxChangeFunction("DraftDeckList", MainGUIClassElement.updateDraftDeckList)

app.startPanedFrame("Canvas", row=4, column=0)
app.addCanvas("ImageCanvas", row=4, column=0)  # Canvas for card image

# Create a frame for the stats and align it to the bottom
app.startFrame("StatsContainer", row=6, column=0, colspan=6)
app.setSticky("s")  # Stick the frame to the bottom
app.setStretch("both")  # Allow the frame to stretch

# Add fields inside the frame
app.addLabel("CardsLabel", "Cards:", row=0, column=0)
app.addLabel("CardsCount", "0", row=0, column=1)  # Placeholder for card count

app.addLabel("LandPercentageLabel", "Land-%:", row=0, column=2)
app.addLabel("LandPercentage", "0%", row=0, column=3)  # Placeholder for land percentage

app.addLabel("LandsLabel", "Lands:", row=0, column=4)
app.addLabel("LandsCount", "0", row=0, column=5)  # Placeholder for land count

app.stopFrame()

# Add a button to save the current draft deck
app.addButton(
    "Save Draft Deck", MainGUIClassElement.saveCurrentDeckCreateDeck, row=5, column=1
)

# Add format selection to the Create Deck Page
app.addLabel("FormatLabelCraeteDeck", "Select Deck Format:", row=2, column=0)
app.addLabelOptionBox("Select Format for Deck", ["Commander", "Pioneer"], row=3, column=0)

app.stopPanedFrame()
app.stopPanedFrame()
app.stopPanedFrame()
app.stopFrame()

### --------------------------------------------------------------------------------
# Search By Attributes Page
app.startFrame("SearchByAttributesPage", row=0, column=0)
app.addLabel("page4Label", "Search by Card Attributes")

# Add fields for card attributes
app.addLabelEntry("Name")
app.addLabelEntry("Mana Cost")
app.addLabelEntry("CMC")
app.addLabelEntry("Colors")
app.addLabelEntry("Color Identity")
app.addLabelEntry("Power")
app.addLabelEntry("Toughness")
app.addLabelEntry("Oracle Text")
app.addLabelEntry("Loyalty")
app.addLabelEntry("Type Line")
app.addLabelEntry("Card Type")
app.addLabelEntry("Artist")

# Add a button to perform the search
app.addButton("Search Attributes", lambda: MainGUIClassElement.searchCardsByAttributes())

# Add a button to go back to the Welcome Page
app.addButton(
    "BackToWelcomeFromAttributes", lambda: MainGUIClassElement.goToPage("WelcomePage")
)
app.setButton("BackToWelcomeFromAttributes", "Back")

app.stopFrame()

### --------------------------------------------------------------------------------
app.hideFrame("LoadDeckPage")  # Hide the LoadDeckPage by default
app.hideFrame("CreateDeckPage")  # Hide the CreateDeckPage by default
app.hideFrame("SearchByAttributesPage")  # Hide the SearchByAttributesPage by default

### Start the GUI application
app.go()
