"""
The `softwareCode` package contains modules and classes for managing decks, cards,
and the graphical user interface for the MTGSorter application.

This `__init__.py` file organizes imports
"""

# Deck-related imports: Classes and modules for managing decks
from .Deck import Deck
from .MTGDeck import MTGDeck
from .EDHDeck import EDHDeck

# Card-related imports: Classes for representing cards
from .PlayingCard import PlayingCard
from .MTGCard import MTGCard

# Utility imports: Helper modules for parsing and database queries
from .DeckParser import DeckParser
from .DBQueries import DBQueries

# GUI-related imports: Logic for the graphical user interface
from .mainGUILogic import MainLogic

# Explicitly define what is exported when using `from softwareCode import *`
__all__ = [
    "DBQueries",
    "Deck",
    "DeckParser",
    "EDHDeck",
    "MainLogic",
    "MTGCard",
    "MTGDeck",
    "PlayingCard",
]
