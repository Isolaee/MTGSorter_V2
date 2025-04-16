from .MTGCard import MTGCard


class MLMTGCard(MTGCard):
    """Class for a Magic: The Gathering card with machine learning features."""

    def __init__(
        self,
        name,
        manacost,
        cmc,
        colors,
        power,
        toughness,
        oracleText,
        loyalty,
        typeline,
        cardType,
    ):

        super().__init__(
            name,
            manacost,
            cmc,
            colors,
            power,
            toughness,
            oracleText,
            loyalty,
            typeline,
            cardType,
            colorIdentity=None,
            cardFaces=None,
            allParts=None,
            layout=None,
            artist=None,
            scryfallid=None,
            legalities=None,
        )
