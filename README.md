# MTG Sorter Version 2

A Magic: The Gathering deck and card management tool.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Testing](#testing)
- [Machine Learning](#machine-learning)
- [Development Notes](#development-notes)
- [More Information](#more-information)

---

## Overview

MTG Sorter is a tool for organizing, analyzing, and managing Magic: The Gathering decks and cards. Originally built as a desktop application, the project is evolving towards a modern, three-layer web application (Webpage - Server - Database) with a REST API.

## Features

- Deck and card management with SQLite database backend
- Attribute and partial search for cards
- Deck legality checks for supported formats
- Modular codebase for easy extension
- Plans for web-based UI and RESTful API
- Machine learning integration for card analysis (Word2Vec)
- Test-driven development practices

## Project Structure

- `softwareCode/`  
  Main application code:
  - `mainGUI.py` – Application entry point (AppJar GUI)
  - `mainGUILogic.py` – Application logic
  - `DeckParser.py` – Deck parsing utilities
  - `Deck.py` – Abstract base class for decks
  - `MTGDeck.py` – MTG deck class (format-specific)
  - `PlayingCard.py` – Abstract base class for cards
  - `MTGCard.py` – MTG card data structure
  - `DBQueries.py` – SQLite database methods

- `tests/`  
  Pytest-based unit tests

- `Schemas/`  
  Diagrams and flowcharts

- `mtg_card_db.db`  
  SQLite database file

## Technologies Used

- Python 3.x
- AppJar (GUI)
- SQLite (database)
- PyTest (testing)
- Black, Flake8, Ruff (code style/linting)
- Git (version control)
- Word2Vec (ML, for card text analysis)


## Testing

- Tests are located in the `tests/` folder.
- Run with `pytest`.

## Machine Learning

- Uses a Word2Vec model trained on MTG card text for vector representation.
- The dataset is small, so results may be inaccurate.
- ML features are experimental and subject to change.

## Development Notes

- The project is transitioning to a web-based, three-layer architecture (Webpage - Server - Database) with RESTful APIs.
- Future versions will use HTML, CSS, and TypeScript for the frontend, and Python for the backend.
- Test-driven development and Kanban-style planning are being adopted.

## More Information

- [Development Diary](developmentDiary.md)
- [How To Guide](HowTo.md)
- Diagrams and flowcharts in the `Schemas/` folder

---

Eero Isola