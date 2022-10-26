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
    def color(self):
        return self._color

    @property
    def rank(self):
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

    def __str__(self):
        return self.color.value + " of " + str(self.rank).lstrip("Rank.")



class Deck:
    def __init__(self, nb_decks):
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
    def stop_index(self):
        return self._stop_index

    @property
    def nb_decks(self):
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
        if (
            self.stop_index > 0
        ):  # If the dealer hasn't reached the red card yet, he draws
            self.stop_index_decrease()
            return self._cards.pop()
        else:# Else he shuffles the deck and then draws one
            self.reset()
            self.perfect_shuffle()
            self.stop_index_decrease()
            return self._cards.pop()


class Player:
    def __init__(self, name):
        self._hand = []
        self._name = name

    @property
    def name(self):
        return self._name

    @property
    def hand(self):
        return self._hand

    def pair(self) -> bool:
        if len(self._hand) != 2:
            return False
        return self._hand[0] == self._hand[1]

    def reset(
        self,
    ):
        self._hand = []

    def value(self) -> int:
        """
        Return the maximal possible value of the player's hand, below 21.
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

    def draw(self, deck: Deck):
        """
        The player draws the top card of the deck and adds it to his hand.
        """
        self._hand.append(deck.draw())
        print(self._name + ": have ", end="")
        for card in self._hand:
            print(card, end="")
            print(", ", end="")
        print(f"With a value of {self.value()}")


class Dealer(Player):
    def __init__(self):
        super().__init__("DEALER")

    def draw_without_showing(self, deck: Deck):
        """
        The dealer draws the top card of the deck and adds it to his hand without showing because it's his 2nd card.
        """
        self._hand.append(deck.draw())


class HumanPlayer(Player):
    def __init__(self, name):
        super().__init__(name)


class AI(Player):
    def __init__(self, name):
        super().__init__(name)
        #test
