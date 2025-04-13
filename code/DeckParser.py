from EDHDeck import EDHDeck
from MTGCard import MTGCard
import json


class DeckParser:
    """Utility class for parsing deck lists."""

    @staticmethod
    def CreateDeck(
        file_path: str, deck_name: str, format: str, commander_name: str, regex_engine
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
                    match = regex_engine.search(line)
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

                    card = MTGCard(
                        name=card_name,
                        manacost=card_data.get("manacost"),
                        cmc=card_data.get("cmc"),
                        colors=card_data.get("colors"),
                        power=card_data.get("power"),
                        toughness=card_data.get("toughness"),
                        oracleText=card_data.get("oracleText"),
                        loyalty=card_data.get("loyalty"),
                        typeline=card_data.get("typeline"),
                        cardFaces=card_data.get("cardFaces"),
                        allParts=card_data.get("allParts"),
                        layout=card_data.get("layout"),
                        artist=card_data.get("artist"),
                        scryfallid=card_data.get("scryfallid"),
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
