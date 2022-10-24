import game
import model


def play():
    want_play = True
    nb_player = int(input("Nubmber of players"))
    players = []
    nb_IA = 0
    for i in range(nb_player):
        mode = int(input("Ia or human ? (0 IA, 1 human)"))
        if mode == 0:
            players.append(model.AI(nb_IA))
            nb_IA += 1
        else:
            name = input(f"Name player : ")
            players.append(model.HumanPlayer(name))
    Party = game.Game(players)
    while want_play:
        Party.play_round()
        choice = int(input("Do you want to continue ? (0 Yes, 1 No)"))
        if choice == 1:
            want_play = False
            print("END OF THE GAME")


if __name__ == '__main__':
    play()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
