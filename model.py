import enum
import random


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
    def __init__(self, nb_decks: int):
        self._nb_decks = nb_decks
        self._cards = []
        for _ in range(0, nb_decks):
            for color in Color:
                for rank in Rank:
                    self._cards.append(Card(color, rank))
        self._stop_index = random.randrange(
            52, 52 * (nb_decks - 1)
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
        self._stop_index = random.randrange(52, 52 * (self.nb_decks - 1))

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

    @property
    def name(self) -> str:
        return self._name

    @property
    def hand(self) -> [Card]:
        return self._hand

    @property
    def nb_hand(self):
        return self._nb_hand

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

    def show_hand(self):
        print(self._name + ": have ", end="")
        for card in self._hand:
            print(card, end="")
            print(", ", end="")
        print(f"With a value of {self.value()}")

    def draw(self, deck: Deck):
        """
        The player draws the top card of the deck and adds it to his hand.
        """
        self._hand.append(deck.draw())
        self.show_hand()


class Dealer(Player):
    def __init__(self):
        super().__init__("DEALER")

    def draw_without_showing(self, deck: Deck):
        """
        The dealer draws the top card of the deck and adds it to his hand without showing because it's his 2nd card.
        """
        self._hand.append(deck.draw())

    def play(self, deck: Deck):
        """
        This function make a dealer play.
        """
        self.show_hand()
        while self.value() < 17:
            self.draw(deck)


class HumanPlayer(Player):
    def __init__(self, name: str):
        super().__init__(name)

    def show_possibilities(self):
        print("1st Option : Stand")
        print("2nd Option : Hit")
        if self.pair():
            print("3rd Option : Split")
        return int(input("Which option do you choose ? (Put the number)"))


class AI(Player):
    def __init__(self, nb: int):
        super().__init__('IA number' + str(nb))

    def choose_option_ai_classic(self):  # A faire
        """"
        This function will choose for the AI to stand, hit or spilt
        """
        if self.pair():
            return 3
        elif self.value() < 17:
            return 2
        else:
            return 1


class AliasPlayer(AI,HumanPlayer):
    def __init__(self, player, i: int):
        Player.__init__(self,player.name + f" hand {i}")
        self._index_hand = i
        self._owner = player

    @property
    def owner(self):
        return self._owner

    @property
    def index_hand(self):
        return self._index_hand

    @owner.setter
    def owner(self, new_owner: Player):
        self._owner = new_owner
