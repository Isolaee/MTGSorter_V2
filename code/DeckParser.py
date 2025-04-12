from EDHDeck import EDHDeck
from MTGCard import MTGCard


class DeckParser:
    """Utility class for parsing deck lists."""

    @staticmethod
    def CreateDeck(
        file_path: str, deck_name: str, format: str, commander_name: str, regex_engine
    ):
        cards = []
        commander = commander_name
        if format != "Commander":
            commander = None

        with open(file_path, "r") as file:

            for line in file:
                try:
                    match = regex_engine.search(line)
                    if not match:
                        raise ValueError(f"Invalid line format: {line.strip()}")
                    card_name = match.group("name").strip()
                    quantity = int(match.group("amount"))

                    card = MTGCard(
                        name=card_name,
                        manacost=[],
                        cmc=0,
                        colors=[],
                        power=0,
                        toughness=0,
                        oracleText="",
                        loyalty="",
                        typeline="",
                        cardFaces="",
                        allParts="",
                        layout="",
                        artist="",
                        scryfallid=0,
                        legalities="Commander",
                    )

                    for _ in range(quantity):
                        cards.append(card)

                    if card_name == commander_name:
                        commander = card
                except ValueError as e:
                    print(f"Error parsing line '{line.strip()}': {e}")
                    continue

        if not commander:
            raise ValueError(f"Commander '{commander_name}' not found in the deck list.")

        return EDHDeck(
            name=deck_name,
            format="Commander",
            formatRules=["Singleton", "100 cards"],
            cards=cards,
            commander=commander,
            scryfallStatic="https://scryfall.com",
        )
