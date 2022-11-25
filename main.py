import game
import model


def play():
    nb_player = int(input("Number of players"))
    players = []
    nb_IA = 0
    for i in range(nb_player):
        mode = int(input("Ia or human ? (0 IA, 1 human)"))
        if mode == 0:
            players.append(model.AI(nb_IA))
            nb_IA += 1
        else:
            name = input("Name player : ")
            players.append(model.HumanPlayer(name))
    party = game.Game(players)
    while True:
        party.play_round()
        is_empty = party.reset()
        if is_empty:
            print("END OF THE GAME NO MORE PLAYER")
            return
        choice = int(input("Do you want to continue ? (0 Yes, 1 No)"))
        if choice == 1:
            print("END OF THE GAME")
            return


if __name__ == "__main__":
    play()
