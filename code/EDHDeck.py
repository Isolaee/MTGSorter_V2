from MTGDeck import MTGDeck
from MTGCard import MTGCard
from collections import Counter


class EDHDeck(MTGDeck):
    """Class representing a Commander (EDH) deck of Magic: The Gathering cards."""

    def __init__(
        self,
        name: str,
        format: str,
        formatRules: list,
        cards: list,
        commander: MTGCard,
        scryfallStatic: str,
    ) -> None:
        super().__init__(name, cards, scryfallStatic)
        self.name = name
        self.format = format
        self.formatRules = formatRules
        self.cards = cards
        self.commander = commander

    def getName(self) -> str:
        """Return the name of the deck."""
        return self.name

    def getFormat(self) -> str:
        """Return the format of the deck."""
        return self.format

    def getFormatRules(self) -> list:
        """Return the format rules of the deck."""
        return self.formatRules

    def getCards(self) -> list:
        """Return the cards in the deck."""
        return self.cards

    def getCommander(self) -> MTGCard:
        """Return the commander of the deck."""
        return self.commander.toString()  # This toString() might of might not work.

    def getScryfallStatic(self) -> str:
        """Return the Scryfall static URL."""
        return self.scryfallStatic

    def shuffle(self):
        return super().shuffle()

    def draw_card(self):
        return super().draw_card()

    def __str__(self):
        return self.getName()

    def getAllCardNames(self) -> list:
        return super().getAllCardNames()

    def getCardNamesAndAmounts(self):
        """Return a dictionary of card names and their amounts."""
        card_counts = Counter(card.getName() for card in self.cards)
        return dict(card_counts)

    def getDeckData(self) -> dict:
        """Return the deck data as a dictionary. This data is meant to be used for graphical representation."""
        deck_data = {
            "name": self.getName(),
            "format": self.getFormat(),
            "formatRules": self.getFormatRules(),
            "commander": self.getCommander(),
            "cards": self.getAllCardNames(),
            "CMCs": [card.getCMC() for card in self.cards],
        }
        return deck_data

    def getHistogramData(self, histogramType):
        return super().getHistogramData(histogramType)
