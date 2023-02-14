import pygame
from pygame.locals import *
from PIL import Image
import numpy as np
import math
import os

pygame.init()
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (200, 200, 200)
BLACK_GREY = (100, 100, 100)
RED = (255, 0, 0)
BLACK_RED = (200, 0, 0)
FONT = pygame.font.Font(pygame.font.get_default_font(), 36)
SPEED = 5
PATH = os.getcwd().rstrip('src')
SOUND_INTRO = pygame.mixer.Sound(PATH + 'assets/son/INTRO.mp3')
SOUND_CARD = pygame.mixer.Sound(PATH + 'assets/son/CARD.mp3')
SOUND_TOKEN = pygame.mixer.Sound(PATH + 'assets/son/TOKEN.mp3')
SOUND_RESULT = {'WIN !': pygame.mixer.Sound(PATH + 'assets/son/WIN.mp3'),
                'LOOSE !': pygame.mixer.Sound(PATH + 'assets/son/LOOSE.mp3'),
                'BUST !': pygame.mixer.Sound(PATH + 'assets/son/BUST.mp3'),
                'EVEN !': pygame.mixer.Sound(PATH + 'assets/son/EVEN.mp3'),
                'BLACKJACK !': pygame.mixer.Sound(PATH + 'assets/son/BLACKJACK.mp3')}
SOUND_ANOTHER = pygame.mixer.Sound(PATH + 'assets/son/ANOTHER.mp3')


class Rectangle:
    def __init__(self, x, y, width, height, color, text, text_color, font):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._color = color
        self._text = text
        self._text_color = text_color
        self._font = font

    def display(self, window) -> None:
        """
        This function display the rectangle
        :param window:
        :return:
        """
        # Object text
        object_text = pygame.font.Font.render(self._font, self._text, True, self._text_color)
        text_ini_width, text_ini_height = object_text.get_size()

        # Resize object text
        coef = min((self._width - (self._height / 2)) / text_ini_width,
                   (self._height - (self._height / 2)) / text_ini_height)
        text_width = coef * text_ini_width
        text_height = coef * text_ini_height
        object_text = pygame.transform.scale(object_text, (text_width, text_height))

        # Display
        button = pygame.Rect(self._x - (self._width / 2), self._y - (self._height / 2), self._width, self._height)
        pygame.draw.rect(window, self._color, button)
        text_rect = object_text.get_rect(center=(self._x, self._y))
        window.blit(object_text, text_rect)

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, new_text: str):
        self._text = new_text


class Button(Rectangle):
    def __init__(self, x, y, width, height, color, text, text_color, font, cover_color):
        super().__init__(x, y, width, height, color, text, text_color, font)
        self._cover_color = cover_color

    def is_in(self, event) -> bool:
        """
        This function returns True if the mouse is in the rectangle (else False)

        :param event:
        :return: a boolean
        """
        if (self._x + (self._width / 2)) > event.pos[0] > self._x - (self._width / 2) and \
                self._y - (self._height / 2) < event.pos[1] < (self._y + (self._height / 2)):
            return True
        return False

    def display(self, window, event=None) -> None:
        """
        This function displays the button with the method of the rectangle and if the mouse is on the button we change
        the color by cover color (like an hoover)

        :param window:
        :param event:
        :return:
        """
        if event is not None and event.type == MOUSEMOTION and self.is_in(event):
            temp_color = self._color
            self._color = self._cover_color
            super().display(window)
            self._color = temp_color
        else:
            super().display(window)

    def click(self, event) -> bool:
        """
        This function returns True if there is a right click in the rectangle (else False)

        :param event:
        :return: a boolean
        """
        if event.type == MOUSEBUTTONDOWN and event.button == 1 and self.is_in(event):
            return True
        return False


class Images:
    def __init__(self, x, y, name_file, is_button=False):
        self._x = x
        self._y = y
        self._image = pygame.image.load(name_file).convert_alpha()
        self._button = None
        if is_button:
            self._button = Button(x + self._image.get_width() / 2, y + self._image.get_height(),
                                  self._image.get_width(), self._image.get_height(), None, None, None, None, None)

    def reshape(self, width, height) -> None:
        """
        This function reshapes the image and the button associate if there is one

        :param width:
        :param height:
        :return:
        """
        self._image = pygame.transform.scale(self._image, (width, height))
        if self._button is not None:
            self._button = Button(self._x + self._image.get_width() / 2, self._y + self._image.get_height() / 2,
                                  self._image.get_width(), self._image.get_height(), None, None, None, None, None)

    def move(self, new_x, new_y) -> None:
        """
        This function moves the card to a new position

        :param new_x:
        :param new_y:
        :return:
        """
        self._x = new_x
        self._y = new_y

    def display(self, window) -> None:
        """
        Display the image

        :param window:
        :return:
        """
        window.blit(self._image, (self._x, self._y))

    @property
    def button(self) -> Button:
        return self._button


