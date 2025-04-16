import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

import pytest
from sofwareCode.EDHDeck import EDHDeck


def test_get_name():
    # Arrange: Create an instance of EDHDeck with a specific name
    deck_name = "Test Deck"
    deck = EDHDeck(name=deck_name, format="Commander", cards=[], commander=None)

    # Act: Call the getName() method
    result = deck.getName()

    # Assert: Verify that the result matches the expected name
    assert result == deck_name, f"Expected {deck_name}, but got {result}"

