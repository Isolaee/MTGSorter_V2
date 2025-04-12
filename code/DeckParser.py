from EDHDeck import EDHDeck
from MTGCard import MTGCard


class DeckParser:
    """Utility class for parsing deck lists."""

    @staticmethod
    def CreateDeck(file_path: str, deck_name: str, commander_name: str) -> EDHDeck:
        cards = []
        commander = None

        with open(file_path, "r") as file:

            # implementing the parsing logic
            # remember the handle
            # different formats
            # error cases

            for line in file:
                line = line.strip()
                if not line:
                    continue

                parts = line.split(" ", 1)
                quantity = int(parts[0])
                card_name = parts[1]

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
