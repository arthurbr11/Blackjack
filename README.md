# Blackjack

***
# 1. Introduction
Dans ce projet, nous allons coder l'interface de jeu du [BlackJack : régles et déroulement du jeu](https://www.le-black-jack.com/regles-du-blackjack.html). Ensuite nous coderons une IA qui pourra jouer au jeu contre d'autres joueurs. Nous comptons premièrement avoir un jeu fonctionnel sans mise. Nous allons donc coder au départ le nombre de joueurs, leur noms et les différentes fonctionnalités du BlackJack. Ces fonctionnalités sont par exemple : Split (on split notre deck en deux), Rester ou encore tirer une carte. Nous allons aussi coder l'interface graphique à l'aide de la bibliothèque pygame. Ensuite nous allons faire jouer des IA à notre jeu contre les utilisateurs. Nous verrons ensuite pour mettre en place un système de mise. Enfin nous voudrions coder une IA qui compte les cartes et etudier differents paramètres sur le taux de victoire de notre IA (deck avec beaucoup de cartes, mélange de carte humain contre complètement aléatoire...)  

# 2. Structure of the code
To modelize the BlackJack game, we structured it through two main files : 
      -model.py : at a low granulity level, describing the elementary pieces of this card game
            *Card, Color, Rank : used to modelize the cards of the game
            *Deck : modelizes the BlackJack card stack handled by the dealer -> incorporates (human or perfect) shuffling methods and a "red card", to know when the                                                                                     dealer has to shuffle the deck
            *Player : 
            
      -game.py : from a more global standpoint, gathers all the methods and objects to have a functionnal usable game
      


# 3. Interface graphique
Nous avons ensuite la volonté de produire une interface graphique pour permettre à l'utilisateur de jouer. Nous utilisons pour ceci la bibliothèque pygame.
