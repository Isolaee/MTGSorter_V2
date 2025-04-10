from typing import TypeVar
from PlayingCard import PlayingCard  # Assuming MTGCard inherits from PlayingCard
from Deck import Deck
from abc import ABC, abstractmethod

# Define a TypeVar for the card type
T = TypeVar("T", bound=PlayingCard)  # T must be a subclass of PlayingCard


class MTGdeck(Deck, ABC):
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
    def add_card(self, card: T) -> None:
        """Add a card to the deck."""
        if len(self.cards) < 60:
            self.cards.append(card)
        else:
            raise ValueError("Deck already contains 60 cards.")

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
