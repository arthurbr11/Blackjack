import model

NB_DECK = 8


class Game:
    def __init__(self, players: [model.Player]):
        self._deck = model.Deck(NB_DECK)
        self._players = players
        self._dealer = model.Dealer()
        self._count = 0  # Card count, depending on the counting methods
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

    @property
    def count(self) -> int:
        return self._count

    def increase_count_hi_lo(self, card: model.Card):
        if 2 <= card.value <= 6:
            self._count += 1
        elif card.value == 1 or card.value == 10:
            self._count += -1

    def increase_count_ko(self, card: model.Card):
        if 2 <= card.value <= 7:
            self._count += 1
        elif card.value == 1 or card.value == 10:
            self._count += -1

    def increase_count_omega2(self, card: model.Card):
        if card.value == 2 or card.value == 3 or card.value == 7:
            self._count += 1
        elif 4 <= card.value <= 6:
            self._count += 2
        elif card.value == 9:
            self._count += -1
        elif card.value == 10:
            self._count += -2

    def reset(self,WINDOWS=0):
        """
        We set the hand of the dealer and each player empty.
        """
        self._dealer.reset()

        player_copy = []
        for player in self.players:
            if not isinstance(player, model.AliasPlayer):
                if player.money != 0:
                    player.reset()
                    player_copy.append(player)
                elif model.SHOW_TERMINAL:
                    print(f'{player.name} you are out of the game not enough money for you')
                else:
                    0#display.show_looser(player,WINDOWS)
            else:
                if player.index_hand == 1:
                    player.owner.reset()
                    player_copy.append(player.owner)

        self._players = player_copy.copy()
        self._count = 0  # When the dealer shuffles the deck, we reset the count to 0
        if len(self.players) == 0:
            return True
        return False

    def results(self) -> {str: str}:
        """
        :return: a dictionary with the player's name for key and is statut for value.
        """
        results = {}
        value_dealer = self.dealer.value()
        if value_dealer > 21:
            for player in self.players:
                value_player = player.value()
                if value_player > 21:
                    results[player.name] = "bust"
                else:
                    results[player.name] = player.win_money()
        else:
            for player in self.players:
                value_player = player.value()
                if value_player > 21:
                    results[player.name] = "bust"
                elif player.value() > self.dealer.value():
                    results[player.name] = player.win_money()
                elif player.value() < self.dealer.value():
                    results[player.name] = "loose"
                else:
                    results[player.name] = player.even_money()  # The dealer and the player are even

        return results

    def choose_bet(self,WINDOWS):
        for player in self.players:
            if isinstance(player, model.HumanPlayer):
                if model.SHOW_TERMINAL:
                    print(f'{player.name}: Your current money is {player.money}')
                    player.bet = int(input("What is your bet ?"))
                else:
                    player.bet =0#display.get_bet(player,WINDOWS) A faire afficher les jetons actuels avce le nom du gars et quel est son bet retourne un entier
            elif isinstance(player, model.AI):
                bet = int(player.money / 10 * (1 + (self.count / NB_DECK)))
                if bet != 0:
                    player.bet = int(player.money / 10 * (1 + (self.count / NB_DECK)))
                else:
                    player.bet = player.money
            player.money -= player.bet

    def first_distribution(self,WINDOWS):
        """
        The dealer distributes one card for his self and two cards for each players and after his second card.
        """
        self._dealer.draw(self.deck,WINDOWS)  # The dealer draws one
        for i in range(0, 2):  # Each player draws two cards
            for player in self.players:
                player.draw(self.deck,WINDOWS)
        self._dealer.draw_without_showing(self.deck,WINDOWS)

    def play_player(self, player: model.Player, i: int,WINDOWS) -> int:
        """
        This function make a player play.
        To test if the split method work well change 52 by
        16 in the classe deck and add a condition that card.value==10 we will have the possibility to split each time

        :param i: this index allow us to know where we are in the list to pop the good element
        :param player: this is the player who is about to play
        :return: the number of elements we have add to the list

        """
        if model.SHOW_TERMINAL:
            print(player.name + ": it's your turn to play !!")
            player.show_hand(WINDOWS)
        else:
            0# display.round_of(player,WINDOWS)
        keep_going = True
        while keep_going:
            keep_going = False
            chosen_option = 0
            if (isinstance(player, model.HumanPlayer) and not isinstance(player, model.AliasPlayer)) or (
                    isinstance(player, model.AliasPlayer) and isinstance(player.owner, model.HumanPlayer)):
                chosen_option = player.show_possibilities(WINDOWS)
            elif isinstance(player, model.AI) or (
                    isinstance(player, model.AliasPlayer) and isinstance(player.owner, model.AI)):
                chosen_option = player.choose_option_ai_cheat(self.count)
            if chosen_option == 2:
                self.increase_count_omega2(player.draw(self.deck,WINDOWS))
                if player.value() < 21:
                    keep_going = True
            if chosen_option == 3:
                player.double()
                self.increase_count_omega2(player.draw(self.deck,WINDOWS))
                if player.value() < 21:
                    keep_going = True
            elif chosen_option == 4:
                player_father = self._players.pop(i)
                index = 1
                if isinstance(player_father, model.AliasPlayer):
                    player_father.owner.nb_hand += 1
                    for k in range(0, 2):
                        alias_player = model.AliasPlayer(player_father.owner, player_father.index_hand + k * index)
                        if k == 0:
                            alias_player.owner.money -= alias_player.bet
                        alias_player.hand.append(player_father.hand[k])
                        self._players.insert(i, alias_player)
                        index += self.play_player(alias_player, i,WINDOWS)
                else:
                    player_father.nb_hand += 1
                    for k in range(0, 2):
                        alias_player = model.AliasPlayer(player_father, player_father.nb_hand - (1 - k))
                        alias_player.hand.append(player_father.hand[k])
                        self._players.insert(i, alias_player)
                        index += self.play_player(alias_player, i,WINDOWS)
                return index
        return 0

    def play_round(self,WINDOWS=0):
        """
        This function is the main loop for each round.
        """
        self.choose_bet(WINDOWS)
        self.first_distribution(WINDOWS)
        players_copy = self._players.copy()
        index = 0
        for (i, player) in enumerate(players_copy):
            index += self.play_player(player, i + index,WINDOWS)

        self.dealer.play(self.deck,WINDOWS)
        results = self.results()

        if model.SHOW_TERMINAL:
            for player_name, message in results.items():
                print(player_name + " you have " + message)
        else:
            0#display.show_results(results,WINDOWS)
        return results
