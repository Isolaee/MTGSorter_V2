from abc import ABC, abstractmethod


class PlayingCard(ABC):
    """Abstract base class for a playing card."""

    def __init__(
        self,
        name: str,
        legalities: str,
    ):

        self.name = name
        self.legalities = legalities

    @abstractmethod
    def __str__(self) -> str:
        """Return a string representation of the card."""
        pass

    @abstractmethod
    def __eq__(self, other) -> bool:
        """Check if two cards are equal."""
        pass
