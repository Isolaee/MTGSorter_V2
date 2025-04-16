from .MTGDeck import MTGDeck
from .MTGCard import MTGCard
from collections import Counter
from typing import Tuple, Dict


class EDHDeck(MTGDeck):
    """Class representing a Commander (EDH) deck of Magic: The Gathering cards."""

    formatRules: dict = {
        "commander": True,
        "deck_size": 100,
        "singleton": True,
        "banned_cards": [
            "Ancestral Recall",
            "Balance",
            "Biorhythm",
            "Black Lotus",
            "Braids, Cabal Minion",
            "Chaos Orb",
            "Coalition Victory",
            "Channel",
            "Dockside Extortionist",
            "Emrakul, the Aeons Torn",
            "Erayo, Soratami Ascendant",
            "Falling Star",
            "Fastbond",
            "Flash",
            "Gifts Ungiven",
            "Golos, Tireless Pilgrim",
            "Griselbrand",
            "Hullbreacher",
            "Iona, Shield of Emeria",
            "Karakas",
            "Jeweled Lotus",
            "Leovold, Emissary of Trest",
            "Library of Alexandria",
            "Limited Resources",
            "Lutri, the Spellchaser",
            "Mana Crypt",
            "Mox Emerald",
            "Mox Jet",
            "Mox Pearl",
            "Mox Ruby",
            "Mox Sapphire",
            "Nadu, Winged Wisdom",
            "Panoptic Mirror",
            "Paradox Engine",
            "Primeval Titan",
            "Prophet of Kruphix",
            "Recurring Nightmare",
            "Rofellos, Llanowar Emissary",
            "Shahrazad",
            "Sundering Titan",
            "Sway of the Stars",
            "Sylvan Primordial",
            "Time Vault",
            "Time Walk",
            "Tinker",
            "Tolarian Academy",
            "Trade Secrets",
            "Upheaval",
            "Yawgmoth's Bargain",
        ],
        "color_identity": True,
    }

    def __init__(
        self,
        name: str,
        format: str,
        cards: list,
        commander: MTGCard,
    ) -> None:
        super().__init__(name, cards)
        self.name = name
        self.format = format
        self.cards = cards
        self.commander = commander

    def getName(self) -> str:
        """Return the name of the deck."""
        if self.name == "":
            return "Unnamed Deck"

        return self.name

    def getFormat(self) -> str:
        """Return the format of the deck."""
        return self.format

    def getFormatRules(self) -> list:
        """Return the format rules of the deck."""
        return self.formatRules

    def getCards(self) -> list:
        """Return the cards in the deck."""
        return self.cards

    def getCommander(self) -> MTGCard:
        """Return the commander of the deck."""
        return self.commander.toString()  # This toString() might of might not work.

    def getScryfallStatic(self) -> str:
        """Return the Scryfall static URL."""
        return self.scryfallStatic

    def shuffle(self):
        return super().shuffle()

    def draw_card(self):
        return super().draw_card()

    def __str__(self):
        return self.getName()

    def getAllCardNames(self) -> list:
        return super().getAllCardNames()

    def getCardNamesAndAmounts(self):
        """Return a dictionary of card names and their amounts."""
        card_counts = Counter(card.getName() for card in self.cards)
        return dict(card_counts)

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

    def getHistogramData(self, histogramType):
        return super().getHistogramData(histogramType)

    def enforceFormatRules(self) -> Tuple[bool, Dict]:
        """Enforce the format rules for the deck."""
        formatCheckFails: dict = {}
        isValid: bool = True

        # Check if the commander is in the deck
        if self.commander.getName() not in self.getAllCardNames():
            formatCheckFails["Commander"] = "Commander not in deck"
            isValid = False

        # Check if the deck size is within the Decklimit
        if len(self.cards) != self.formatRules.get("deck_size"):
            formatCheckFails["Deck Size"] = (
                f"Deck size is invalid. Deck has to be: {self.formatRules.get('deck_size')}"
            )
            isValid = False
        else:
            len(self.cards) == self.formatRules.get("deck_size")
            pass

        # Check if contains banned cards
        overlap = set(self.getAllCardNames()) & set(self.formatRules.get("banned_cards"))
        if overlap:
            formatCheckFails["Banned Cards"] = (
                f"Contains banned cards: {', '.join(overlap)}"
            )
            isValid = False

        # Check singleton rule
        singleton_exceptions = [
            "Plains",
            "Island",
            "Swamp",
            "Mountain",
            "Forest",
            "Snow-Covered Plains",
            "Snow-Covered Island",
            "Snow-Covered Swamp",
            "Snow-Covered Mountain",
            "Snow-Covered Forest",
        ]
        duplicates = [
            item
            for item, count in Counter(self.getAllCardNames()).items()
            if count > 1 and item not in singleton_exceptions
        ]
        if duplicates:
            formatCheckFails["Singleton"] = (
                f"Contains duplicates: {', '.join(duplicates)}"
            )
            isValid = False

        # Check color identity rule
        commander_color_identity = set(self.commander.getColorIdentity())
        invalid_cards = [
            card.getName()
            for card in self.cards
            if not set(card.getColorIdentity()).issubset(commander_color_identity)
        ]
        if invalid_cards:
            formatCheckFails["Color Identity"] = (
                f"Cards with invalid color identity: {', '.join(invalid_cards)}"
            )
            isValid = False

        return isValid, formatCheckFails
