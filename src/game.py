import model
import display

NB_DECK = 8


class Game:
    def __init__(self, players: [model.Player], counting_method=0, test=False, split=False):
        self._deck = model.Deck(NB_DECK, split=split)
        self._players = players
        self._dealer = model.Dealer()
        self._count = 0  # Card count, depending on the counting methods
        self.deck.perfect_shuffle()
        self._test = test
        self._counting_method = counting_method
        if split:
            model.SIZE_DECK = 16

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

    def increase_count(self, card: model.Card):
        """
        Select the counting_method to increase the count of the game (_counting_method = 0 : no counting)
        :param card: the card that has been drawn
        """
        if self._counting_method == 1:
            self.increase_count_hi_lo(card)
        elif self._counting_method == 2:
            self.increase_count_ko(card)
        elif self._counting_method == 3:
            self.increase_count_omega2(card)

    def reset(self, windows_param: list = None) -> bool:
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
                elif model.SHOW_PYGAME:
                    display.show_looser(player, windows_param)
            else:
                if player.index_hand == 1:
                    player.owner.reset()
                    player_copy.append(player.owner)

        self._players = player_copy.copy()
        self._count = 0  # When the dealer shuffles the deck, we reset the count to 0
        if len(self.players) == 0:
            return True
        return False

    def results(self) -> {str: [str, int]}:
        """
        :return: a dictionary with the player's name for key and his result and the money the owner have after this
        round for value.
        """
        results = {}
        value_dealer = self.dealer.value()
        if value_dealer > 21:
            for player in self.players:
                value_player = player.value()
                if value_player > 21:
                    results[player.name] = ["bust", player.owner.money]
                else:
                    results[player.name] = [player.win_money(), player.owner.money]
        else:
            for player in self.players:
                value_player = player.value()
                if value_player > 21:
                    results[player.name] = ["bust", player.owner.money]
                elif player.value() > self.dealer.value():
                    results[player.name] = [player.win_money(), player.owner.money]
                elif player.value() < self.dealer.value():
                    results[player.name] = ["loose", player.owner.money]
                else:
                    results[player.name] = player.even_money()  # The dealer and the player are even

        return results

    def choose_bet(self, windows_param: list, test=False):
        for player in self.players:
            if isinstance(player, model.HumanPlayer) and not test:
                if model.SHOW_TERMINAL:
                    print(f'{player.name}: Your current money is {player.money}')
                    player.bet = int(input("What is your bet ?"))
                elif model.SHOW_PYGAME:
                    player.bet = display.get_bet(player,
                                                 windows_param)
            elif isinstance(player, model.HumanPlayer) and test:  # Used to test the function in test_model.py
                player.bet = player.money // 2
            elif isinstance(player, model.AI):
                bet = int(player.money / 10 * (1 + (self.count / NB_DECK)))
                if bet != 0:
                    player.bet = int(player.money / 10 * (1 + (self.count / NB_DECK)))
                else:
                    player.bet = player.money
            player.money -= player.bet

    def first_distribution(self, windows_param: list):
        """
        The dealer distributes one card for his self and two cards for each players and after his second card.
        """
        self._dealer.draw(self, windows_param, True)  # The dealer draws one
        for i in range(0, 2):  # Each player draws two cards
            for player in self.players:
                player.draw(self, windows_param, True)
        self._dealer.draw_without_showing(self)
        if model.SHOW_PYGAME:
            display.show_first_distribution(self, windows_param)

    def play_player(self, player: model.Player, i: int, windows_param: list) -> int:
        """
        This function make a player play.
        To test if the split method work well change 52 by
        16 in the class deck and add a condition that card.value==10 we will have the possibility to split each time

        :param windows_param:
        :param i: this index allow us to know where we are in the list to pop the good element
        :param player: this is the player who is about to play
        :return: the number of elements we have add to the list

        """
        if model.SHOW_TERMINAL:
            print(player.name + ": it's your turn to play !!")
            player.show_hand(self, windows_param)
        elif model.SHOW_PYGAME:
            display.round_of(player, self, windows_param)
        keep_going = True
        while keep_going:
            keep_going = False
            chosen_option = 0
            if (isinstance(player, model.HumanPlayer) and not isinstance(player, model.AliasPlayer)) or (
                    isinstance(player, model.AliasPlayer) and isinstance(player.owner, model.HumanPlayer)):
                if not self._test:
                    chosen_option = player.show_possibilities(windows_param)
                else:
                    chosen_option = player.choose_option_ai_cheat(self.count)
            elif isinstance(player, model.AI) or (
                    isinstance(player, model.AliasPlayer) and isinstance(player.owner, model.AI)):
                chosen_option = player.choose_option_ai_cheat(self.count)
            if chosen_option == 2:
                self.increase_count(player.draw(self, windows_param))
                if player.value() < 21:
                    keep_going = True
            if chosen_option == 3:
                player.double()
                self.increase_count(player.draw(self, windows_param))
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
                        index += self.play_player(alias_player, i, windows_param)
                else:
                    player_father.nb_hand += 1
                    for k in range(0, 2):
                        alias_player = model.AliasPlayer(player_father, player_father.nb_hand - (1 - k))
                        if k == 0:
                            alias_player.owner.money -= alias_player.bet
                        alias_player.hand.append(player_father.hand[k])
                        self._players.insert(i, alias_player)
                        index += self.play_player(alias_player, i, windows_param)
                return index
        return 0

    def play_round(self, windows_param=None) -> {str: str}:
        """
        This function is the main loop for each round.
        """
        self.choose_bet(windows_param)
        self.first_distribution(windows_param)
        players_copy = self._players.copy()
        index = 0
        for (i, player) in enumerate(players_copy):
            index += self.play_player(player, i + index, windows_param)

        self.dealer.play(self, windows_param)
        results = self.results()

        if model.SHOW_TERMINAL:
            for player_name, [message, _] in results.items():
                print(player_name + " you have " + message)
        elif model.SHOW_PYGAME:
            display.show_results(self, results, windows_param)

        return results
