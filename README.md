# Blackjack

***
# 1. Introduction
Nous allons donc coder au départ le nombre de joueurs, leur noms et les différentes fonctionnalités du BlackJack. Ces fonctionnalités sont par exemple : Split (on split notre deck en deux), Rester ou encore tirer une carte. Nous allons aussi coder l'interface graphique à l'aide de la bibliothèque pygame. Ensuite nous allons faire jouer des IA à notre jeu contre les utilisateurs. Nous verrons ensuite pour mettre en place un système de mise. Enfin nous voudrions coder une IA qui compte les cartes et etudier differents paramètres sur le taux de victoire de notre IA (deck avec beaucoup de cartes, mélange de carte humain contre complètement aléatoire...)  
In this project, we will code the BlackJack game interface: [BlackJack : régles et déroulement du jeu](https://www.le-black-jack.com/regles-du-blackjack.html). Then we will code an AI that can play the game against other players. We first planned to have a working game without any wagering. We will therefore code the number of players, their names and the different features of BlackJack. These features are for example: Split (we split our deck in two), Remain or draw a card. We will also code the graphical interface using the pygame library. Then we will make AIs play our game against the users. Then we will see how to set up a betting system. Finally we would like to code an AI that counts cards and study different parameters on the victory rate of our AI (deck with many cards, human vs. completely random card shuffle...)


# 2. Structure of the code
To modelize the BlackJack game, we structured it through two main files : 

1. **model.py** : At a low granulity level, describing the elementary pieces of this card game
    - Card, Color, Rank : used to modelize the cards of the game
    - Deck : modelizes the BlackJack card stack handled by the dealer -> incorporates (human or perfect) shuffling methods and a "red card", to know when the                                                                                     dealer has to shuffle the deck
    - Player :
    
2. **game.py**:  From a more global standpoint, gathers all the methods and objects to have a functionnal usable game
    - Card, Color, Rank : used to modelize the cards of the game
    - Deck : modelizes the BlackJack card stack handled by the dealer -> incorporates (human or perfect) shuffling methods and a "red card", to know when the                                                                                     dealer has to shuffle the deck
    - Player : 
            
                 


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
   2-  Features

# 2. Structure du jeu 
    - model.py (classes et methodes expliquées)
    - game.py
    
# 3. Interface Graphique 

# 4. Data Analysis

# 5. Features 
    - Music
    - Aide au joueur avec IA (tickets bonus)

# 6. Conclusion
 

