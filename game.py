import model

NB_DECK = 6


class Game:

    def __init__(self, players: [model.Player]):
        self.deck = model.Deck(NB_DECK)
        self._players = players
        self._dealer = model.Dealer()

    @property
    def players(self) -> [model.Player]:
        return self._players

    @property
    def dealer(self) -> model.Dealer:
        return self._dealer

    def winners(self) -> [model.Player]:
        winners = []
        for player in self.players:
            if player.value() > self.dealer.value():
                winners.append(player)
            elif player.value() < self.dealer.value():
                winners.append(self.dealer)
            else:
                winners.append(None)  # The dealer and the player are even
        return winners

    """The dealer distributes one card for his self and two cards for each players"""
    def first_distribution(self):
        self.dealer.draw(self.deck)  # The dealer draws one
        for i in range(0, 2):  # Each player draws two cards
            for player in self.players:
                player.draw(self.deck)


