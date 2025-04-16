# Development Diary, aka Rambling.

<details>
<summary>12/04</summary>

# Regex and linescraping
I was pondering to replace regex with my own scraper. But I got convinced that it would be bad idea, and regex is good for for that.
But in the spirit of improving this software I simplified regex string and added better reading for different formats. Last time, my regex could only handle <number>\s<chars> now it can handle x and or , after number. And the name may contain special characters.

# GUI
The short term plan is to implement two panel system to my GUI. Right panel would list cards etc, and left panel would serve as place for graphs or card images. Today evening I implemented the panels and left one got working with out a hitch.

# TODO
I also implented the method for my deckdata. So assume that I will/can implement different (Mana curve etc) graphs tomorrow.
</details>

<details>
<summary>14/04</summary>

# Filling the different cards.
One of the goals of this rewrite was to increase errorhandling. Or rather make better pipeline from cardname to card Obj. Unfortunatelu I forgot a thing. In MTG these is cards called MDFC. Modal double-faced cards. Their names are written as "Side1 // side2". This is not feasable to my software at the moment. The software refuses any MDFC and thus the decklists might be incomplete. Hopefully this is fixable with regex update.
Update:
This is due:
My data, where every card data is found, has names as "side1/side2", but every deckbuilding site export cards just as name = side1.
I need to reporgram way I look data from my file.

# GUI
The deckupload can be handled by clicking saved deck.
GUI is as big as its content. Same as Saved Decks list.
Basicly the saving and loading saved decks feel better and require less clicks.
</details>

<details>
<summary>15/04</summary>

# reading and makings cards
For some time I have had problem with
- Loading time
- Two faced cards.
Today I have fixed on problem and imporved upon another.
Now my software do not throw an error when it encounters two faced card. That naming was a problem because it is somewhat different.
The problem two was quite a hefty loading time when creating a deck. But based on my feeling, it got down a bit because I adjusted the logic.

# Enforcing format rules
Even tho this software only understand one game and one format, I am going expand on at least different formats. So this is one of the reasons I need to have these format rules enforced. If I load a deck, I need to be able to trust it is "legal". First enforceFormatRules is located in EDHDeck class. I need to think if MTGDeck is better place for it. I could just overload that function to use it in every format.

# Machine Learning
The biggest part of this ML rewrite is creating new data pipeline and writing new class for data. But because V2 has more robust foundations I think it will be much easier than last time. Also now I have experince on this software.
Today I imported some of my old code regarding vectorizing code and wrote class for ML-MTGCard.

# TODO: Tests
I still haven't wrote any tests. That is something I need to do.
</details>

<details>
<summary>16/04</summary>

# Tests
Today is the time to write tests. My strategy is to write test to "critical path".
As I said I am using PyTest. Tests are located in tests foldel.