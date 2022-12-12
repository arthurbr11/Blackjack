import game
import model


def play(test=False, split=False, test_players=[], nb_round=-1, counting_method=0):  # Parameters used in the case of
    # a test (in game_test.py)
    if test:
        nb_player = len(test_players)
    else:
        nb_player = int(input("Number of players"))
    players = []
    nb_ia = 0
    if not test:
        for i in range(nb_player):
            mode = int(input("Ia or human ? (0 IA, 1 human)"))
            if mode == 0:
                players.append(model.AI(nb_ia))
                nb_ia += 1
            else:
                name = input("Name player : ")
                players.append(model.HumanPlayer(name))
    else:
        for player_name in test_players:
            if player_name == "IA":
                players.append(model.AI(nb_ia))
                nb_ia += 1
            else:
                players.append(model.HumanPlayer(player_name))

    party = game.Game(players, test=test, split=split, counting_method=counting_method)
    turn = 0

    while nb_round == -1 or turn < nb_round:
        turn += 1
        party.play_round()
        is_empty = party.reset()
        if is_empty:
            print("END OF THE GAME NO MORE PLAYER")
            return
        choice = 0
        if not test:
            choice = int(input("Do you want to continue ? (0 Yes, 1 No)"))
        if choice == 1:
            print("END OF THE GAME")
            return


if __name__ == "__main__":
    play()