def init_display(window_width=1000) -> list:
    """
    This function initializes all the variables for the start of the game

    :param window_width:
    :return windows_params: a list of all parameters
    """
    # load background image to get the size

    im_background = Image.open(PATH + 'assets/fond_vert.jpg')
    background_width, background_height = im_background.size

    # Set the size of the window

    prop_background = window_width / background_width
    background_width = int(prop_background * background_width)
    background_height = int(prop_background * background_height)

    # dimension rect

    white_rect_width = background_width
    white_rect_height = white_rect_width / 15
    white_rect_x = 0
    white_rect_y = background_height
    white_rect = pygame.Rect(white_rect_x, white_rect_y, white_rect_width, white_rect_height)

    # Open the window

    window_height = background_height + white_rect_height
    window = pygame.display.set_mode((window_width, window_height))

    # background
    background = Images(0, 0, PATH + "assets/fond_vert.jpg")
    background.reshape(background_width, background_height)

    # card
    im_card = Image.open(PATH + 'assets/cartes/1_hearts.png')
    card_width_ini, card_height_ini = im_card.size

    # Set the size of the window
    card_height = int(background_height / 10)
    card_width = int(card_width_ini * card_height / card_height_ini)

    return [window, window_height, window_width, white_rect, white_rect_height, background, card_width, card_height]


