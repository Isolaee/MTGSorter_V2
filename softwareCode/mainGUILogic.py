from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MaxNLocator
from PIL import ImageTk, Image
from .DBQueries import DBQueries
from .EDHDeck import EDHDeck
from .PioneerDeck import PioneerDeck


import matplotlib.pyplot as plt
import requests
import os
import sqlite3
import re


class MainLogic:
    def __init__(self, app_instance):
        self.app = app_instance
        self.graph_canvas_widget = None

    # Regex patterns for parsing card names and types
    regex_engine_card = re.compile(r"(?P<amount>\d+)x?,?\s+(?P<name>.+)")
    regex_engine_type = re.compile(
        r"^(?P<CardType>\w+?)\s*(-|—|$)\s*(?P<CreatureType>.+)?"
    )

    # Saved decks parh for depricated saveDeck function
    saved_decks_path = "./Decks"  # Path to the folder containing saved decks

    # Global variables for lists or deck objects
    current_deck = None  # Variable to store the current deck object
    createDeckCardList = []  # List to store card names for the deck creation process
    searchResultsLists = []  # List to store search results for cards

    ### ----------------------------------------------------------------------------------

    # press method for the app buttons.
    # Currently, it handles the "Load" button press event.
    def press(self, btn):
        """
        Handle button presses.

        Args:
            btn (str): The button that was pressed.
        """

        if btn == "Load":
            # Get the file path from the file entry widget
            file_path = self.app.getEntry("DeckUpload")

            # Get the selected format from the drop-down menu
            format = self.app.getOptionBox("Deck Format")

            # Get the deck name from the entry field
            deck_name = self.app.getEntry(name="Deck Name")
            if not deck_name:
                deck_name = "My Deck"

            # Get the commander name if the format is Commander
            commander_name = None
            if format == "Commander":
                commander_name = self.app.getEntry("Commander Name")

            # Pass the regex engine to the DeckParser
            self.current_deck = DBQueries.CreateEDHDeckFromDB(
                file_path,
                deck_name,
                format,
                commander_name,
                self.regex_engine_card,
                # regex_engine_type,
            )

            # Update the DeckPreview list box
            self.app.clearListBox("DeckPreview", callFunction=False)
            self.app.addListItem("DeckPreview", self.unPackCardNames())

    # MenuControl function
    def menuControls(self, item):
        """
        MenuControl function

        Args:
            Item that was clicked
        Returns:
            Nothing.
        """
        if item == "Close":
            self.app.stop()
        elif item == "Help":
            self.app.infoBox("Help", "This is a help message.")
        elif item == "About":
            self.app.infoBox("About", "This is an about message.")

    # DataMenuControl function
    def dataMenuControls(self, item):
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
            data = self.current_deck.getHistogramData("CMC")
            self.updateGraphCanvas(data, "GraphCanvas")
        elif item == "Permanents":
            pass  # Implement permanents functionality here
        elif item == "Spells":
            pass  # Implement spells functionality here
        elif item == "Card Distribution":
            data = self.current_deck.getHistogramData("CardType")
            self.updateGraphCanvas(data, "GraphCanvas")

    def goToPage(self, page):
        """Switch to the specified page."""
        self.app.hideFrame("WelcomePage")
        self.app.hideFrame("LoadDeckPage")
        self.app.hideFrame("CreateDeckPage")
        self.app.hideFrame("SearchByAttributesPage")
        self.app.showFrame(page)

    ### ----------------------------------------------------------------------------------
    # Shared Methods
    # Unpack the card names and amounts from the current deck
    def unPackCardNames(self):
        deck = self.current_deck.getCardNamesAndAmounts()
        for card_name, amount in deck.items():
            self.app.addListItem("DeckPreview", f"{amount}x {card_name}")

    # Update the GraphCanvas with a graph based on the provided data
    def updateGraphCanvas(self, data, canvasName):
        """
        Update the GraphCanvas with a graph based on the provided data.
        """
        frame = self.app.getFrame(canvasName)

        # Destroy the previous FigureCanvasTkAgg widget if it exists
        if hasattr(self, "graph_canvas_widget") and self.graph_canvas_widget is not None:
            self.graph_canvas_widget.get_tk_widget().destroy()
            self.graph_canvas_widget = None

        # Create a Matplotlib figure
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.bar(data.keys(), data.values(), color="skyblue")
        ax.set_title("Card Data")
        ax.set_xlabel("Categories")
        ax.set_ylabel("Counts")
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))

        # Embed the figure into the AppJar frame
        self.graph_canvas_widget = FigureCanvasTkAgg(fig, frame)
        self.graph_canvas_widget.draw()
        self.graph_canvas_widget.get_tk_widget().pack(fill="both", expand=True)

    def showCardImage(self, card, canvasName):
        """
        Show the image of the selected card to Selected Canvas.
        """
        canvas = self.app.getCanvas(canvasName)
        canvas.delete("all")

        image_url = card.getImage()
        response = requests.get(image_url)
        if response.status_code == 200:
            temp_img_dir = os.path.join(os.path.dirname(__file__), "TempImg")
            os.makedirs(temp_img_dir, exist_ok=True)
            jpg_image_path = os.path.join(temp_img_dir, "selected_card.jpg")
            with open(jpg_image_path, "wb") as file:
                file.write(response.content)

            canvas.update_idletasks()
            canvas_width = canvas.winfo_width()
            canvas_height = canvas.winfo_height()

            with Image.open(jpg_image_path) as img:
                aspect_ratio = img.width / img.height
                new_height = canvas_height
                new_width = int(new_height * aspect_ratio)
                img = img.resize((new_width, new_height))
                tk_image = ImageTk.PhotoImage(img)

            canvas.create_image(
                canvas_width // 2, canvas_height // 2, image=tk_image, anchor="center"
            )
            canvas.image = tk_image
        else:
            print(
                f"Failed to retrieve image from {image_url}. Status code: {response.status_code}"
            )

    def populateSavedDecks(self):
        """
        Populate the Saved Decks list box with the names of all decks in the database.
        """
        self.app.clearListBox("SavedDecks")  # Clear the list box first

        # Query the database for all saved decks
        conn = sqlite3.connect("mtg_card_db.db")
        cursor = conn.cursor()

        try:
            # Assuming there is a table `decks` with a column `name` for deck names
            cursor.execute("SELECT name FROM decks")
            saved_decks = [row[0] for row in cursor.fetchall()]  # Fetch all deck names

            # Add the deck names to the list box
            self.app.addListItems("SavedDecks", saved_decks)

            # Dynamically adjust the size of the list box
            num_rows = len(saved_decks)
            self.app.setListBoxRows(
                "SavedDecks", num_rows if num_rows > 0 else 1
            )  # At least 1 row
        except sqlite3.Error as e:
            print(f"Error querying database: {e}")
        finally:
            conn.close()  # Ensure the database connection is closed

    def getSelectedItemFromDeck(self, clickedItem):
        """Get the selected item from the DeckPreview list box."""
        selected_item = self.app.getListBox(clickedItem)
        if not selected_item:  # Check if the list box is empty
            print(f"No item selected in {clickedItem}.")
            return

        selected_card_name = selected_item[0].split("x ", 1)[-1]  # Extract card name

        selected_card = None
        for card in self.current_deck.cards:
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
            os.makedirs(
                temp_img_dir, exist_ok=True
            )  # Create the folder if it doesn't exist

            # Save the image as a temporary .JPG file
            jpg_image_path = os.path.join(temp_img_dir, "selected_card.jpg")
            with open(jpg_image_path, "wb") as file:
                file.write(response.content)

            # Get the tkinter Canvas object from appJar
            canvas = self.app.getCanvas("GraphCanvas")

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

    ### ----------------------------------------------------------------------------------
    # Load Deck
    def loadDeckByClick(self, clickedDeck):
        """
        Load the deck by clicking on the list box.

        Args:
            clickedDeck (str): The name of the clicked deck.
        """
        selected_deck = self.app.getListBox(clickedDeck)
        if selected_deck:
            file_path = selected_deck[0]  # Construct the full file path
            try:
                self.current_deck = DBQueries.loadDeckFromDB(file_path)
                # Update the DeckPreview list box
                self.app.clearListBox("DeckPreview", callFunction=False)
                self.unPackCardNames()
            except Exception as e:
                print(f"Error loading deck: {e}")

    def getSelectedItemFromListBox(self, clickedItem):
        """
        Get the selected item from the list box.

        Args:
            The field look from
        Returns:
            The selected item from the list box as a card object.

        """
        selected_item = self.app.getListBox(clickedItem)
        print(f"Selected item from {clickedItem}: {selected_item}")
        if selected_item:
            selected_card_name = selected_item[0].split("x ", 1)[-1]
            card = DBQueries.get_card_from_db(selected_card_name)
            return card[0] if card else None
        else:
            print(f"No item selected in {clickedItem}.")
        return None

    ### ----------------------------------------------------------------------------------
    # Create Deck
    def updateDeckStats(self):
        """
        Update the deck statistics: total cards, land percentage, and total lands.
        """
        total_cards = len(self.createDeckCardList)
        total_lands = sum(
            1 for card in self.createDeckCardList if "Land" in card.getCardType()
        )
        land_percentage = (total_lands / total_cards * 100) if total_cards > 0 else 0

        # Update the labels
        self.app.setLabel("CardsCount", str(total_cards))
        self.app.setLabel("LandPercentage", f"{land_percentage:.1f}%")
        self.app.setLabel("LandsCount", str(total_lands))

    def searchCardsByAttributes(self):
        """
        Search for cards based on multiple attributes and update the Create Deck Page.
        """
        # Collect values from the fields
        filters = {
            "name": self.app.getEntry("Name"),
            "manacost": self.app.getEntry("Mana Cost"),
            "cmc": self.app.getEntry("CMC"),
            "colors": self.app.getEntry("Colors"),
            "coloridentity": self.app.getEntry("Color Identity"),
            "power": self.app.getEntry("Power"),
            "toughness": self.app.getEntry("Toughness"),
            "oracletext": self.app.getEntry("Oracle Text"),
            "loyalty": self.app.getEntry("Loyalty"),
            "typeline": self.app.getEntry("Type Line"),
            "cardtype": self.app.getEntry("Card Type"),
            "artist": self.app.getEntry("Artist"),
        }

        # Remove empty filters
        filters = {key: value for key, value in filters.items() if value}

        # Modify the name filter to allow partial matches
        if "name" in filters:
            filters["name"] = f"%{filters['name']}%"  # Add wildcards for partial matching

        # Query the database
        matching_cards = DBQueries.queryCardsByProperties(filters)

        # Update the SearchResultsList on the Create Deck Page
        self.app.clearListBox("SearchResultsList")
        for card in matching_cards:
            self.searchResultsLists.append(card)
            self.app.addListItem("SearchResultsList", card.getName())

        # Navigate back to the Create Deck Page
        self.goToPage("CreateDeckPage")

    def updateDraftDeckList(self):
        item = self.getSelectedItemFromListBox("DraftDeckList")
        self.showCardImage(item, "ImageCanvas")

    def searchCard(self):
        """
        Search for a card by its name, allowing partial matches and handling multiple results.
        """
        card_name = self.app.getEntry("SearchField")
        if not card_name:
            print("Please enter a card name to search.")
            return

        # Get all matching cards from the database
        matching_cards = DBQueries.get_card_from_db(card_name)

        # Clear the search results list box
        self.app.clearListBox("SearchResultsList")

        if matching_cards:
            # Add matching card names to the search results list box
            for card in matching_cards:
                self.searchResultsLists.append(card)  # Add the card to the draft deck
                self.app.addListItem("SearchResultsList", card.getName())
        else:
            self.app.addListItem("SearchResultsList", "No matches found.")

    def saveCurrentDeckCreateDeck(self):
        """Save the current draft deck to a file."""

        format = self.app.getOptionBox("Select Format")
        # commander = app.getEntry("Commander Name")  # Get the commander name from the entry field
        commander = "Tajic, Blade of the Legion"  # Placeholder for the commander name
        deck_name = "My Draft Deck"  # Placeholder for the deck name
        commanderCard = DBQueries.get_card_from_db(commander)

        if format == "Commander":
            self.current_deck = EDHDeck(
                name=deck_name,
                format="commander",
                cards=self.createDeckCardList,
                commander=commanderCard[0],
            )
        elif format == "Pioneer":
            self.current_deck = PioneerDeck(
                name=deck_name,
                format="pioneer",
                cards=self.createDeckCardList,
            )
        else:
            print("Invalid format selected. Please choose either Commander or Pioneer.")
            return  # Exit the function if the format is invalid

        self.saveCurrentDeck()
        self.populateSavedDecks()  # Refresh the saved decks list after saving

    def updateSearchResultsList(self):
        """Update the search results list when a card is selected."""
        card = self.getSelectedItemFromListBox("SearchResultsList")
        if card:
            self.createDeckCardList.append(card)
            self.app.addListItem("DraftDeckList", card.getName())
            self.updateDeckStats()  # Update the deck stats

    ### ----------------------------------------------------------------------------------
    # Not sure section
    ## Save deck
    def saveCurrentDeck(self):
        """Save the current deck to a file."""
        cond = None

        if self.current_deck != cond:
            DBQueries.saveDeckToDB(self.current_deck)
        self.populateSavedDecks()

    def formatChanged(self):
        """Show or hide the Commander Name field based on the selected format."""
        format = self.app.getOptionBox("Deck Format")
        if format == "Commander":
            self.app.showLabel("Commander Name")
            self.app.showEntry("Commander Name")
        else:
            self.app.hideLabel("Commander Name")
            self.app.hideEntry("Commander Name")
