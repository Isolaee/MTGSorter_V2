# Development Diary, aka Rambling.

<details>
<summary>12/04</summary>

# Regex and Line Scraping
I was pondering replacing regex with my own scraper. But I got convinced that it would be a bad idea, and regex is good for that purpose.  
In the spirit of improving this software, I simplified the regex string and added better handling for different formats. Previously, my regex could only handle `<number>\s<chars>`. Now it can handle `x` and/or `,` after the number. Additionally, the name may contain special characters.

# GUI
The short-term plan is to implement a two-panel system in my GUI. The right panel would list cards, etc., and the left panel would serve as a place for graphs or card images. Today evening, I implemented the panels, and the left one worked without a hitch.

# TODO
I also implemented the method for my deck data. So, I assume that I will/can implement different graphs (e.g., Mana curve) tomorrow.
</details>

<details>
<summary>14/04</summary>

# Filling the Different Cards
One of the goals of this rewrite was to increase error handling, or rather, make a better pipeline from card name to card object. Unfortunately, I forgot one thing. In MTG, there are cards called MDFC (Modal Double-Faced Cards). Their names are written as "Side1 // Side2". This is not feasible for my software at the moment. The software refuses any MDFC, and thus the decklists might be incomplete. Hopefully, this is fixable with a regex update.  
**Update:**  
This is due to:  
My data, where every card's data is found, has names as "Side1/Side2", but every deckbuilding site exports cards with names like "Side1".  
I need to reprogram the way I look up data from my file.

# GUI
The deck upload can now be handled by clicking a saved deck.  
The GUI is as big as its content, same as the Saved Decks list.  
Basically, saving and loading saved decks feels better and requires fewer clicks.
</details>

<details>
<summary>15/04</summary>

# Reading and Making Cards
For some time, I have had problems with:
- Loading time
- Two-faced cards.

Today, I fixed one problem and improved upon another.  
Now my software does not throw an error when it encounters a two-faced card. The naming was a problem because it is somewhat different.  
The second problem was quite a hefty loading time when creating a deck. Based on my feeling, it has decreased a bit because I adjusted the logic.

# Enforcing Format Rules
Even though this software only understands one game and one format, I am going to expand on at least different formats. This is one of the reasons I need to have these format rules enforced. If I load a deck, I need to be able to trust that it is "legal".  
Currently, `enforceFormatRules` is located in the `EDHDeck` class. I need to think if `MTGDeck` is a better place for it. I could just overload that function to use it in every format.

# Machine Learning
The biggest part of this ML rewrite is creating a new data pipeline and writing a new class for data. But because V2 has more robust foundations, I think it will be much easier than last time. Also, now I have experience with this software.  
Today, I imported some of my old code regarding vectorizing and wrote a class for ML-MTGCard.

# TODO: Tests
I still haven't written any tests. That is something I need to do.
</details>

<details>
<summary>16/04</summary>

# Tests
Today is the time to write tests. My strategy is to write tests for the "critical path".  
As I said, I am using PyTest. Tests are located in the `tests` folder.
</details>

<details>
<summary>19/04</summary>

# Card Images
I value the card image feature because there are over 40,000 unique cards in MTG, and it's a fool's errand trying to remember them all. Having access to card images is vital when pondering your deck. So, it is a very user-friendly feature.  
I implemented this as follows:  
In my data, I have a link to Scryfall, so when creating a card object, it fetches the link.  
In the software, when you click that card in the deck preview, it dynamically fetches that image, temporarily saves it, and shows it.  
This way, there is no massive card image database in the software.
</details>

<details>
<summary>24/04</summary>

# Database Update
For some time, I have suffered from slow deck/card creation times. This was (of course) due to a horrible way of finding card data. I used JSON and iterated over it, basically having O(n/2) times. I decided to implement an SQLite database to cut search times and enable better partial search and attribute search.  
Today, I implemented the database, filled it, and created new methods. As you can imagine, load times were drastically reduced. In the future, I will implement attribute search and partial search.

Some reasons to choose a relational database, SQLite in this case:
- Two features, partial match and attribute search, are important.
- SQLite has native support.
- With SQLite, I don't have to care about balancing binary trees because the DB does it for me. I was thinking about implementing a binary search tree with my data.
- SQLite gives me flexibility when creating new features. With this software, I don't benefit from absolute search time. It just needs to be fast enough not to be noticed by the user.
</details>

<details>
<summary>05/05</summary>

For the last week, I had a terrible week and did not think about this project at all. Of course, this gave me some perspective once I opened my editor again. On days 04 and 05, I implemented new features for the Create Deck page. There is card search by attributes, and you can save the deck. But once I finished these features, I felt something had changed. **My code has become too messy.**  
I suppose, because this is all "new code", it made me lose sight of the most important aspect: **Planning**. I am having a hard time finding the correct piece of code or bug. I have too much code in one place, and I have too many different methods.  

So... For the next few days, I will do some cleanup.  
I will:
- Review the code
- Think long and hard
- Draw some schemas of the system
- Hopefully reduce the number of methods by making more generic methods
- Make code more reusable
- Improve error handling

I think the root cause of these recent problems is a lack of "vision". Taking time to review my code and trying to improve it, instead of making new code, will make for a better development experience.  
On a small side note, I think I should not only think about what my methods return, but also what I want them to return and why. I need to make myself clear on what is the main data I am handling.
</details>

<details>
<summary>06/05</summary>

# Software
After some pondering, I have decided that every piece of data related to the "game" in the software will be represented as `MTGCard` or `MTGDeck` objects (or other TCG objects in the future). This approach allows me to build data analysis directly on "decks" and unify the way I display names and other information.

# MainGUI
I have decided to separate the `MainGUI` GUI elements and the `MainGUI` logic into separate files. This will give me better flexibility and easier access when modifying the visuals.

# TODO
Since the software and `MainGUI` logic are currently intertwined, I will start by separating the `MainGUI` logic and rebuilding the methods in a new file (`MainGUILogic.py`). When using methods, `MainGUI` will call `MainGUILogic.method()` or pass the method name as required by AppJar.
</details>