from .EDHDeck import EDHDeck
from .MTGCard import MTGCard
from .DeckParser import DeckParser
import json
import sqlite3


class DBQueries:
    """
    A class to handle database queries for Magic: The Gathering cards and decks.
    """

    @staticmethod
    def queryCardsByProperties(properties: dict) -> list:
        """
        Query the card database based on given properties.

        Args:
            properties (dict): A dictionary of properties to filter cards by.
                            Example: {"colors": "red", "cmc": 3}

        Returns:
            list: A list of dictionaries representing the cards that match the query.
        """
        conn = sqlite3.connect("mtg_card_db.db")
        cursor = conn.cursor()

        # Base query
        query = "SELECT * FROM cards"
        conditions = []
        values = []

        # Dynamically build the WHERE clause based on the properties
        for key, value in properties.items():
            if value:  # Only include non-empty filters
                if isinstance(value, (list, tuple)):
                    # Handle lists (e.g., colors IN ('red', 'blue'))
                    placeholders = ", ".join("?" for _ in value)
                    conditions.append(f"{key} IN ({placeholders})")
                    values.extend(value)
                else:
                    # Handle single values (e.g., cmc = ?)
                    conditions.append(f"{key} = ?")
                    values.append(value)

        # Add conditions to the query if any exist
        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        try:
            # Execute the query
            cursor.execute(query, values)
            rows = cursor.fetchall()

            # Map the rows to dictionaries
            columns = [
                "name",
                "manacost",
                "cmc",
                "colors",
                "coloridentity",
                "power",
                "toughness",
                "oracletext",
                "loyalty",
                "typeline",
                "cardtype",
                "cardfaces",
                "allparts",
                "layout",
                "artist",
                "legalities",
                "image",
            ]
            results = [dict(zip(columns, row)) for row in rows]
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            results = []
        finally:
            conn.close()

        return results

    @staticmethod
    def CreateSingleMTGCardFromDB(card_name):
        """
        Create a single MTGCard object from the database by its name.
        Args:
            card_name (str): The name of the card to search for.
        Returns:
            MTGCard: An MTGCard object, or None if the card is not found.
        """
        card_data = DBQueries.get_card_from_db(card_name)
        if not card_data or len(card_data) != 1:
            print(f"Card '{card_name}' not found or multiple matches exist.")
            return None

        card_data = card_data[0]  # Get the first (and only) match

        # Create and return the MTGCard object
        return MTGCard(
            name=card_data["name"],
            manacost=card_data["manacost"],
            cmc=card_data["cmc"],
            colors=json.loads(card_data["colors"]),  # Convert JSON string back to list
            colorIdentity=json.loads(
                card_data["coloridentity"]
            ),  # Convert JSON string back to list
            power=card_data["power"],
            toughness=card_data["toughness"],
            oracleText=card_data["oracletext"],
            loyalty=card_data["loyalty"],
            typeline=card_data["typeline"],
            cardType=card_data["cardtype"],
            cardFaces=json.loads(
                card_data["cardfaces"]
            ),  # Convert JSON string back to list
            allParts=json.loads(
                card_data["allparts"]
            ),  # Convert JSON string back to list
            layout=card_data["layout"],
            artist=card_data["artist"],
            scryfallid=None,  # Not stored in the database, set to None or add it to the schema
            legalities=json.loads(
                card_data["legalities"]
            ),  # Convert JSON string back to dict
            image=card_data["image"],
        )

    def CreateEDHDeckFromDB(
        file_path: str,
        deck_name: str,
        format: str,
        commander_name: str,
        regex_engine_card,
    ) -> EDHDeck:
        """
        Create an EDHDeck object from a file containing card names and quantities.
        """

        cards: list = []
        commander = commander_name

        namesDict = DeckParser.CreateDictkWithList(file_path, regex_engine_card)

        for name in namesDict:
            card = DeckParser.CreateSingleMTGCardFromDB(name)
            if card:
                for _ in range(namesDict[name]["quantity"]):
                    cards.append(card)

                if card.name == commander_name:
                    commander = card

        deck = EDHDeck(
            name=deck_name,
            format="commander",
            cards=cards,
            commander=commander,
        )

        # Check for format legality
        isValid, error = deck.enforceFormatRules()
        cond = False
        if isValid == cond:
            raise ValueError(error)

        return deck

    def saveDeckToDB(deck):
        """
        Save the deck to the database.
        """
        conn = sqlite3.connect("mtg_card_db.db")
        cursor = conn.cursor()

        # Create the table if it doesn't exist
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS decks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                format TEXT NOT NULL,
                commander TEXT NOT NULL,
                cards TEXT NOT NULL
            )
            """
        )

        # Serialize the commander and cards as JSON
        commander_json = json.dumps(deck.commander.to_dict()) if deck.commander else None
        cards_json = json.dumps([card.to_dict() for card in deck.cards])

        # Insert the deck into the database
        cursor.execute(
            """
            INSERT INTO decks (name, format, commander, cards)
            VALUES (?, ?, ?, ?)
            """,
            (deck.name, deck.format, commander_json, cards_json),
        )

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

    def loadDeckFromDB(deck_name: str) -> EDHDeck:
        """
        Load a deck from the database by its name.

        Args:
            deck_name (str): The name of the deck to load.

        Returns:
            EDHDeck: The loaded deck object, or None if the deck is not found.
        """
        if not isinstance(deck_name, str) or not deck_name.strip():
            raise ValueError("Invalid deck name provided.")

        conn = sqlite3.connect("mtg_card_db.db")
        cursor = conn.cursor()

        try:
            print(f"Loading deck with name: {deck_name}")
            cursor.execute(
                "SELECT name, format, commander, cards FROM decks WHERE name = ?",
                (deck_name,),
            )
            row = cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            conn.close()

        if not row:
            print(f"Deck '{deck_name}' not found in the database.")
            return None

        # Extract data from the row
        deck_name, deck_format, commander_json, cards_json = row

        # Deserialize the commander
        try:
            commander = MTGCard(**json.loads(commander_json)) if commander_json else None
        except (json.JSONDecodeError, TypeError) as e:
            raise ValueError(f"Error decoding commander JSON: {e}")

        # Deserialize the cards
        try:
            cards_data = json.loads(cards_json)
            cards = [MTGCard(**card_data) for card_data in cards_data]
        except json.JSONDecodeError as e:
            raise ValueError(f"Error decoding cards JSON: {e}")

        # Create and return the EDHDeck object
        return EDHDeck(
            name=deck_name,
            format=deck_format,
            commander=commander,
            cards=cards,
        )

    @staticmethod
    def get_card_from_db(card_name):
        """
        Search for cards in the database by their name and return their data.
        Args:
            card_name (str): The name of the card to search for.
        Returns:
            list: A list of dictionaries containing the cards' data, or an empty list if no matches are found.
        """
        search_pattern = f"%{card_name}%"  # Add wildcards for partial matching
        conn = sqlite3.connect("mtg_card_db.db")
        cursor = conn.cursor()

        try:
            # Query the database for cards with names matching the pattern
            cursor.execute("SELECT * FROM cards WHERE name LIKE ?", (search_pattern,))
            rows = cursor.fetchall()

            if rows:
                # Map the rows to a list of dictionaries
                columns = [
                    "name",
                    "manacost",
                    "cmc",
                    "colors",
                    "coloridentity",
                    "power",
                    "toughness",
                    "oracletext",
                    "loyalty",
                    "typeline",
                    "cardtype",
                    "cardfaces",
                    "allparts",
                    "layout",
                    "artist",
                    "legalities",
                    "image",
                ]
                return [dict(zip(columns, row)) for row in rows]
            else:
                return []
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
        finally:
            conn.close()
