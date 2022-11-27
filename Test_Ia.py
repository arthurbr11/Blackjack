import game
import model
import tools_json
import matplotlib.pyplot as plt


def play_extract_data_ia(nb_players, nb_round_theoric):
    nb_player = nb_players
    players = []
    nb_IA = 0
    for i in range(nb_player):
        players.append(model.AI(nb_IA))
        nb_IA += 1
    data = {
        'parameters': {'nb_players': nb_players, 'nb_round_theo': nb_round_theoric, 'nb_round_reel': nb_round_theoric}}
    party = game.Game(players)
    for k in range(nb_round_theoric):
        data[f'round {k}'] = {}
        result = party.play_round()
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
    List_ia_money = []
    for i in range(data['parameters']['nb_players']):
        List_ia_money.append([])
        for k in range(data['parameters']['nb_round_reel']):
            if f'IA number{i}' in data[f'round {k}'].keys():
                List_ia_money[i].append(data[f'round {k}'][f'IA number{i}']['money'])
            else:
                List_ia_money[i].append(0)
        print(List_ia_money)

    return List_ia_money


def plot_money(List_ia_money):
    X = [k for k in range(len(List_ia_money[0]))]
    for i in range(len(List_ia_money)):
        plt.plot(X, List_ia_money[i])
    plt.show()


def limit_rate_reward(List_ia_money, rate):
    Better_than_rate = [False] * len(List_ia_money)
    for i in range(len(List_ia_money)):
        for k in range(len(List_ia_money[0])):
            if (List_ia_money[i][k] / model.INITIAL_MONEY) >= rate:
                Better_than_rate[i] = True
    return Better_than_rate


nb_players_ask = int(input('Nb_players'))
nb_round_theo = int(input('Nb_round'))

data_ia = play_extract_data_ia(nb_players_ask, nb_round_theo)
tools_json.create_json(data_ia, 'test')

list_result = get_list_of_ia_money(data_ia)
"""print(list_result)"""
plot_money(list_result)

list_better = limit_rate_reward(list_result, 1.5)
print(list_better)
