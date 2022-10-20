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

    """Return the value of the card, with one for an ace."""

    @property
    def value(self):
        if self._rank == Rank.ACE:
            return 1
        elif self._rank == Rank.TWO:
            return 2
        elif self._rank == Rank.THREE:
            return 3
        elif self._rank == Rank.FOUR:
            return 4
        elif self._rank == Rank.FIVE:
            return 5
        elif self._rank == Rank.SIX:
            return 6
        elif self._rank == Rank.SEVEN:
            return 7
        elif self._rank == Rank.EIGHT:
            return 8
        elif self._rank == Rank.NINE:
            return 9
        elif self._rank == Rank.TEN:
            return 10
        elif self._rank == Rank.JACK:
            return 10
        elif self._rank == Rank.QUEEN:
            return 10
        elif self._rank == Rank.KING:
            return 10


class Deck:

    def __init__(self, nb_decks):
        self._nb_decks = nb_decks
        self._cards = [Card]
        for _ in range(0, nb_decks):
            for color in Color:
                for rank in Rank:
                    self._cards.append(Card(color, rank))
        self._stop_index = random.randrange(52, 52 * (
                nb_decks - 1))  # Position of the red card in the deck : the dealer shuffles the deck when drawn

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

    """Shuffles the deck in an unpredictable way."""

    def perfect_shuffle(self):
        random.shuffle(self._cards)
        self.random_stop_index()

    def draw(self) -> Card:
        if self.stop_index > 0:  # If the dealer hasn't reached the red card yet, he draws
            self.stop_index_decrease()
            return self._cards.pop()
        else:
            self.perfect_shuffle()  # Else he shuffles the deck and then draws one
            self.draw()


class Player:

    def __init__(self):
        self._hand = [Card]

    def pair(self) -> bool:
        if len(self._hand) != 2:
            return False
        return self._hand[0] == self._hand[1]

    """Return the maximal possible value of the player's hand, below 21."""

    def value(self) -> int:
        values = [0]  # Stocks the different possible values of the player's hand
        for card in self._hand:
            if card == Rank.ACE:
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
                return -1  # The player's hand value is beyond 21
            else:
                for i in range(1, len(values)):  # We compute the maximal possible value of the player's hand below 21
                    if values[i] > 21:
                        return values[i - 1]
                return values[len(values) - 1]

    """The player draws the top card of the deck and adds it to his hand."""

    def draw(self, deck: Deck):
        self._hand.append(deck.draw())


class Dealer(Player):

    def __init__(self):
        super().__init__()


class HumanPlayer(Player):

    def __init__(self):
        super().__init__()


class AI(Player):

    def __init__(self):
        super().__init__()
