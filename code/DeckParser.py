from EDHDeck import EDHDeck
from MTGCard import MTGCard
from pathlib import Path
import json


class DeckParser:
    """Utility class for parsing deck lists."""

    @staticmethod
    def CreateDeck(
        file_path: str,
        deck_name: str,
        format: str,
        commander_name: str,
        regex_engine_card,
        regex_engine_type,
    ):
        cards = []
        ScryData = "Data\\ScryfallCardData13_04_2025.json"
        commander = commander_name
        if format != "Commander":
            commander = None

            # Load Scryfall data from JSON
        with open(ScryData, "r", encoding="utf-8") as scryfall_file:
            scryfall_data = json.load(scryfall_file)

        with open(file_path, "r") as file:

            for line in file:
                try:
                    match = regex_engine_card.search(line)
                    if not match:
                        raise ValueError(f"Invalid line format: {line.strip()}")
                    card_name = match.group("name").strip()
                    quantity = int(match.group("amount"))

                    ## Get card Data from Scryfall
                    # Find card data in Scryfall JSON
                    card_data = next(
                        (card for card in scryfall_data if card["name"] == card_name),
                        None,
                    )
                    if not card_data:
                        raise ValueError(
                            f"Card '{card_name}' not found in Scryfall data."
                        )

                    creature_type_match = regex_engine_type.search(card_data["type_line"])
                    if creature_type_match:
                        cardType = creature_type_match.group("CardType")
                        creatureType = creature_type_match.group("CreatureType")
                    else:
                        cardType = (
                            "Unknown"  # Assign a default value for cardType if needed
                        )
                        creatureType = ""  # Assign a default value for creatureType

                    card = MTGCard(
                        name=card_name,
                        manacost=card_data.get("mana_cost"),
                        cmc=card_data.get("cmc"),
                        colors=card_data.get("colors"),
                        power=card_data.get("power"),
                        toughness=card_data.get("toughness"),
                        oracleText=card_data.get("oracle_text"),
                        loyalty=card_data.get("loyalty"),
                        typeline=creatureType,
                        cardType=cardType,
                        cardFaces=card_data.get("card_faces"),
                        allParts=card_data.get("all_parts"),
                        layout=card_data.get("layout"),
                        artist=card_data.get("artist"),
                        scryfallid=card_data.get("id"),
                        legalities="Commander",
                    )

                    for _ in range(quantity):
                        cards.append(card)

                    if card_name == commander_name:
                        commander = card
                except ValueError as e:
                    print(f"Error': {e}")
                    continue

        if not commander:
            raise ValueError(f"Commander '{commander_name}' not found in the deck list.")

        return EDHDeck(
            name=deck_name,
            format="Commander",
            formatRules=["Singleton", "100 cards"],
            cards=cards,
            commander=commander,
        )

    @staticmethod
    def serializeDeck(deck) -> None:
        """
        Serialize the EDHDeck object to a JSON file.

        Args:
            deck (EDHDeck): The deck object to serialize.
        """
        file_path = "Decks/" + deck.name + ".json"
        deck = deck.to_dict()  # Convert the deck object to a dictionary
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(deck, file, indent=4)

    @staticmethod
    def deserializeDeck(file_path: str) -> EDHDeck:
        """
        Deserialize an EDHDeck object from a JSON file.

        Args:
            file_path (str): The path to the JSON file.

        Returns:
            EDHDeck: The deserialized deck object.
        """
        with open(file_path, "r", encoding="utf-8") as file:
            deck_data = json.load(file)

        # Validate and recreate the MTGCard objects
        cards = []
        for card_data in deck_data["cards"]:
            if isinstance(card_data, dict):  # Ensure card_data is a dictionary
                cards.append(MTGCard(**card_data))
            else:
                raise ValueError(f"Invalid card data: {card_data}")

        # Validate and recreate the commander object
        commander = None
        if deck_data["commander"]:
            if isinstance(
                deck_data["commander"], dict
            ):  # Ensure commander is a dictionary
                commander = MTGCard(**deck_data["commander"])
            else:
                raise ValueError(f"Invalid commander data: {deck_data['commander']}")

        # Return the reconstructed EDHDeck object
        return EDHDeck(
            name=deck_data["name"],
            format=deck_data["format"],
            formatRules=deck_data["formatRules"],
            cards=cards,
            commander=commander,
        )

    @staticmethod
    def read_folder_contents(folder_path):
        """
        Read the contents of a folder and return a list of file names.

        Args:
            folder_path (str): The path to the folder.

        Returns:
            list: A list of file names in the folder.
        """
        folder = Path(folder_path)
        if folder.exists() and folder.is_dir():
            return [item.name for item in folder.iterdir() if item.is_file()]
        else:
            print(f"The folder '{folder_path}' does not exist.")
            return []

    ## Saved Decks
    @staticmethod
    def loadSavedDecks(file_path: str):
        """
        Load saved decks from the JSON file.

        Returns:
            list: A list of saved decks.
        """

        try:
            with open(file_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []
