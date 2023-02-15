# Blackjack

***
# 0. How to run the code

To just paly the game run the field **main.py** in the folder src.

To have the terminal change **play_with_pygame** to **play**.

To run the test you have to run the field **test.py** in the folder test.

# 1. Introduction
  
In this project, we will code the BlackJack game interface: [BlackJack : régles et déroulement du jeu](https://www.le-black-jack.com/regles-du-blackjack.html). Then we will code an AI that can play the game against other players. We first planned to have a working game without any wagering. Therefore we will code the number of players, their names and the different features of BlackJack. These features are for example: Split (we split our deck in two), Remain or draw a card. We will also code the graphical interface using the pygame library. Then we will see how to set up a betting system. We will then make AIs play our game against the users. We aim to do different card counts with our AI to know the best counting method, to know when to get out of the game...  Finally we would like to study different parameters on the victory rate of our AI (deck with many cards, human vs. completely random card shuffle...). 


# 2. Structure of the code

To modelize the BlackJack game, we structured it through two main files : 

2.1. **model.py** : At a low granulity level, describing the elementary pieces of this card game.
The three first classes are : Card, Color, Rank. These ones are used to modelize the cards of the game.
After that, a class is defined for the Deck. The class modelizes the BlackJack card stack handled by the dealer. Moreover, it incorporates (human or perfect) shuffling methods and a "red card", to know when the dealer has to shuffle the deck as in the real game.
We then have players classes which define AI or human player because the two can play to this game. Players are defined by a lot of features : his name, his hand, his number of hands, his money, the maximal possible value of his hand, and all the mooves he can do in a party. Then there is a class to describe the dealer, and two classes to differentiate between AI and human players.
    
2.2. **game.py**:  From a more global standpoint, gathers all the methods and objects to have a functionnal usable game. 
In this file, the players, the dealer and their decks are described with the previous methods. It then describes the overall operations of the game.
In the code, we first code functions for players, deck and initialization of the game. Then the three couting methods are linked by the class **increase_count** that chooses the counting method to increase the count of the game. It follows with the class **reset** which restart the game ( no card for players, setting for dealer's hand).
Secondly, the code describes the centre of the game with the distribution of the cards, the choice of the players' bets and the result of the game. 
These two files describe all the technical part of the code to make the game work properly.
            
    
# 3. Graphical interface 
The graphical interface is strongly linked to the structure of the code. In fact, players' actions in the graphical interface are directly treated by the two main  files to make the game work. This part has been done page by page in relation to the structure of the code to make each page work before moving on to the next
The file that describes all of these operations is **display**. In this file there are a lot of classes and functions to describe all the graphical part of the game. For instance, at the beginning the class button describes all the buttons on which players can pressed to trigger an action. 
For the first and second pages, functions describe the number of players, their type (AI or Human) and their name if they are human.
Then, the game starts and the rest of the code describes the dynamic of the game with the movement of card, the bets, the actions of players...
At the end, the player can choose both to continue of to stop the game.

# 4. Data Analysis

The file **analysis_proba** allows us to better understand the game and to analyze counting methods. The five functions in the file retrives data from the game and plot curbs to analyze counting methods. The code is quite explicit : the first function extract data from the game of AI players. Then the second function create the list of AI money to each party and the last functions plot the data and calculate the moment when the AI should leave the game to maximize the gain.
# 5. Features 
The global operation of the game works, so we decided to make the player's experience of the game more enjoyable. To do so, the idea was to add music on the game, when a card is dealt, or some other actions...In addition, we also tried to add some flexibility for the user so he could change his bet when he have to choose it (not fix when you clik).


