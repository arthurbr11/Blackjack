import game
import model


def play(test: bool = False, split: bool = False, test_players: list = None, nb_round: int = -1,
         counting_method: int = 0):  # Parameters used in the case of a test (in test.py)
    model.SHOW_PYGAME = False

    if test:
        model.SHOW_TERMINAL = False
        nb_player = len(test_players)
    else:
        model.SHOW_TERMINAL = True
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


def play_with_pygame():
    import display_function
    model.SHOW_TERMINAL = False
    model.SHOW_PYGAME = True

    window, window_height, window_width, white_rect, white_rect_height, background = display_function.init_display()
    windows_param = [window, window_height, window_width, white_rect, white_rect_height, background]
    print(type(window))
    list_players = display_function.get_start(windows_param)[1]
    nb_ia = 0
    players = []
    for i in range(len(list_players)):
        if len(list_players[i]) == 1:
            players.append(model.AI(nb_ia))
            nb_ia += 1
        else:
            players.append(model.HumanPlayer(list_players[i][1]))
    party = game.Game(players)
    while True:
        party.play_round(windows_param)
        is_empty = party.reset(windows_param)
        if is_empty:
            display_function.close_the_game(windows_param)
            return
        if display_function.ask_want_to_continue(windows_param):
            display_function.close_the_game(windows_param)
            return


if __name__ == "__main__":
    play_with_pygame()
