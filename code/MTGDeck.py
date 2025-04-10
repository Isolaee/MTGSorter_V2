from typing import Generic, TypeVar, List
from PlayingCard import PlayingCard  # Assuming MTGCard inherits from PlayingCard

# Define a TypeVar for the card type
T = TypeVar("T", bound=PlayingCard)  # T must be a subclass of PlayingCard


class MTGdeck(Generic[T]):
    """Class representing a deck of Magic: The Gathering cards."""

    def __init__(self):
        self.cards: List[T] = []  # List to hold cards of type T

    def add_card(self, card: T) -> None:
        """Add a card to the deck."""
        if len(self.cards) < 60:
            self.cards.append(card)
        else:
            raise ValueError("Deck already contains 60 cards.")

    def shuffle(self) -> None:
        """Shuffle the deck."""
        import random

        random.shuffle(self.cards)

    def draw_card(self) -> T:
        """Draw a card from the top of the deck."""
        if self.cards:
            return self.cards.pop(0)
        else:
            raise ValueError("The deck is empty.")
