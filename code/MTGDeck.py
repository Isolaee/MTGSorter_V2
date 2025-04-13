from typing import TypeVar
from MTGCard import MTGCard  # Assuming MTGCard inherits from PlayingCard
from Deck import Deck
from abc import ABC, abstractmethod

# Define a TypeVar for the card type
T = TypeVar("T", bound=MTGCard)  # T must be a subclass of PlayingCard


class MTGDeck(Deck, ABC):
    """Class representing a deck of Magic: The Gathering cards."""

    def __init__(self, name: str, cards: list[T], scryfallStatic: str) -> None:
        super().__init__(name)
        self.name = name
        self.cards: list = cards
        self.scryfallStatic = scryfallStatic

    @abstractmethod
    def getName(self) -> str:
        """Return the name of the deck."""
        return self.name

    @abstractmethod
    def getScryfallStatic(self) -> str:
        """Return the Scryfall static URL."""
        return self.scryfallStatic

    @abstractmethod
    def shuffle(self) -> None:
        """Shuffle the deck."""
        import random

        random.shuffle(self.cards)

    @abstractmethod
    def draw_card(self) -> T:
        """Draw a card from the top of the deck."""
        if self.cards:
            return self.cards.pop(0)
        else:
            raise ValueError("The deck is empty.")

    def getAllCardNames(self):
        """Return a list of all card names in the deck."""
        return [card.getName() for card in self.cards]

    @abstractmethod
    def getDeckData(self) -> dict:
        """Return the deck data as a dictionary. This data is meant to be used for graphical representation."""
        pass

    @abstractmethod
    def getHistogramData(self, histogramType) -> dict:
        """Return a dict that has relevant data for Histograms
        Params: Histogram Type, CMC, CardType
        """

        values = {}

        # CMC histogram
        if histogramType == "CMC":
            parsedData: dict = {}
            for card in self.cards:
                if card.getCMC() != 0:
                    if card.getCMC() in parsedData:
                        parsedData[card.getCMC()] += 1
                    else:
                        parsedData[card.getCMC()] = 1

            print(card.getName(), " ", card.getCMC())
            values = parsedData

        # CardType histogram
        elif histogramType == "CardType":
            parsedData: dict
            for card in self:
                if card.getCardType() in parsedData:
                    parsedData[card.getCardType()] += 1
                else:
                    parsedData[card.getCardType()] = 1
            values = parsedData
        else:
            return values

        print(values)  # Debugging
        return values
