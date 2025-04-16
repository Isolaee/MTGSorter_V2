import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

import pytest
from sofwareCode.EDHDeck import EDHDeck


def test_get_name_valid():
    deck_name = "Test Deck"
    deck = EDHDeck(name=deck_name, format="Commander", cards=[], commander=None)

    result = deck.getName()

    assert result == deck_name, f"Expected {deck_name}, but got {result}"

def test_get_name_empty():
    empty_deck_name = ""
    deck = EDHDeck(name=empty_deck_name, format="Commander", cards=[], commander=None)

    result = deck.getName()

    assert result == "Unnamed Deck", f"Expected empty string, but got {result}"