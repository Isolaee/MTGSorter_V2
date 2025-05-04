# Import all classes and modules from the sofwareCode package

# Deck-related imports
from .Deck import Deck
from .MTGDeck import MTGDeck
from .EDHDeck import EDHDeck

# Card-related imports
from .PlayingCard import PlayingCard
from .MTGCard import MTGCard

# Utility imports
from .DeckParser import DeckParser
from .DBQueries import DBQueries


# Explicitly define what is exported when using `from softwareCode import *`
__all__ = [
    "Deck",
    "MTGDeck",
    "EDHDeck",
    "PlayingCard",
    "MTGCard",
    "DeckParser",
    "DBQueries",
]
