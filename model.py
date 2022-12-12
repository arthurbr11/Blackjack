import enum
import random

INITIAL_MONEY = 1000
SIZE_DECK = 52

COUNT_MIN = 4

SHOW_TERMINAL = False
SHOW_PYGAME = False


class Color(enum.Enum):
    CLUBS = "clubs"
    DIAMONDS = "diamonds"
    HEARTS = "hearts"
    SPADES = "spades"


class Rank(enum.Enum):
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13


class Card:
    def __init__(self, color: Color, rank: Rank):
        self._color = color
        self._rank = rank

    @property
    def color(self) -> Color:
        return self._color

    @property
    def rank(self) -> Rank:
        return self._rank

    @property
    def value(self) -> int:
        """
        :return: the value of the card, with one for an ace.
        """
        if (
                self._rank == Rank.JACK
                or self._rank == Rank.QUEEN
                or self._rank == Rank.KING
        ):
            return 10
        else:
            return self._rank.value

    def __str__(self) -> str:
        return str(self.rank).lstrip("Rank.") + " of " + self.color.value


class Deck:
    def __init__(self, nb_decks: int, split=False):
        self._nb_decks = nb_decks
        self._cards = []
        for _ in range(0, nb_decks):
            for color in Color:
                for rank in Rank:
                    if Card(color,
                            rank).value == 10 or not split:  # When we test the split function, we keep in the deck
                        # only cards with a value of 10
                        self._cards.append(Card(color, rank))
        self._stop_index = random.randrange(
            SIZE_DECK, SIZE_DECK * (nb_decks - 1)
        )  # Position of the red card in the deck : the dealer shuffles the deck when drawn

    @property
    def cards(self) -> [Card]:
        return self._cards

    @property
    def stop_index(self) -> int:
        return self._stop_index

    @property
    def nb_decks(self) -> int:
        return self._nb_decks

    def stop_index_decrease(self):
        self._stop_index += -1

    def random_stop_index(self):
        self._stop_index = random.randrange(SIZE_DECK, SIZE_DECK * (self.nb_decks - 1))

    def reset(self):
        self._cards = []
        for _ in range(0, self.nb_decks):
            for color in Color:
                for rank in Rank:
                    self._cards.append(Card(color, rank))

    def perfect_shuffle(self):
        """
        Shuffles the deck in an unpredictable way.
        """
        random.shuffle(self._cards)
        self.random_stop_index()

    def draw(self) -> Card:
        """
        This function draw a card of the deck

        :return: the card which have been drawn
        """
        if (
                self.stop_index > 0
        ):  # If the dealer hasn't reached the red card yet, he draws
            self.stop_index_decrease()
            return self._cards.pop()
        else:  # Else he shuffles the deck and then draws one
            self.reset()
            self.perfect_shuffle()
            self.stop_index_decrease()
            return self._cards.pop()


class Player:
    def __init__(self, name: str):
        self._hand = []
        self._name = name
        self._nb_hand = 1
        self._money = INITIAL_MONEY
        self._bet = 0
        self.stop_splitting = False  # We stop splitting when the player reaches 20 hands : used in test functions

    @property
    def owner(self):
        return self

    @property
    def name(self) -> str:
        return self._name

    @property
    def hand(self) -> [Card]:
        return self._hand

    @property
    def nb_hand(self) -> int:
        return self._nb_hand

    @property
    def money(self) -> int:
        return self._money

    @property
    def bet(self) -> int:
        return self._bet

    @bet.setter
    def bet(self, new_bet: int):
        self._bet = new_bet

    @money.setter
    def money(self, new_money: int):
        self._money = new_money

    @nb_hand.setter
    def nb_hand(self, new_nb_hand: int):
        self._nb_hand = new_nb_hand

    def pair(self) -> bool:
        if len(self.hand) != 2:
            return False
        return self.hand[0].value == self.hand[1].value

    def reset(self):
        self._hand = []
        self._nb_hand = 1
        self.bet = 0

    def value(self) -> int:
        """
        :return: the maximal possible value of the player's hand, below 21.
        """
        values = [0]  # Stocks the different possible values of the player's hand
        for card in self._hand:
            if card.rank == Rank.ACE:
                for i in range(0, len(values)):
                    values[i] += card.value  # We value the ace as 1 here
                    values.append(values[i] + 10)  # Or it can be valued as 11
            else:
                for i in range(0, len(values)):
                    values[i] += card.value
        if len(values) == 1:
            return values[0]
        else:
            values.sort()
            if values[0] > 21:
                return values[0]  # The player's hand value is beyond 21
            else:
                for i in range(
                        1, len(values)
                ):  # We compute the maximal possible value of the player's hand below 21
                    if values[i] > 21:
                        return values[i - 1]
                return values[len(values) - 1]

    def show_hand(self,WINDOWS):
        if SHOW_TERMINAL:
            print(self._name + ": have ", end="")
            for card in self._hand:
                print(card, end="")
                print(", ", end="")
            print(f"With a value of {self.value()} and a bet of {self._bet}")
        elif SHOW_PYGAME:
            0  # display.show_hand_player(self:(player),WINDOWS)

    def draw(self, deck: Deck,WINDOWS) -> Card:
        """
        The player draws the top card of the deck and adds it to his hand.
        """
        drew_card = deck.draw()
        self._hand.append(drew_card)
        self.show_hand(WINDOWS)
        return drew_card

    def win_money(self) -> str:
        if len(self.hand) == 2 and self.value() == 21:
            self.owner.money += int(5 / 2 * self.bet)
            return "Blackjack !"
        else:
            self.owner.money += 2 * self.bet
            return "Won !"

    def even_money(self) -> str:
        self.owner.money += self.bet
        return "Even !"

    def double(self):
        self.owner.money -= self.bet
        self.bet += self.bet


