import model

NB_DECK = 6


class Game:
    def __init__(self, players: [model.Player]):
        self._deck = model.Deck(NB_DECK)
        self._players = players
        self._dealer = model.Dealer()
        self.deck.perfect_shuffle()

    @property
    def deck(self) -> model.Deck:
        return self._deck

    @property
    def players(self) -> [model.Player]:
        return self._players

    @property
    def dealer(self) -> model.Dealer:
        return self._dealer

    def reset(self):
        """
        We set the hand of the dealer and each player empty.
        """
        self._dealer.reset()

        Player_copy = []
        for player in self.players:
            if not isinstance(player, model.AliasPlayer):
                player.reset()
                Player_copy.append(player)
            else:
                if player.index_hand == 1:
                    player.owner.reset()
                    Player_copy.append(player.owner)

        self._players = Player_copy.copy()

    def results(self) -> {str: str}:
        """
        We return a dictionary with the player's name for key and is statut for value.
        """
        results = {}
        value_dealer = self.dealer.value()
        if value_dealer > 21:
            for player in self.players:
                value_player = player.value()
                if value_player > 21:
                    results[player.name] = "bust"
                else:
                    results[player.name] = "win"
        else:
            for player in self.players:
                value_player = player.value()
                if value_player > 21:
                    results[player.name] = "bust"
                elif player.value() > self.dealer.value():
                    results[player.name] = "win"
                elif player.value() < self.dealer.value():
                    results[player.name] = "loose"
                else:
                    results[player.name] = "even"  # The dealer and the player are even
        return results

    def first_distribution(self):
        """
        The dealer distributes one card for his self and two cards for each players and after his second card.
        """
        self._dealer.draw(self.deck)  # The dealer draws one
        for i in range(0, 2):  # Each player draws two cards
            for player in self.players:
                player.draw(self.deck)
        self._dealer.draw_without_showing(self.deck)

    def play_player(self, player, i):
        """
        This function make a player play. :param i: :param player:
        To test if the split method work well change 52 by
        16 in the classe deck and add a condition that card.value==10 we will ve the possibility to split each time
        """
        print(player.name + ": it's your turn to play !!")
        player.show_hand()
        keep_going = True
        while keep_going:
            keep_going = False
            if not isinstance(player, model.AI):
                print("1st Option : Stand")
                print("2nd Option : Hit")
                if player.pair():
                    print("3rd Option : Split")
                chosen_option = int(input("Which option do you choose ? (Put the number)"))
                if chosen_option == 2:
                    player.draw(self.deck)
                    if player.value() < 21:
                        keep_going = True
                elif chosen_option == 3:
                    player_father = self._players.pop(i)
                    index = 1
                    if isinstance(player_father, model.AliasPlayer):
                        player_father.owner.nb_hand += 1
                        for k in range(0, 2):
                            alias_player = model.AliasPlayer(player_father.owner, player_father.index_hand + k)
                            alias_player.hand.append(player_father.hand[k])
                            self._players.insert(i, alias_player)
                            index += self.play_player(alias_player, i)
                    else:
                        player_father.nb_hand += 1
                        for k in range(0, 2):
                            alias_player = model.AliasPlayer(player_father, player_father.nb_hand - (1 - k))
                            alias_player.hand.append(player_father.hand[k])
                            self._players.insert(i, alias_player)
                            index += self.play_player(alias_player, i)
                    return index
            # if isinstance(player, model.AI):
        return 0

    def play_round(self):
        """
        This function is the main loop for each round.
        """
        self.first_distribution()
        players_copy = self._players.copy()
        index = 0
        for (i, player) in enumerate(players_copy):
            index += self.play_player(player, i + index)

        self.dealer.play(self.deck)
        results = self.results()

        for player_name, message in results.items():
            print(player_name + " you have " + message)
