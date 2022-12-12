import game
import model
import tools_json
import matplotlib.pyplot as plt
from tqdm import tqdm


def play_extract_data_ia(nb_players, nb_round_theoric, counting_method):
    model.SHOW_TERMINAL = False
    model.SHOW_PYGAME = False
    nb_player = nb_players
    players = []
    nb_AI = 0
    for i in range(nb_player):
        players.append(model.AI(nb_AI))
        nb_AI += 1
    data = {
        'parameters': {'nb_players': nb_players, 'nb_round_theo': nb_round_theoric, 'nb_round_reel': nb_round_theoric}}
    party = game.Game(players, counting_method=counting_method)
    for k in range(nb_round_theoric):
        data[f'round {k}'] = {}
        result = party.play_round()
        data[f'round {k}']['Count'] = party.count
        for i in range(len(party.players)):
            data[f'round {k}'][f'{party.players[i].name}'] = {}
            data[f'round {k}'][f'{party.players[i].name}']['bet'] = party.players[i].bet
            data[f'round {k}'][f'{party.players[i].name}']['result'] = result[f'{party.players[i].name}']
            if party.players[i].money != -1:
                data[f'round {k}'][f'{party.players[i].name}']['money'] = party.players[i].money
        party.reset()
        for i in range(len(party.players)):
            if f'{party.players[i].name}' not in data[f'round {k}'].keys():
                data[f'round {k}'][f'{party.players[i].name}'] = {'money': party.players[i].money}
        if len(party.players) == 0:
            data['parameters']['nb_round_reel'] = k
            return data

    return data


def get_list_of_ia_money(data):
    list_ia_money = []
    for i in range(data['parameters']['nb_players']):
        list_ia_money.append([])
        for k in range(data['parameters']['nb_round_reel']):
            if f'IA number{i}' in data[f'round {k}'].keys():
                list_ia_money[i].append(data[f'round {k}'][f'IA number{i}']['money'])
            else:
                list_ia_money[i].append(0)
    return list_ia_money


def plot_money(list_ia_money):
    X = [k for k in range(len(list_ia_money[0]))]
    for i in range(len(list_ia_money)):
        plt.plot(X, list_ia_money[i])
    plt.show()


def limit_rate_reward(list_ia_money, rate):
    better_than_rate = [False] * len(list_ia_money)
    for i in range(len(list_ia_money)):
        for k in range(len(list_ia_money[0])):
            if (list_ia_money[i][k] / model.INITIAL_MONEY) >= rate:
                better_than_rate[i] = True
    return better_than_rate


def compute_proba_superior_rate(nb_player, nb_round, rate, counting_method):
    proba = [0] * nb_player
    for _ in tqdm(range(nb_round)):
        data = play_extract_data_ia(nb_player, 100000, counting_method)
        list_of_result = get_list_of_ia_money(data)
        list_of_better = limit_rate_reward(list_of_result, rate)
        for i in range(nb_player):
            if list_of_better[i]:
                proba[i] += 1
    for i in range(nb_player):
        proba[i] = proba[i] / nb_round
    print(proba)
    return proba



