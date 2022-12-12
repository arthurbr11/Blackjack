# Blackjack

***
# 1. Introduction
  
In this project, we will code the BlackJack game interface: [BlackJack : régles et déroulement du jeu](https://www.le-black-jack.com/regles-du-blackjack.html). Then we will code an AI that can play the game against other players. We first planned to have a working game without any wagering. We will therefore code the number of players, their names and the different features of BlackJack. These features are for example: Split (we split our deck in two), Remain or draw a card. We will also code the graphical interface using the pygame library. Then we will make AIs play our game against the users. Then we will see how to set up a betting system. Finally we would like to code an AI that counts cards and study different parameters on the victory rate of our AI (deck with many cards, human vs. completely random card shuffle...).


# 2. Structure of the code

To modelize the BlackJack game, we structured it through two main files : 

2.1. **model.py** : At a low granulity level, describing the elementary pieces of this card game. This file is decomposed in 8 classes. 
The three first classes are : Card, Color, Rank. These ones are used to modelize the cards of the game.
After that, a class is defined for the Deck. The classe modelizes the BlackJack card stack handled by the dealer. Moreover, it incorporates (human or perfect) shuffling methods and a "red card", to know when the dealer has to shuffle the deck as in the real game.
We then have players classes which define AI or human player because the two can play to this game.
    
2.2. **game.py**:  From a more global standpoint, gathers all the methods and objects to have a functionnal usable game. 
In this file, the players, the dealer and their decks are described with the previous methods. It then describes the overall operations of the game. Finally, we return the winner of the game 
            
                 


# 3. Interface graphique
Nous avons ensuite la volonté de produire une interface graphique pour permettre à l'utilisateur de jouer. Nous utilisons pour ceci la bibliothèque pygame.


# 1. Introduction

1. **Objectifs** :
    - Executable(Joueur humain, IA)
    - IA avec comptage de cartes

2. **Cheminement** :
    - Structure de base
    - BlackJack fonctionnel sur le terminal sans mise
    - ajout des mises
    - ajout IA comptage de carte
    - Interface graphique
    -  Features

# 2. Structure du jeu 
    - model.py (classes et methodes expliquées)
    - game.py
    
# 3. Interface Graphique 

# 4. Data Analysis

# 5. Features 
    - Music
    - Aide au joueur avec IA (tickets bonus)

# 6. Conclusion
 