def init_page_nb_players(windows_param) -> tuple[list, np.ndarray]:
    """
    One initialise all the block that will be used for the page which display the numbers of players

    :param windows_param:
    :return rect_page_nb_players: all the rectangle of the page
    :return buttons_nb_players: all the button of the page
    """
    [_, window_height, window_width, _, _, _, _, _] = windows_param

    rect_page_nb_players = []
    # TITRE

    title_blackjack_font = FONT
    title_blackjack = Rectangle(window_width / 2, window_height / 5, window_width / 2, window_height / 6, BLACK,
                                "blackJack", WHITE, title_blackjack_font)
    rect_page_nb_players += [title_blackjack]

    # QUESTION

    question_font = FONT
    question = Rectangle(window_width / 2, 2 * window_height / 5, window_width / 3, window_height / 6, WHITE,
                         "Numbers of players:", BLACK, question_font)
    rect_page_nb_players += [question]

    # NB playerS
    buttons_nb_player_size = int(window_width // 9)
    buttons_nb_players = np.empty(6, dtype=Button)

    for k in range(3):
        x = (5 / 2) * buttons_nb_player_size + (2 * k * buttons_nb_player_size)
        y1 = int(3 * window_height / 5)
        y2 = int(4 * window_height / 5)
        buttons_nb_players[k] = Button(x, y1, buttons_nb_player_size, buttons_nb_player_size, GREY, str(k + 1), BLACK,
                                       FONT, BLACK_GREY)
        buttons_nb_players[k + 3] = Button(x, y2, buttons_nb_player_size, buttons_nb_player_size, GREY, str(k + 4),
                                           BLACK, FONT, BLACK_GREY)

    return rect_page_nb_players, buttons_nb_players


def init_page_name_player(windows_param) -> tuple[list, list]:
    """
    We initialise all the block we will use for the page which display the name of players

    :param windows_param:
    :return rect_page_name_players: all the rectangle of the page
    :return buttons_name_players: all the button of the page
    """
    [_, window_height, window_width, _, _, _, _, _] = windows_param

    button_return = Button(window_width / 10, window_height / 14, window_width / 10, window_height / 14, RED, "RETURN",
                           BLACK, FONT, BLACK_RED)
    button_IA = Button(window_width * (1 / 2 - 1 / 9), window_height / 2, window_width / 8, window_height / 12, GREY,
                       "IA", BLACK, FONT, BLACK_GREY)
    button_human = Button(window_width * (1 / 2 + 1 / 9), window_height / 2, window_width / 8, window_height / 12,
                          GREY, "HUMAN", BLACK, FONT, BLACK_GREY)

    butt_page_name_player = [button_return, button_IA, button_human]

    rect_num_player = Rectangle(window_width / 2, window_height / 4, window_width / 3, window_height / 10, WHITE,
                                "Player k", BLACK, FONT)
    rect_nom_player = Rectangle(window_width / 2, 3 * window_height / 4, window_width / 3, window_height / 10, GREY,
                                " ", BLACK, FONT)

    rect_page_name_player = [rect_num_player, rect_nom_player]

    return butt_page_name_player, rect_page_name_player


def get_nb_players(window, rect_page_nb_players, buttons_nb_players) -> int:
    """
    This function gets the numbers of players who want to play
    :param window:
    :param rect_page_nb_players:
    :param buttons_nb_players:
    :return nb_players: the numbers of players who play
    """
    while True:
        for event in pygame.event.get():
            for elem in rect_page_nb_players:
                elem.display(window)
            for k in range(len(buttons_nb_players)):
                buttons_nb_players[k].display(window, event)
                if buttons_nb_players[k].click(event):
                    nb_players = k + 1
                    window.fill(WHITE)
                    return nb_players

            if event.type == QUIT:
                pygame.quit()
                exit()
            pygame.display.flip()


def get_name_players(nb_players, window, butt_page_nom_player, rect_page_nom_player) -> tuple[bool, list]:
    """
    This function gets the type and the name of each player who wants to play

    :param nb_players:
    :param window:
    :param butt_page_nom_player:
    :param rect_page_nom_player:
    :return players: it's a list of list, in which element there is the type of the player (0:human,1:ia) and if it's an
    human there is also is name (a string)
    """
    window.fill(WHITE)
    user_text = " "
    i = 0
    type_player = -1
    players = [[] for _ in range(nb_players)]
    while True:
        for event in pygame.event.get():
            if i == nb_players:
                return True, players
            else:
                window.fill(WHITE)
                rect_page_nom_player[0].text = "player " + str(i + 1)
                rect_page_nom_player[0].display(window)
                for elem in butt_page_nom_player:
                    elem.display(window, event)

                if butt_page_nom_player[2].click(event):
                    type_player = 0
                elif butt_page_nom_player[1].click(event):
                    players[i] = [1]
                    i += 1
                    type_player = -1
                elif type_player == 0:
                    rect_page_nom_player[1].display(window)
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE:
                            if len(user_text) == 1:
                                user_text = " "
                            else:
                                user_text = user_text[:-1]
                        elif event.key == pygame.K_RETURN:
                            players[i] = [0, user_text.lstrip(" ")]
                            i += 1
                            type_player = -1
                            user_text = " "
                        else:
                            user_text += event.unicode
                        rect_page_nom_player[1].text = user_text
                elif butt_page_nom_player[0].click(event):
                    if i == 0:
                        window.fill(WHITE)
                        return False, []
                    else:
                        i -= 1
                elif event.type == QUIT:
                    pygame.quit()
                    exit()

                pygame.display.flip()


def get_start(windows_param) -> tuple[int, list]:
    """
    This function displays the 2 first page of starts to get the start parameters of the game

    :param windows_param:
    :return nb_players, players:
    """
    [window, _, _, _, _, _, _, _] = windows_param

    rect_page_nb_players, buttons_nb_players = init_page_nb_players(windows_param)
    butt_page_nom_player, rect_page_nom_player = init_page_name_player(windows_param)

    page_nb_players = True
    page_name_players = False
    nb_players = 0
    SOUND_INTRO.set_volume(0.5)
    SOUND_INTRO.play(-1)
    while True:
        window.fill(WHITE)
        if page_nb_players:
            nb_players = get_nb_players(window, rect_page_nb_players, buttons_nb_players)
            page_nb_players = False
            page_name_players = True
        elif page_name_players:
            test, players = get_name_players(nb_players, window, butt_page_nom_player, rect_page_nom_player)
            page_name_players = False
            page_nb_players = not test
            if test:
                return nb_players, players
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()


def show_money(player, windows_param, money=None) -> Rectangle:
    """
    This function returns the rectangle to show the current money of the player by default it's use the player money

    :param player:
    :param windows_param:
    :param money: if we want to display an other amount of money
    :return:
    """
    [_, _, _, white_rect, white_rect_height, _, _, _] = windows_param
    rect_argent_x = 25 * white_rect_height / 2
    rect_argent_y = white_rect.y + white_rect_height / 2
    rect_argent_width = 3 * white_rect_height
    rect_argent_height = white_rect_height / 2
    if money is None:
        return Rectangle(rect_argent_x, rect_argent_y, rect_argent_width, rect_argent_height, GREY,
                         f'Argent : {player.owner.money} euros', BLACK, FONT)
    return Rectangle(rect_argent_x, rect_argent_y, rect_argent_width, rect_argent_height, GREY,
                     f'Argent : {money} euros', BLACK, FONT)


def position_token(windows_param):
    [_, _, _, _, white_rect_height, _, _, _] = windows_param

    # position token
    token1_x = white_rect_height / 2
    token5_x = white_rect_height * 5 / 4
    token10_x = white_rect_height * 2
    token25_x = white_rect_height * 11 / 4
    token100_x = white_rect_height * 7 / 2
    return [token1_x, token5_x, token10_x, token25_x, token100_x]


def init_token(windows_param, money) -> list[Images]:
    """
    This function returns all the token the player could bet with is money

    :param windows_param:
    :param money:
    :return: a list of Images(which represent token)
    """
    [_, _, _, white_rect, white_rect_height, _, _, _] = windows_param

    # dimension token
    size_token = 3 * white_rect_height / 5
    tokens_y = white_rect.y + (white_rect_height / 4)
    token1_x, token5_x, token10_x, token25_x, token100_x = position_token(windows_param)

    # tokens
    # 1
    token1 = Images(token1_x, tokens_y, PATH + "assets/token/token_1.png", True)
    token1.reshape(size_token, size_token)
    token5 = Images(token5_x, tokens_y, PATH + "assets/token/token_5.png", True)
    token5.reshape(size_token, size_token)
    token10 = Images(token10_x, tokens_y, PATH + "assets/token/token_10.png", True)
    token10.reshape(size_token, size_token)
    token25 = Images(token25_x, tokens_y, PATH + "assets/token/token_25.png", True)
    token25.reshape(size_token, size_token)
    token100 = Images(token100_x, tokens_y, PATH + "assets/token/token_100.png", True)
    token100.reshape(size_token, size_token)

    if money >= 100:
        return [token1, token5, token10, token25, token100]
    elif money >= 25:
        return [token1, token5, token10, token25]
    elif money >= 10:
        return [token1, token5, token10]
    elif money >= 5:
        return [token1, token5]
    else:
        return [token1]


def value_token(i) -> int:
    """
    Return the amount of money for the index of the token in the list of token

    :param i:
    :return:
    """
    if i == 0:
        return 1
    elif i == 1:
        return 5
    elif i == 2:
        return 10
    elif i == 3:
        return 25
    else:
        return 100


def make_current_token(index, windows_param):
    [_, window_height, window_width, _, white_rect_height, _, _, _] = windows_param
    size_token = 3 * white_rect_height / 5
    list_pos_token = position_token(windows_param)
    current_token = Images(window_width / 2 - window_width / 6 + list_pos_token[index],
                           3 * window_height / 5 + window_height / 20,
                           PATH + f'assets/token/token_{value_token(index)}.png',
                           True)
    current_token.reshape(size_token, size_token)
    return current_token


def get_bet(player, windows_param) -> int:
    """
    This function gets the bet of the player

    :param player:
    :param windows_param:
    :return bet:
    """
    [window, window_height, window_width, white_rect, white_rect_height, background, _, _] = windows_param

    # QUESTION

    question_font = FONT
    question = Rectangle(window_width / 2, 2 * window_height / 5, window_width / 3, window_height / 6, WHITE,
                         f'What is your bet {player.name}?', BLACK, question_font)
    rect_argent = show_money(player, windows_param)
    rect_bet = Rectangle(window_width / 2, 3 * window_height / 5, window_width / 3, window_height / 10, WHITE,
                         "0", BLACK, FONT)
    rect_enter = Rectangle(window_width / 2, window_height / 5, window_width / 3, window_height / 10, WHITE,
                           "enter to continue", BLACK, FONT)
    bet = 0
    current_money = player.owner.money
    to_show_elem = [background, rect_enter, question, rect_bet, rect_argent]

    list_token = init_token(windows_param, current_money)
    list_pos_token = position_token(windows_param)

    list_current_token = [0] * 5
    to_show = to_show_elem + list_token + [make_current_token(i, windows_param) for i in range(5) if
                                           list_current_token[i] != 0]
    for elem in to_show:
        elem.display(window)

    while True:
        pygame.display.flip()
        for event in pygame.event.get():
            window.fill(WHITE)

            to_show = to_show_elem + list_token + [make_current_token(j, windows_param) for j in range(5) if
                                                   list_current_token[j] != 0]
            for elem in to_show:
                elem.display(window)
            list_token_init = init_token(windows_param, current_money)
            for i, token in enumerate(list_token_init):
                if token.button.click(event):
                    bet += value_token(i)
                    current_money = player.owner.money - bet
                    to_show_elem[4] = show_money(player, windows_param, current_money)
                    to_show_elem[3] = Rectangle(window_width / 2, 3 * window_height / 5, window_width / 3,
                                                window_height / 10,
                                                WHITE,
                                                str(bet), BLACK, FONT)
                    list_token = init_token(windows_param, current_money)

                    to_show = to_show_elem + list_token + [make_current_token(j, windows_param) for j in range(5) if
                                                           list_current_token[j] != 0]
                    move_object(windows_param, 'token', token, list_pos_token[i],
                                white_rect.y + (white_rect_height / 4),
                                window_width / 2 - window_width / 6 + list_pos_token[i],
                                3 * window_height / 5 + window_height / 20, to_show)

                    list_current_token[i] += 1

                    if current_money == 0:
                        return bet

                    to_show = to_show_elem + list_token + [make_current_token(j, windows_param) for j in range(5) if
                                                           list_current_token[j] != 0]
                    pygame.display.flip()
                    window.fill(WHITE)
                    for elem in to_show:
                        elem.display(window)
            for i in range(len(list_current_token)):
                if list_current_token[i] == 0:
                    continue
                current_token = make_current_token(i, windows_param)
                if current_token.button.click(event):
                    bet -= value_token(i)
                    current_money = player.owner.money - bet
                    to_show_elem[4] = show_money(player, windows_param, current_money)
                    to_show_elem[3] = Rectangle(window_width / 2, 3 * window_height / 5, window_width / 3,
                                                window_height / 10,
                                                WHITE,
                                                str(bet), BLACK, FONT)

                    to_show = to_show_elem + list_token + [make_current_token(j, windows_param) for j in range(5) if
                                                           (list_current_token[j] != 0 and j != i) or (
                                                                   list_current_token[j] > 1 and j == i)]
                    move_object(windows_param, 'token', current_token,
                                window_width / 2 - window_width / 6 + list_pos_token[i],
                                3 * window_height / 5 + window_height / 20, list_pos_token[i],
                                white_rect.y + (white_rect_height / 4), to_show)
                    list_token = init_token(windows_param, current_money)
                    list_current_token[i] -= 1
                    to_show = to_show_elem + list_token + [make_current_token(j, windows_param) for j in range(5) if
                                                           list_current_token[j] != 0]
                    pygame.display.flip()
                    window.fill(WHITE)
                    for elem in to_show:
                        elem.display(window)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if bet != 0:
                        return bet
            if event.type == QUIT:
                pygame.quit()
                exit()


def image_from_card(windows_param, x, y, card) -> Images:
    """
    This function returns an Image of the card

    :param windows_param:
    :param x:
    :param y:
    :param card: if it's None we show the back Card
    :return:
    """
    [_, _, _, _, _, _, card_width, card_height] = windows_param

    # loading card
    if card is not None:
        nom_carte = str(card.rank.value) + "_" + card.color.value
        path = PATH + "assets/cartes/" + nom_carte + ".png"
        carte_test = Images(x, y, path)
        carte_test.reshape(card_width, card_height)
        return carte_test
    else:
        # loading card
        path = PATH + "assets/dos_carte.png"
        back_card = Images(x, y, path)
        back_card.reshape(card_width, card_height)
        return back_card


def flip_card(windows_param, card, x_ini, y_ini, to_show) -> None:
    """
    This function makes a card flip

    :param windows_param:
    :param card:
    :param x_ini:
    :param y_ini:
    :param to_show:
    :return:
    """
    [window, _, _, _, _, background, card_width, card_height] = windows_param

    back_card = image_from_card(windows_param, x_ini, y_ini, None)
    time = 100
    nb_steps = 10
    step_width = card_width / nb_steps
    dt = int(time / nb_steps)
    card_x = x_ini
    while True:
        for step in range(2 * nb_steps):
            window.fill(WHITE)
            background.display(window)
            for elem in to_show:
                elem.display(window)
            if step >= nb_steps:
                card_x = card_x - (step_width / 2)
                new_card = image_from_card(windows_param, card_x, y_ini, card)
                new_card.move(card_x, y_ini)
                new_card.reshape((step - nb_steps + 1) * step_width, card_height)
                new_card.display(window)
            else:
                card_x = card_x + (step_width / 2)
                back_card.move(card_x, y_ini)
                back_card.reshape(card_width - (step * step_width), card_height)
                back_card.display(window)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
            pygame.display.flip()
            pygame.time.delay(dt)

        pygame.time.delay(400)
        return None


def move_object(windows_param, type_object, object, x_ini, y_ini, x_fin, y_fin, to_show) -> None:
    """
    This function  moves an object (card or token) from a position to another

    :param windows_param:
    :param type_object:
    :param object:
    :param x_ini:
    :param y_ini:
    :param x_fin:
    :param y_fin:
    :param to_show:
    :return:
    """
    [window, _, _, _, _, background, _, _] = windows_param
    if type_object == 'card':
        SOUND_CARD.play()
        object_to_show = image_from_card(windows_param, x_ini, y_ini, object)
    else:
        SOUND_TOKEN.play()
        object_to_show = object
    object_x = x_ini
    object_y = y_ini
    dist_x = x_fin - x_ini
    dist_y = y_fin - y_ini
    dist = math.sqrt(dist_x ** 2 + dist_y ** 2)
    nb_steps = int(dist / SPEED) // 10
    time = nb_steps * 10
    speed_x = dist_x / time
    speed_y = dist_y / time
    dt = int(time / nb_steps)
    while True:
        for step in range(nb_steps):
            object_x += speed_x * dt
            object_y += speed_y * dt
            object_to_show.move(int(object_x), int(object_y))
            window.fill(WHITE)
            background.display(window)
            show_deck(windows_param)
            for elem in to_show:
                elem.display(window)
            object_to_show.display(window)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
            pygame.display.flip()
            pygame.time.delay(dt)
        pygame.time.delay(400)
        return None


def moveflip_card(windows_param, card, x_ini, y_ini, x_fin, y_fin, to_show) -> None:
    """
    This function moves and flip the card when it's arrived

    :param windows_param:
    :param card:
    :param x_ini:
    :param y_ini:
    :param x_fin:
    :param y_fin:
    :param to_show:
    :return:
    """
    move_object(windows_param, 'card', None, x_ini, y_ini, x_fin, y_fin, to_show)
    if card is not None:
        flip_card(windows_param, card, x_fin, y_fin, to_show)


def show_deck(windows_param) -> Images:
    """
    This function shows the deck

    :param windows_param:
    :return:
    """
    [_, window_height, _, _, _, _, card_width, card_height] = windows_param
    return image_from_card(windows_param, card_width, (window_height - card_height) / 2, None)


def show_hand_dealer(game, windows_param) -> None:
    """
    This function shows the hand of the dealer

    :param game:
    :param windows_param:
    :return:
    """
    [window, window_height, window_width, _, _, background, card_width, card_height] = windows_param
    window.fill(WHITE)
    background.display(window)
    to_show = [show_deck(windows_param)] + show_side(game, windows_param)[0]
    if len(game.dealer.hand) == 2:  # We have to flip the deck on the back
        to_show += [image_from_card(windows_param, 2 * window_width / 5, window_height / 10, game.dealer.hand[0])]
        for elem in to_show:
            elem.display(window)
        flip_card(windows_param, game.dealer.hand[1], 2 * window_width / 5 + card_width, window_height / 10, to_show)
        pygame.time.delay(800)

    else:
        for i in range(len(game.dealer.hand) - 1):
            to_show += [image_from_card(windows_param, 2 * window_width / 5 + i * card_width, window_height / 10,
                                        game.dealer.hand[i])]
        for elem in to_show:
            elem.display(window)
        moveflip_card(windows_param, game.dealer.hand[-1], card_width, (window_height - card_height) / 2,
                      2 * window_width / 5 + (len(game.dealer.hand) - 1) * card_width,
                      window_height / 10, to_show)


def show_hand_dealer_with_black_instant(game, windows_param) -> list[Images, Images]:
    """
    This function returns a list with the two card of the dealer with the second on the back

    :param game:
    :param windows_param:
    :return:
    """
    [_, window_height, window_width, _, _, _, _, _] = windows_param
    card1 = image_from_card(windows_param, 2 * window_width / 5, window_height / 10, game.dealer.hand[0])
    card2 = image_from_card(windows_param, 2 * window_width / 5 + (window_width * 300) / (726 * 10), window_height / 10,
                            None)
    return [card1, card2]


def show_hand_dealer_instant(game, windows_param):
    """
    This function displays the hand of the dealer instantly (without any animation)

    :param game:
    :param windows_param:
    :return:
    """
    [window, window_height, window_width, _, _, _, card_width, _] = windows_param

    for i in range(len(game.dealer.hand)):
        image_from_card(windows_param, 2 * window_width / 5 + i * card_width, window_height / 10,
                        game.dealer.hand[i]).display(window)
    pygame.display.flip()


def show_hand_player(player, game, windows_param) -> None:
    """
    This function shows the hand of a player with the animation of a drawing card for the last one

    :param player:
    :param game:
    :param windows_param:
    :return:
    """
    [window, window_height, window_width, _, _, background, card_width, card_height] = windows_param

    rect_name_player = Rectangle(window_width / 2, window_height / 3, window_width / 3, window_height / 10, WHITE,
                                 player.name, BLACK, FONT)

    window.fill(WHITE)
    background.display(window)
    to_show = [rect_name_player, show_deck(windows_param), show_money(player, windows_param)]
    to_show += show_hand_dealer_with_black_instant(game, windows_param) + show_side(game, windows_param, player)[0]

    for i in range(len(player.hand) - 1):
        to_show += [
            image_from_card(windows_param, 2 * window_width / 5 + i * card_width, window_height / 2 - card_height,
                            player.hand[i])]
    for elem in to_show:
        elem.display(window)

    moveflip_card(windows_param, player.hand[-1], card_width, (window_height - card_height) / 2,
                  2 * window_width / 5 + (len(player.hand) - 1) * card_width,
                  window_height / 2 - card_height, to_show)


def is_pass(player, player_ref, player_pass, alias) -> tuple[bool, int]:
    """
    This function tells if you are the player who play (with the boolean) and the int is to say: 0 you have play,
    2 you dont, 1 you are playing ,3 you have multiple hands

    :param player:
    :param player_ref:
    :param player_pass:
    :param alias:
    :return: a boolean and a int
    """
    if player is None:
        return player_pass, 2
    if alias:
        if player_ref == player:
            return True, 3
        return False, 3

    if player_ref == player:
        return True, 1
    else:
        if player_pass:
            return player_pass, 2
        else:
            return player_pass, 0


def init_rect_name(game, windows_param, player_ref=None) -> tuple[list, list]:
    """
    This function is to set rectangles of the name of  players and their positions and their statues

    :param game:
    :param windows_param:
    :param player_ref:
    :return rect_names: list of rectangle for the name
    :return statues: list of player with the statue associate
    """
    [_, window_height, window_width, _, _, _, card_width, card_height] = windows_param
    rect_names = []
    statues = []
    names = []
    player_pass = False
    for i in range(len(game.players)):
        if 'hand' not in game.players[i].name:
            player_pass, statue = is_pass(game.players[i], player_ref, player_pass, alias=False)
            statues.append([game.players[i], statue])
            names.append(game.players[i].name)
        else:
            name = game.players[i].name.split(" ")[0]
            if name not in names:
                player_pass, statue = is_pass(game.players[i], player_ref, player_pass, alias=True)
                statues.append([game.players[i].owner, statue])
                names.append(name)
    additional_space = window_width - (3 * len(statues) - 1) * card_width
    margin = additional_space // 2
    for i, name in enumerate(names):
        rect_names += [
            Rectangle(margin + (3 * i + 1) * card_width, 3 * window_height / 5 + 3 * card_height / 2, 2 * card_width,
                      card_height / 2, WHITE,
                      name, BLACK, FONT)]

    return rect_names, statues


def show_first_distribution(game, windows_param) -> None:
    """
    This function makes the animation for the first distribution of the game

    :param game:
    :param windows_param:
    :return:
    """
    [window, window_height, window_width, _, _, background, card_width,
     card_height] = windows_param

    rect_names = init_rect_name(game, windows_param)[0]

    window.fill(WHITE)
    background.display(window)
    to_show = rect_names + [show_deck(windows_param)]
    for elem in to_show:
        elem.display(window)

    nb_player = len(rect_names)
    for c in range(2 * nb_player + 2):
        if c == 0:
            moveflip_card(windows_param, game.dealer.hand[0], card_width, (window_height - card_height) / 2,
                          2 * window_width / 5, window_height / 10, to_show)
            to_show += [image_from_card(windows_param, 2 * window_width / 5, window_height / 10, game.dealer.hand[0])]
        elif c == 2 * nb_player + 1:
            moveflip_card(windows_param, None, card_width,
                          (window_height - card_height) / 2, 2 * window_width / 5 + card_width,
                          window_height / 10, to_show)
            to_show += [image_from_card(windows_param, 2 * window_width / 5 + card_width,
                                        window_height / 10, None)]
        elif c < 2 * nb_player + 1:
            index_player = (c - 1) % nb_player
            index_hand = (c - 1) // nb_player
            moveflip_card(windows_param, game.players[index_player].hand[index_hand], card_width,
                          (window_height - card_height) / 2,
                          rect_names[index_player].x + (index_hand - 1) * card_width, 3 * window_height / 5, to_show)
            to_show += [
                image_from_card(windows_param, rect_names[index_player].x + (index_hand - 1) * card_width,
                                3 * window_height / 5,
                                game.players[index_player].hand[index_hand])]
    return


def show_side(game, windows_param, player=None) -> tuple[list, list]:
    """
    This function is to know every block we have to show on the side and witch hand we have to show to the top (
    player who play)

    :param game:
    :param windows_param:
    :param player:
    :return side_element:
    :return hand_to_show:
    """
    [_, window_height, _, _, _, _, card_width,
     card_height] = windows_param
    rect_names, statues = init_rect_name(game, windows_param, player)
    side_element = rect_names
    hand_to_show = None
    for i, s in enumerate(statues):  # 0 u ve play, 2 u dont , 1 u are playing ,3 u ve multiple hands
        if s[1] == 0:
            side_element += [
                Rectangle(rect_names[i].x, 3 * window_height / 5 + card_height, 2 * card_width, card_height / 2, WHITE,
                          "val:" + str(s[0].value()), BLACK, FONT)]
        if s[1] == 1:
            hand_to_show = [[s[0].hand[0], s[0].hand[1]], [rect_names[i].x - card_width, rect_names[i].x],
                            3 * window_height / 5]
        if s[1] == 2:
            side_element += [image_from_card(windows_param, rect_names[i].x - card_width, 3 * window_height / 5,
                                             s[0].hand[0])]
            side_element += [image_from_card(windows_param, rect_names[i].x, 3 * window_height / 5,
                                             s[0].hand[1])]
        if s[1] == 3:
            side_element += [
                Rectangle(rect_names[i].x, 3 * window_height / 5 + card_height, 2 * card_width, card_height / 2, WHITE,
                          "nb_hand:" + str(s[0].nb_hand), BLACK, FONT)]

    return side_element, hand_to_show


def round_of(player, game, windows_param) -> None:
    """
    This function initializes the display for the round of the player

    :param player:
    :param game:
    :param windows_param:
    :return:
    """
    [window, window_height, window_width, _, _, background, card_width,
     card_height] = windows_param

    rect_name_player = Rectangle(window_width / 2, window_height / 3, window_width / 3, window_height / 10, WHITE,
                                 player.name, BLACK, FONT)
    window.fill(WHITE)
    background.display(window)
    to_show = [show_deck(windows_param), rect_name_player,
               show_money(player, windows_param)] + show_hand_dealer_with_black_instant(game,
                                                                                        windows_param)
    side_element, hand_to_show = show_side(game, windows_param, player)
    to_show += side_element

    if hand_to_show is not None:
        to_show += [image_from_card(windows_param, hand_to_show[1][1], hand_to_show[2], hand_to_show[0][1])]
        move_object(windows_param, 'card', hand_to_show[0][0], hand_to_show[1][0], hand_to_show[2],
                    2 * window_width / 5,
                    window_height / 2 - card_height, to_show)
        to_show.pop()
        to_show += [
            image_from_card(windows_param, 2 * window_width / 5, window_height / 2 - card_height, hand_to_show[0][0])]
        move_object(windows_param, 'card', hand_to_show[0][1], hand_to_show[1][1], hand_to_show[2],
                    2 * window_width / 5 + card_width, window_height / 2 - card_height, to_show)
    else:
        for k in range(len(player.hand)):
            to_show += [
                image_from_card(windows_param, 2 * window_width / 5 + k * card_width, window_height / 2 - card_height,
                                player.hand[k])]

    for elem in to_show:
        elem.display(window)
    return


def button_possibilities(windows_param) -> list[Button]:
    """
    This function returns the list of button to choose what we want to play
    :param windows_param:
    :return: a list of button
    """
    [_, _, _, white_rect, white_rect_height, _, _, _] = windows_param

    # dim buttons

    button_width = white_rect_height * (3 / 2)
    button_height = white_rect_height / 2
    button_y = white_rect.y + white_rect_height / 2
    button_stand_x = 14 * white_rect_height / 4
    button_hit_x = white_rect_height * 21 / 4
    button_double_x = white_rect_height * 28 / 4
    button_split_x = white_rect_height * 35 / 4

    # buttons

    button_hit = Button(button_hit_x, button_y, button_width, button_height, GREY, "HIT", BLACK, FONT, BLACK_GREY)
    button_stand = Button(button_stand_x, button_y, button_width, button_height, GREY, "STAND", BLACK, FONT,
                          BLACK_GREY)
    button_double = Button(button_double_x, button_y, button_width, button_height, GREY, "DOUBLE", BLACK, FONT,
                           BLACK_GREY)
    button_split = Button(button_split_x, button_y, button_width, button_height, GREY, "SPLIT", BLACK, FONT, BLACK_GREY)

    return [button_stand, button_hit, button_double, button_split]


def show_possibilities(player, windows_param) -> int:
    """
    This function displays just the button that we could play and if the player click on it we return the number
    associate to this choose

    :param player:
    :param windows_param:
    :return: a int
    """
    [window, _, _, _, _, _, _, _] = windows_param
    buttons = button_possibilities(windows_param)
    if player.owner.money < player.bet:
        buttons.pop(2)
    if not player.pair() or player.owner.money < player.bet:
        buttons.pop(len(buttons) - 1)
    show_money(player, windows_param)
    for button in buttons:
        button.display(window)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            for k, button in enumerate(buttons):
                button.display(window, event)
                if button.click(event):
                    return k + 1
            if event.type == QUIT:
                pygame.quit()
                exit()
            pygame.display.flip()


def show_results(game, results, windows_param) -> None:
    """
    This function displays the result for each player and we have to click to pass to an other result

    :param game:
    :param results:
    :param windows_param:
    :return:
    """
    [window, window_height, window_width, _, _, background, card_width, card_height] = windows_param
    window.fill(WHITE)
    background.display(window)
    show_hand_dealer_instant(game, windows_param)
    show_deck(windows_param).display(window)
    rect_ask_result = Rectangle(window_width / 2, window_height / 3, window_width / 3,
                                window_height / 10,
                                WHITE,
                                "CLICK TO SEE THE RESULT", BLACK, FONT)
    rect_ask_result.display(window)
    pygame.display.flip()

    c = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if c < len(results):
                    count = 0
                    for player_name in results.keys():
                        if count == c:
                            for i in range(len(game.players[count].hand)):
                                image_from_card(windows_param, 2 * window_width / 5 + i * card_width,
                                                window_height / 2 - card_height,
                                                game.players[count].hand[i]).display(window)
                            rect_name_player = Rectangle(window_width / 2, window_height / 3, window_width / 3,
                                                         window_height / 10,
                                                         WHITE,
                                                         player_name + " " + results[player_name][0], BLACK, FONT)
                            SOUND_RESULT[results[player_name][0]].play()
                            rect_name_player.display(window)
                            show_money(None, windows_param, results[player_name][1]).display(window)
                            c += 1
                            break

                        else:
                            count += 1
                else:
                    return
            if event.type == QUIT:
                pygame.quit()
                exit()
            pygame.display.flip()


def show_looser(player, windows_param) -> None:
    """
    This function shows people who can't play anymore

    :param player:
    :param windows_param:
    :return:
    """
    [window, window_height, window_width, _, _, background, _, _] = windows_param
    window.fill(WHITE)
    background.display(window)
    rect_name_player = Rectangle(window_width / 2, window_height / 3, window_width / 3,
                                 window_height / 10,
                                 WHITE,
                                 player.name + " you are out of the game", BLACK, FONT)
    rect_name_player.display(window)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                return
            if event.type == QUIT:
                pygame.quit()
                exit()
            pygame.display.flip()


def ask_want_to_continue(windows_param) -> bool:
    """
    This function asks if we want to continue and return the answer

    :param windows_param:
    :return: a boolean
    """
    [window, window_height, window_width, _, _, background, _, _] = windows_param
    window.fill(WHITE)
    background.display(window)
    rect_name_player = Rectangle(window_width / 2, window_height / 3, window_width / 3,
                                 window_height / 10,
                                 WHITE,
                                 "CONTINUE ?", BLACK, FONT)
    rect_name_player.display(window)
    button_yes = Button(window_width * (1 / 2 - 1 / 9), window_height / 2, window_width / 8, window_height / 12, GREY,
                        "YES", BLACK, FONT, BLACK_GREY)
    button_no = Button(window_width * (1 / 2 + 1 / 9), window_height / 2, window_width / 8, window_height / 12,
                       GREY, "NO", BLACK, FONT, BLACK_GREY)
    SOUND_ANOTHER.play()
    while True:
        for event in pygame.event.get():
            button_yes.display(window, event)
            if button_yes.click(event):
                SOUND_ANOTHER.stop()
                return False
            button_no.display(window, event)
            if button_no.click(event):
                SOUND_ANOTHER.stop()
                return True
            if event.type == QUIT:
                SOUND_ANOTHER.stop()
                pygame.quit()
                exit()
            pygame.display.flip()


def close_the_game(windows_param) -> None:
    """
    This function is the screen for closing

    :param windows_param:
    :return:
    """
    [window, window_height, window_width, _, _, background, _, _] = windows_param
    window.fill(WHITE)
    background.display(window)
    rect_end = Rectangle(window_width / 2, window_height / 3, window_width / 3,
                         window_height / 10,
                         WHITE,
                         "END click to close", BLACK, FONT)
    rect_end.display(window)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                return
            if event.type == QUIT:
                pygame.quit()
                exit()
            pygame.display.flip()
