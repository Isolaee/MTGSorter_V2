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