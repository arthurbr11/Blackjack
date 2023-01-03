import main
import model
import analysis_proba


def global_game_test():
    """"
    This function globally tests the files model.py and test.py, running a game with 1 AI, with 1 Human, and a game with
    4 Human players and 4 AI on 10 rounds.
    Then we successively test each counting method with an AI.
    The program should first successfully run, and then the programmer can check on the terminal if the players
    properly played, following rules.
    """
    model.SHOW_TERMINAL = True
    main.play(test=True, test_players=["IA"], nb_round=10)
    main.play(test=True, test_players=["Human1"], nb_round=10)
    main.play(test=True, test_players=["IA", "IA", "Human1", "Human2", "IA", "IA", "Human3", "Human4"], nb_round=10)
    main.play(test=True, test_players=["IA"], nb_round=10, counting_method=1)  # Hi-Lo method
    main.play(test=True, test_players=["IA"], nb_round=10, counting_method=2)  # Ko method
    main.play(test=True, test_players=["IA"], nb_round=10, counting_method=3)  # Omega II method


def split_test():
    """
    This function tests the split feature, in extreme cases where players split a lot of times their hand. It tests
    it on AI and Human Players.
    NB : players stop splitting when they reach 20 hands. We chose arbitrarily chose 20 since it is highly unlikely and
    should be sufficient to detect any bug.
    """
    model.SHOW_TERMINAL = True
    main.play(test=True, split=True, test_players=["IA"], nb_round=10)
    main.play(test=True, split=True, test_players=["Human1"], nb_round=10)
    main.play(test=True, split=True, test_players=["IA", "IA", "Human1", "Human2", "IA", "IA", "Human3", "Human4"],
              nb_round=10)


def proba_plot_test(nb_players_ask: int, nb_round_theo: int, counting_method: int, limit_rate: float):
    data_ia = analysis_proba.play_extract_data_ia(nb_players_ask, nb_round_theo, counting_method)
    analysis_proba.tools_json.create_json(data_ia,
                                          f'test with {nb_players_ask} players playing with the counting method number '
                                          f'{counting_method} during {nb_round_theo} rounds if they still have money')
    # Creates a JSON file with all the data of the game that has been played.
    # One can check on this JSON file the evolution of the game, especially the evolutions of bets and money of
    # each player.

    list_result = analysis_proba.get_list_of_ia_money(data_ia)
    analysis_proba.plot_money(list_result)  # plots the evolution of the money of each AI during the game

    list_better = analysis_proba.limit_rate_reward(list_result, limit_rate)
    print(list_better)  # returns a list of bool, where list_better[i] is True if the ith player has exceeded k
    # times his initial stake  and False in the other case


def counting_method_efficiency_test(counting_method):
    analysis_proba.compute_proba_superior_rate(4, 500, 1.5, counting_method)


global_game_test()
# split_test()
# proba_plot_test(3, 500, 0, 1.5)
counting_method_efficiency_test(1)