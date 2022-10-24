import model

NB_DECK = 6


class Game:

    def __init__(self, players: [model.Player()]):
        self.deck = model.Deck(NB_DECK)
        self._players = players
        self._dealer = model.Dealer

    @property
    def players(self) -> [model.Player]:
        return self._players

    @property
    def dealer(self) -> model.Dealer:
        return self._dealer

    def winners(self):
        winners = {}
        for player in self.players:
            if player.value() > self.dealer.value():
                winners[player._name]='win'
            elif player.value() < self.dealer.value():
                winners[player._name]='loose'
            else:
                winners[player._name]='even'  # The dealer and the player are even
        return winners

    def play(self):
        keep_going = True
        while keep_going:
            keep_going = False
            for player in self.players:
                if player.value() < 21:
                    if isinstance(player, model.HumanPlayer):
                        print("1st Option : Stand")
                        print("2nd Option : Hit")
                        if player.pair():
                            print("3rd Option : Split")
                    chosen_option = input("Which option do you choose ?")
                    if chosen_option == 2:
                        player.draw(self.deck)
                     # elif chosen_option == 3:
                     # if isinstance(player, model.AI):
