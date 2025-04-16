from .MLMTGCard import MLMTGCard
from .Word2Vec import Word2Vec as W2V


class MLDataTools:
    """
    A class to handle data preprocessing for machine learning tasks.
    """

    def CreateMLMTGCARD(card) -> MLMTGCard:
        """
        Creates a machine learning ready MTGCard out of MTGCard.
        """
        MLcard = MLMTGCard(
            name=W2V.getWordVec(card.getName()),
            manacost=W2V.getWordVec(card.getManaCost()),
            cmc=W2V.getWordVec(card.getCMC()),
            colors=W2V.getWordVec(card.getColors()),
            power=card.getPower(),
            toughness=card.getToughness(),
            oracleText=W2V.getSentenceVector(card.getOracleText()),
            loyalty=card.getLoyalty(),
            typeline=W2V.getWordVec(card.getTypeLine()),
            cardType=W2V.getWordVec(card.getCardType()),
        )
        return MLcard

    def CreateMLEDHDeck():
        """
        Creates a machine learning ready EDH deck out of MLMTGDeck.
        """
        pass
