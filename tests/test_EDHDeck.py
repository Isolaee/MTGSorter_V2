import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

import pytest
from softwareCode.EDHDeck import EDHDeck


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

def test_get_format_Commander():
    deck_format = "Commander"
    deck = EDHDeck(name="Test Deck", format=deck_format, cards=[], commander=None)

    result = deck.getFormat()

    assert result == deck_format, f"Expected {deck_format}, but got {result}"

def test_get_format_other():
    deck_format = "Standard"
    deck = EDHDeck(name="Test Deck", format=deck_format, cards=[], commander=None)

    result = deck.getFormat()

    assert result == deck_format, f"Expected {deck_format}, but got {result}"

def test_get_Cards_valid():
    deck_cards = ["Card1", "Card2", "Card3"]
    deck = EDHDeck(name="Test Deck", format="Commander", cards=deck_cards, commander=None)

    result = deck.getCards()

    assert result == deck_cards, f"Expected {deck_cards}, but got {result}"
    
def test_get_Cards_noCards():
    deck_cards = []
    deck = EDHDeck(name="Test Deck", format="Commander", cards=deck_cards, commander=None)

    result = deck.getCards()

    assert result == deck_cards, f"Expected {deck_cards}, but got {result}"

def get_commander_valid():
    commander = "CommanderCard"
    deck = EDHDeck(name="Test Deck", format="Commander", cards=[], commander=commander)

    result = deck.getCommander()

    assert result == commander, f"Expected {commander}, but got {result}"