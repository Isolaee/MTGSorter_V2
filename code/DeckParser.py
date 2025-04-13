from EDHDeck import EDHDeck
from MTGCard import MTGCard
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
