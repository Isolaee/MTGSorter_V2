### This document is guide how to use this software

<details>
<summary>Start</summary>
Currently these is no executable file. You can run program from root with "python -m softwareCode.app", or from enywhere with proper path.
</details>

<details>
<summary>Pages</summary>
There are three pages at the moment.
- Welcome
- Load deck page, which is for importing a deck.
- Create a deck, which is for making decks.
</details>

<details>
<summary>Usage - Welcome</summary>
Welcome is "redirect" page, in here you can choose what to do.
</details>

<details>
<sumary>Usage -  Deck import</summary>
The software GUI can be divided in thee sections.
- Deckload -> loading new deck from txt
- Deckview -> Seeing Deck Data
- Saved Decks -> see saved Decks and load them.

# Deckload
From top of the GUI you can see Deckname, Commander name and deckpath and Load selections.
By giving asked information you can create your deck from .txt file.

# Deck view
In the middle section, you can see the "active" deck. On the left there is the cards and on the right there is space for visuals. From top left, if you click "data" and one the selection, the right container gets filled with requested data.
You may see card images by clicking them.

# Saved Decks
On the bottom, you can see saved decks, and button for saving your active deck. By clicking any of the saved decks, the software will load them as active deck.
</details>

<details>
<summary>Usage - Create Deck</summary>
On this page, you can (ot will be able, when this is done, marked with * symbol in this text) search for single cards using it's name or with attributes*. You can see image of the card and add it to your deck by clicking it. You can delete the card from you deck by clicking it in deck section*. You also can choose if deck is for spesific format* and give metadata*. You have option to save the deck*.
</details>

<details>
<summary>Future?</summary>
Future section includes multiple subsection.
These are divided by time, since my take on software changes over the project.
<details>
<summary>16/04</summary>

# immidiate future

There are two concrete updates that I want to do.
1. Get the ML part working in software.
2. While you have active deck, seeing the card image from request. (Done 19/04)

Of course I would like to implement more data tools, but I feel like having that ML integration was big part why I rewrote the software and seeing deck images is very important since that image contains almoust all of the data you need, from a single card. It would make thinking about your deck as a user, much easier.

But this project is not yet done, so I will have time to make proper changes.
</details>
<details>
<summary>25/04</summary>

# ML & software
While pondering over twi things.
1. Implementing the ML as soon as possible
2. Creating robust data tools before ML

I have started to lean on data tools. I have few reasons. I have found myself having fun optimizing certain methods in my code. The latest example is the searcing for cards. The search time went down about 1/30 of the time after implementing SQLite database.
Another reason is software philosophy, If I can say so.
If I made MTG/Cardgame datatool, that is not totally unique. It's not common, but not unique. Making my own neuronetwork that can asses the deck power would be unique, BUT... It would not matter because that is still not important to players on it's own. In isolation it is interesting feature, but I doubt that anyone would use my tool just because of it. This software needs to tick every other deckbuilding box, before that.
So solid deck building and search tools, analytics and "example hands". ML is just Cherry on top.
</details>
</details>