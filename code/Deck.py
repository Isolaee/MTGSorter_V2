from abc import ABC, abstractmethod


class Deck(ABC):
    """Abstract base class for a Deck."""

    def __init__(
        self,
        name: str,
    ):

        self.name = name

    @abstractmethod
    def __str__(self) -> str:
        """Return a string representation of the deck."""
        pass

    @abstractmethod
    def CreateDeck(self, filename: str):
        """Create a deck from a file."""
        pass