class Dealer(Player):
    def __init__(self):
        super().__init__("DEALER")
        self.money = 0

    def draw(self, deck: Deck,WINDOWS) -> Card:
        """
        The dealer draws the top card of the deck and adds it to his hand.
        """
        drew_card = deck.draw()
        self._hand.append(drew_card)
        self.show_hand(WINDOWS)
        return drew_card

    def draw_without_showing(self, deck: Deck,WINDOWS):
        """
        The dealer draws the top card of the deck and adds it to his hand without showing because it's his 2nd card.
        """
        self._hand.append(deck.draw())
        if SHOW_PYGAME:
            0#display.show_hand_dealer_back(self:(dealer),WINDOWS)

    def play(self, deck: Deck,WINDOWS):
        """
        This function make a dealer play.
        """
        self.show_hand(WINDOWS)
        while self.value() < 17:
            self.draw(deck,WINDOWS)

    def show_hand(self,WINDOWS):
        if SHOW_TERMINAL:
            print(self._name + ": have ", end="")
            for card in self._hand:
                print(card, end="")
                print(", ", end="")
            print(f"With a value of {self.value()}")
        elif SHOW_PYGAME:
            0  # display.show_hand_dealer(self:(dealer),WINDOWS)


class HumanPlayer(Player):
    def __init__(self, name: str):
        super().__init__(name)

    def show_possibilities(self,WINDOWS) -> int:
        if SHOW_TERMINAL:
            print("1st Option : Stand")
            print("2nd Option : Hit")
            if self.owner.money >= self.bet:
                print("3rd Option : Double")
            if self.pair() and self.owner.money >= self.bet:
                print("4th Option : Split")
            return int(input("Which option do you choose ? (Put the number)"))
        elif SHOW_PYGAME:
            0#return(display.show_possibilities(self(HumanPlayer)),WINDOWS)

    def choose_option_test_classic(self) -> int:  # A faire
        """"
        This function will simulate a player choosing to stand, hit or spilt
        """
        if self.pair() and self.owner.money >= self.bet and not self.stop_splitting:
            return 4
        elif self.value() < 17:
            return 2
        else:
            return 1


class AI(Player):
    def __init__(self, nb: int):
        super().__init__('IA number' + str(nb))

    def choose_option_ai_classic(self) -> int:  # A faire
        """"
        This function will choose for the AI to stand, hit or spilt
        """
        if self.pair() and self.owner.money >= self.bet and not self.stop_splitting:
            return 4
        elif self.value() < 17:
            return 2
        else:
            return 1

    def choose_option_ai_cheat(self, count: int) -> int:
        """"
        This function will choose for the AI to stand, hit or spilt while counting cards
        """
        if self.pair() and self.owner.money >= self.bet and not self.stop_splitting:
            return 4
        elif self.value() < 14 and count > COUNT_MIN and self.owner.money >= self.bet:
            return 3
        elif self.value() > 14 and count < -COUNT_MIN:
            return 1
        elif self.value() < 17:
            return 2
        else:
            return 1


class AliasPlayer(AI, HumanPlayer):
    def __init__(self, player, i: int):
        Player.__init__(self, player.name + f" hand {i}")
        self._index_hand = i
        self._owner = player
        self.money = -1
        self.bet = player.bet
        if i == 20:
            player.stop_splitting = True  # After 20 splits, a player can't split anymore (only reached on tests
            # functions)

    @property
    def owner(self):
        return self._owner

    @property
    def index_hand(self) -> int:
        return self._index_hand
