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

    def results(self):
        winners = {}
        value_dealer = self.dealer.value()
        if value_dealer > 21:
            for player in self.players:
                value_player = player.value()
                if value_player > 21:
                    winners[player.name] = 'bust'
                else:
                    winners[player.name] = 'win'
        else:
            for player in self.players:
                value_player = player.value()
                if value_player > 21:
                    winners[player.name] = 'bust'
                elif player.value() > self.dealer.value():
                    winners[player.name] = 'win'
                elif player.value() < self.dealer.value():
                    winners[player.name] = 'loose'
                else:
                    winners[player.name] = 'even'  # The dealer and the player are even
        return winners

    def first_distribution(self):
        """
        The dealer distributes one card for his self and two cards for each players
        :return:
        """
        self._dealer.draw(self.deck)  # The dealer draws one
        for i in range(0, 2):  # Each player draws two cards
            for player in self.players:
                player.draw(self.deck)
        self._dealer.draw_without_showing(self.deck)

    def play_player(self, player):
        """
        This function make a player play.
        :param player:
        :return:
        """
        keep_going = True
        while keep_going:
            keep_going = False
            if isinstance(player, model.HumanPlayer):
                print("1st Option : Stand")
                print("2nd Option : Hit")
                if player.pair():
                    print("3rd Option : Split")
            chosen_option = int(input("Which option do you choose ? (Put the number)"))
            if chosen_option == 2:
                player.draw(self.deck)
                if player.value() < 21:
                    keep_going = True
            # elif chosen_option == 3:
            # if isinstance(player, model.AI):

    def play_dealer(self):
        print(self.dealer.name + ": have ", end='')
        for card in self._dealer.hand:
            print(card, end='')
            print(", ", end='')
        print(f"With a value of {self.dealer.value()}")
        while self.dealer.value() < 17:
            self.dealer.draw(self.deck)
            print(self.dealer.name + ": have ", end='')
            for card in self.dealer.hand:
                print(card, end='')
                print(", ", end='')
            print(f"With a value of {self._dealer.value()}")

    def play_round(self):
        self.first_distribution()
        for player in self._players:
            self.play_player(player)

        self.play_dealer()

        results = self.results()

        for player_name, message in results.items():
            print(player_name + " you have " + message)
