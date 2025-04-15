# MTG Sorter versio 2.

## Why?
I decided to rewrite the program simply beacuse I was not happy with it. I can do better.

## The Plan
Simple plan is to rewrite the program.
Not so simple plan is to:
- Create digital diagrams
- Enforce coding habits, and implement tests
- Rewrite the classes
- New error handling

## Tools
- Tests: pyTest
- Coding: black/flake8/ruff
- Git: pre-commit/Git

## GUI
- JarApp (not included in Git)

## Code is located in Code folder
- App.py -> app starting point
- DeckParser.py -> utility class for deck
- Deck.py -> abstract base class for MTGDeck.py
- MTGDeck.py -> abstract class for different MTGDecks. Because MTG and other TCG have different formats, the class we instantiate object from will be defied by format.
- PlayingCard.py -> Abtract base class for MTGCard.py
- MTGCard.py -> Card Class, that hold the datastructure of a MTG card.

## Tests are located in tests folder

## Diagrams are located in Schemas folder.
- Deck & Card class diagram

## Machine Learning
The plan is to implement my old (rewritten) ML model to this software.
These are some key points to remember.
- Model often don't understand natural languages. This is why I need to make vector representation of my text. I made that with Word2Vec library. The Word2Vec model is trained on all MTG words. So it is higly spesific.
- I have only small dataset, so the results will be highly inaccurate.