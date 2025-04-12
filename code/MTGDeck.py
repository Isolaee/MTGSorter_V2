from typing import TypeVar
from PlayingCard import PlayingCard  # Assuming MTGCard inherits from PlayingCard
from Deck import Deck
from abc import ABC, abstractmethod

# Define a TypeVar for the card type
T = TypeVar("T", bound=PlayingCard)  # T must be a subclass of PlayingCard


class MTGDeck(Deck, ABC):
    """Class representing a deck of Magic: The Gathering cards."""

    def __init__(self, name: str, scryfallStatic: str) -> None:
        super().__init__(name)
        self.name = name
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
        deck_data = {
            "name": self.getName(),
            "format": self.getFormat(),
            "formatRules": self.getFormatRules(),
            "commander": self.getCommander(),
            "cards": self.getAllCardNames(),
            "CMCs": [card.getCMC() for card in self.cards],
        }
        return deck_data
