import game
import model
import tools_json

def play_IA(nb_players,nb_round):
    nb_player = nb_players
    players = []
    nb_IA = 0
    for i in range(nb_player):
        players.append(model.AI(nb_IA))
        nb_IA += 1
    data={'parameters':{'nb_players':nb_players,'nb_round':nb_round}}
    party = game.Game(players)
    for k in range(nb_round):
        data[f'round {k}']={}
        party.play_round()
        for i in range(len(party.players)):
            data[f'round {k}'][f'{party.players[i].name}']={}
            data[f'round {k}'][f'{party.players[i].name}']['bet']=party.players[i].bet
            if party.players[i].money!=-1:
                data[f'round {k}'][f'{party.players[i].name}']['money']=party.players[i].money
        party.reset()
        for i in range(nb_player):
            if f'{party.players[i].name}' not in data[f'round {k}'].keys():
                data[f'round {k}'][f'{party.players[i].name}'] = {'money':party.players[i].money}

    return data

data=play_IA(int(input('Nb_players')),int(input('Nb_round')))
tools_json.create_json(data,'test')