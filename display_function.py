import model
import pygame
from pygame.locals import *
from PIL import Image
import numpy as np

pygame.init()
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (200, 200, 200)
BLACK_GREY = (100, 100, 100)
RED = (255, 0, 0)
BLACK_RED = (200, 0, 0)
font = pygame.font.Font(pygame.font.get_default_font(), 36)


class Images:
    def __init__(self, x, y, name_file):
        self._x = x
        self._y = y
        self._image = pygame.image.load(name_file).convert_alpha()

    def reshape(self, width, height):
        self._image = pygame.transform.scale(self._image, (width, height))

    def display(self, window):
        window.blit(self._image, (self._x, self._y))


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

    def display(self, window):
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
    def text(self):
        return self._text

    @text.setter
    def text(self, new_text):
        self._text = new_text


class Button(Rectangle):
    def __init__(self, x, y, width, height, color, text, text_color, font, cover_color):
        super().__init__(x, y, width, height, color, text, text_color, font)
        self._cover_color = cover_color

    # def __init__(self, x, y, width, height, color, text, text_color, font):
    #     super().__init(x, y, width, height, color, text, text_color, font)
    #     self._cover_color = self._color

    def cove_red(self, event):  # true si couvert false sinon
        if event.type == MOUSEMOTION:
            if (self._x + (self._width / 2)) > event.pos[0] > self._x - (self._width / 2) and \
                    self._y - (self._height / 2) < event.pos[1] < (self._y + (self._height / 2)):
                return True
        return False

    def display(self, window, event):
        if self.cove_red(event):
            temp_color = self._color
            self._color = self._cover_color
            super().display(window)
            self._color = temp_color

        else:
            super().display(window)

    def click(self, event):  # true si click false sinon
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                if (self._x + (self._width / 2)) > event.pos[0] > self._x - (self._width / 2) and \
                        self._y - (self._height / 2) < event.pos[1] < (self._y + (self._height / 2)):
                    return True
        return False


class DisplayCards:
    def __init__(self, card, x, y, width, height):
        self._x = x
        self._y = y
        self._card = card
        col = card.color()
        r = card.rank()
        name_file = str(r) + "_" + col + ".png"
        self._im_card = pygame.transform.scale(pygame.image.load(name_file).convert_alpha(), (width, height))

    def resize(self, new_width, new_height):
        self._im_card = pygame.transform.scale(self._im_card, (new_width, new_height))

    def repos(self, new_x, new_y):
        self._x = new_x
        self._y = new_y

    def display(self, window):
        window.blit(self._im_card, (self._x, self._y))


def init_display(window_width=1000):
    # load background image to get the size

    im_background = Image.open('assets/fond_vert.jpg')
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
    background = Images(0, 0, "assets/fond_vert.jpg")
    background.reshape(background_width, background_height)

    return window, window_height, window_width, white_rect, white_rect_height, background


def init_page_nb_players(window_width, window_height):
    rect_page_nb_players = []

    # TITRE

    title_blackjack_font = pygame.font.Font(pygame.font.get_default_font(), 36)
    title_blackjack = Rectangle(window_width / 2, window_height / 5, window_width / 2, window_height / 6, BLACK,
                                "blackJack", WHITE, title_blackjack_font)
    rect_page_nb_players += [title_blackjack]

    # QUESTION

    question_font = pygame.font.Font(pygame.font.get_default_font(), 36)
    question = Rectangle(window_width / 2, 2 * window_height / 5, window_width / 3, window_height / 6, WHITE,
                         "Nombre de players :", BLACK, question_font)
    rect_page_nb_players += [question]

    # NB playerS
    buttons_nb_player_size = int(window_width // 9)
    buttons_nb_players = np.empty((6), dtype=Button)

    for k in range(3):
        x = (5 / 2) * buttons_nb_player_size + (2 * k * buttons_nb_player_size)
        y1 = int(3 * window_height / 5)
        y2 = int(4 * window_height / 5)
        buttons_nb_players[k] = Button(x, y1, buttons_nb_player_size, buttons_nb_player_size, GREY, str(k + 1), BLACK,
                                       font, BLACK_GREY)
        buttons_nb_players[k + 3] = Button(x, y2, buttons_nb_player_size, buttons_nb_player_size, GREY, str(k + 4),
                                           BLACK, font, BLACK_GREY)

    return rect_page_nb_players, buttons_nb_players


def init_page_name_player(window_width, window_height):
    button_retour = Button(window_width / 10, window_height / 14, window_width / 10, window_height / 14, RED, "RETOUR",
                           BLACK, font, BLACK_RED)
    button_IA = Button(window_width * (1 / 2 - 1 / 9), window_height / 2, window_width / 8, window_height / 12, GREY,
                       "IA", BLACK, font, BLACK_GREY)
    button_humain = Button(window_width * (1 / 2 + 1 / 9), window_height / 2, window_width / 8, window_height / 12,
                           GREY, "HUMAIN", BLACK, font, BLACK_GREY)

    butt_page_nom_player = [button_retour, button_IA, button_humain]

    rect_num_player = Rectangle(window_width / 2, window_height / 4, window_width / 3, window_height / 10, WHITE,
                                "player k", BLACK, font)
    rect_nom_player = Rectangle(window_width / 2, 3 * window_height / 4, window_width / 3, window_height / 10, GREY,
                                " ", BLACK, font)

    rect_page_nom_player = [rect_num_player, rect_nom_player]

    return butt_page_nom_player, rect_page_nom_player


def get_nb_players(window, window_width, window_height, white_rect, white_rect_height, rect_page_nb_players,
                   buttons_nb_players):
    activated = True
    while activated:
        for event in pygame.event.get():
            for elem in rect_page_nb_players:
                elem.display(window)
            for k in range(len(buttons_nb_players)):
                buttons_nb_players[k].display(window, event)
                if buttons_nb_players[k].click(event):
                    nb_players = k + 1
                    window.fill(WHITE)
                    activated = False
                    return True, nb_players

            if event.type == QUIT:
                pygame.quit()
                exit()
            pygame.display.flip()


def get_name_players(nb_players, window, window_width, window_height, white_rect, white_rect_height,
                     butt_page_nom_player, rect_page_nom_player):
    activated = True
    window.fill(WHITE)
    user_text = " "
    i = 0
    type_player = -1
    players = [[] for j in range(nb_players)]
    while activated:
        for event in pygame.event.get():
            if i == nb_players:
                return True, players
            else:
                window.fill(WHITE)
                rect_page_nom_player[0].text = "player " + str(i + 1)
                rect_page_nom_player[0].display(window, )
                for elem in butt_page_nom_player:
                    elem.display(window, event)

                if butt_page_nom_player[2].click(event):
                    type_player = 0
                elif butt_page_nom_player[1].click(event):
                    players[i] = [1]
                    i += 1
                    type_player = -1
                elif type_player == 0:
                    rect_page_nom_player[1].display(window, )
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
                        return False, 0
                    else:
                        i -= 1
                elif event.type == QUIT:
                    pygame.quit()
                    exit()

                pygame.display.flip()


def get_start(windows_param):
    [window, window_height, window_width, white_rect, white_rect_height, background] = windows_param
    rect_page_nb_players, buttons_nb_players = init_page_nb_players(window_width, window_height)
    butt_page_nom_player, rect_page_nom_player = init_page_name_player(window_width, window_height)

    window_open = True
    page_nb_players = True
    page_name_players = False
    nb_players = 0
    while window_open:
        window.fill(WHITE)
        if page_nb_players:
            test, nb_players = get_nb_players(window, window_width, window_height, white_rect, white_rect_height,
                                              rect_page_nb_players, buttons_nb_players)
            page_nb_players = False
            page_name_players = True
            window_open = test
        elif page_name_players:
            test, players = get_name_players(nb_players, window, window_width, window_height, white_rect,
                                             white_rect_height, butt_page_nom_player, rect_page_nom_player)
            if test is None:
                window_open = False
            else:
                page_name_players = False
                page_nb_players = not test
                if test:
                    return nb_players, players
        elif window_open:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()


def show_money(player, windows_param):
    [window, window_height, window_width, white_rect, white_rect_height, background] = windows_param
    rect_argent_x = 25 * white_rect_height / 2
    rect_argent_y = white_rect.y + white_rect_height / 2
    rect_argent_width = 3 * white_rect_height
    rect_argent_height = white_rect_height / 2
    return Rectangle(rect_argent_x, rect_argent_y, rect_argent_width, rect_argent_height, GREY,
                     f'Argent : {player.owner.money} euros', BLACK, font)


def get_bet(player,
            windows_param):  # au lieu d'avoir une question show les jetons en fct de ce qu'on a en money et en faire des buttons clicable

    [window, window_height, window_width, white_rect, white_rect_height, background] = windows_param
    # QUESTION  A faire de maniere plus jolie

    question_font = pygame.font.Font(pygame.font.get_default_font(), 36)
    question = Rectangle(window_width / 2, 2 * window_height / 5, window_width / 3, window_height / 6, WHITE,
                         f'Quel est ton bet {player.name}?', BLACK, question_font)
    rect_argent = show_money(player, windows_param)
    rect_bet = Rectangle(window_width / 2, 3 * window_height / 4, window_width / 3, window_height / 10, GREY,
                         " ", BLACK, font)

    window_open = True
    page_bet = True
    bet = " "
    background.display(window)
    rect_argent.display(window)
    question.display(window)
    rect_bet.display(window, )
    while window_open:
        pygame.display.flip()
        for event in pygame.event.get():
            if page_bet:
                background.display(window)
                rect_argent.display(window)
                question.display(window)
                rect_bet.display(window, )
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        if len(bet) == 1:
                            bet = " "
                        else:
                            bet = bet[:-1]
                    elif event.key == pygame.K_RETURN:
                        background.display(window)
                        return int(bet)
                    else:
                        bet += event.unicode
                    rect_bet.text = bet
            if event.type == QUIT:
                pygame.quit()
                exit()


def show_card(x, y, card, windows_param):
    [window, window_height, window_width, white_rect, white_rect_height, background] = windows_param

    # loading card
    nom_carte = str(card.rank.value) + "_" + card.color.value
    path = "assets/cartes/" + nom_carte + ".png"
    carte_test = Images(x, y, path)

    # dimension
    im_carte = Image.open(path)
    carte_ini_width, carte_ini_height = im_carte.size
    carte_height = int(window_height / 10)
    prop_carte = carte_height / carte_ini_height
    carte_width = int(prop_carte * carte_ini_width)  #

    carte_test.reshape(carte_width, carte_height)
    return carte_test


def show_hand_dealer(dealer, windows_param):  # affiche au clique car normalement animation

    [window, window_height, window_width, white_rect, white_rect_height, background] = windows_param

    c = 0

    while True:
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                c += 1
                for i, card in enumerate(dealer.hand):
                    show_card(2 * window_width / 5 + (i * window_width * 300) / (726 * 10), window_height / 10, card,
                              windows_param).display(window)
                    pygame.display.flip()
                if c == 2:
                    return
            if event.type == QUIT:
                pygame.quit()
                exit()


def show_hand_dealer_back(dealer, windows_param):  # affiche au clique car normalement animation

    [window, window_height, window_width, white_rect, white_rect_height, background] = windows_param

    # loading card
    path = "assets/dos_carte.png"
    back_card = Images(2 * window_width / 5 + (window_width * 300) / (726 * 10), window_height / 10, path)

    # dimension
    im_carte = Image.open(path)
    carte_ini_width, carte_ini_height = im_carte.size
    carte_height = int(window_height / 10)
    prop_carte = carte_height / carte_ini_height
    carte_width = int(prop_carte * carte_ini_width)  #

    back_card.reshape(carte_width, carte_height)
    c = 0

    while True:
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                c += 1
                show_card(2 * window_width / 5, window_height / 10, dealer.hand[0], windows_param).display(window)
                pygame.display.flip()
                back_card.display(window)
                pygame.display.flip()
                if c == 2:
                    return
            if event.type == QUIT:
                pygame.quit()
                exit()


def show_hand_player(player, windows_param):  # affiche au clique car normalement animation

    [window, window_height, window_width, white_rect, white_rect_height, background] = windows_param
    rect_name_player = Rectangle(window_width / 2, window_height / 3, window_width / 3, window_height / 10, WHITE,
                                 player.name, BLACK, font)
    rect_name_player.display(window)
    show_money(player, windows_param).display(window)
    c = 0
    while True:
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                c += 1
                for i, card in enumerate(player.hand):
                    show_card(2 * window_width / 5 + (i * window_width * 300) / (726 * 10), window_height / 2, card,
                              windows_param).display(window)
                if c == 2:
                    return
            if event.type == QUIT:
                pygame.quit()
                exit()


def round_of(dealer, player, windows_param):
    [window, window_height, window_width, white_rect, white_rect_height, background] = windows_param

    rect_name_player = Rectangle(window_width / 2, window_height / 3, window_width / 3, window_height / 10, WHITE,
                                 player.name + " It's  your turn", BLACK, font)
    window.fill(WHITE)
    background.display(window)
    show_hand_dealer(dealer, windows_param)
    rect_name_player.display(window)
    show_money(player, windows_param).display(window)
    for i, card in enumerate(player.hand):
        pygame.display.flip()
        show_card(2 * window_width / 5 + (i * window_width * 300) / (726 * 10), window_height / 2, card,
                  windows_param).display(window)


def button_possibilities(windows_param):
    [window, window_height, window_width, white_rect, white_rect_height, background] = windows_param

    # dim buttons

    button_width = white_rect_height * (3 / 2)
    button_height = white_rect_height / 2
    button_y = white_rect.y + white_rect_height / 2
    button_stand_x = 14 * white_rect_height / 4
    button_hit_x = white_rect_height * 21 / 4
    button_double_x = white_rect_height * 28 / 4
    button_split_x = white_rect_height * 35 / 4

    # buttons

    button_hit = Button(button_hit_x, button_y, button_width, button_height, GREY, "HIT", BLACK, font, BLACK_GREY)
    button_stand = Button(button_stand_x, button_y, button_width, button_height, GREY, "STAND", BLACK, font,
                          BLACK_GREY)
    button_double = Button(button_double_x, button_y, button_width, button_height, GREY, "DOUBLE", BLACK, font,
                           BLACK_GREY)
    button_split = Button(button_split_x, button_y, button_width, button_height, GREY, "SPLIT", BLACK, font, BLACK_GREY)

    return [button_stand, button_hit, button_double, button_split]


def show_possibilities(player, windows_param):
    [window, window_height, window_width, white_rect, white_rect_height, background] = windows_param
    buttons = button_possibilities(windows_param)
    if player.money < player.bet:
        buttons.pop(2)
    if not player.pair() or player.owner.money < player.bet:
        buttons.pop(len(buttons) - 1)
    show_money(player, windows_param)
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


def show_results(dealer, results, windows_param):
    [window, window_height, window_width, white_rect, white_rect_height, background] = windows_param
    window.fill(WHITE)
    background.display(window)
    show_hand_dealer(dealer, windows_param)
    c = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if c < len(results):
                    count = 0
                    for player_name in results.keys():
                        if count == c:
                            rect_name_player = Rectangle(window_width / 2, window_height / 3, window_width / 3,
                                                         window_height / 10,
                                                         WHITE,
                                                         player_name + " " + results[player_name], BLACK, font)
                            rect_name_player.display(window)
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


def show_looser(player, windows_param):
    [window, window_height, window_width, white_rect, white_rect_height, background] = windows_param
    window.fill(WHITE)
    background.display(window)
    rect_name_player = Rectangle(window_width / 2, window_height / 3, window_width / 3,
                                 window_height / 10,
                                 WHITE,
                                 player.name + " you are out of the game", BLACK, font)
    rect_name_player.display(window)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                return
            if event.type == QUIT:
                pygame.quit()
                exit()
            pygame.display.flip()
def ask_want_to_continue(windows_param):
    [window, window_height, window_width, white_rect, white_rect_height, background] = windows_param
    window.fill(WHITE)
    background.display(window)
    rect_name_player = Rectangle(window_width / 2, window_height / 3, window_width / 3,
                                 window_height / 10,
                                 WHITE,
                                 "CONTINUE ?", BLACK, font)
    rect_name_player.display(window)
    button_yes = Button(window_width * (1 / 2 - 1 / 9), window_height / 2, window_width / 8, window_height / 12, GREY,
                       "YES", BLACK, font, BLACK_GREY)
    button_no = Button(window_width * (1 / 2 + 1 / 9), window_height / 2, window_width / 8, window_height / 12,
                           GREY, "NO", BLACK, font, BLACK_GREY)
    while True:
        for event in pygame.event.get():
            button_yes.display(window, event)
            if button_yes.click(event):
                return False
            button_no.display(window, event)
            if button_no.click(event):
                return True
            if event.type == QUIT:
                pygame.quit()
                exit()
            pygame.display.flip()


def close_the_game(windows_param):
    [window, window_height, window_width, white_rect, white_rect_height, background] = windows_param
    window.fill(WHITE)
    background.display(window)
    rect_end = Rectangle(window_width / 2, window_height / 3, window_width / 3,
                                 window_height / 10,
                                 WHITE,
                                 "END click to close", BLACK, font)
    rect_end.display(window)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                return
            if event.type == QUIT:
                pygame.quit()
                exit()
            pygame.display.flip()

def init_jeton(windows_param):
    [window, window_height, window_width, white_rect, white_rect_height, background] = windows_param
    # dim jeton
    taille_jeton = white_rect_height / 2
    jetons_y = white_rect.y + (white_rect_height / 4)
    jeton1_x = white_rect_height / 2
    jeton5_x = white_rect_height * 5 / 4
    jeton10_x = white_rect_height * 2
    jeton25_x = white_rect_height * 11 / 4
    jeton100_x = white_rect_height * 7 / 2

    # jetons
    # 1
    jeton1 = Images(jeton1_x, jetons_y, "assets/jeton.png")
    jeton1.reshape(taille_jeton, taille_jeton)
    jeton5 = Images(jeton5_x, jetons_y, "assets/jeton.png")
    jeton5.reshape(taille_jeton, taille_jeton)
    jeton10 = Images(jeton10_x, jetons_y, "assets/jeton.png")
    jeton10.reshape(taille_jeton, taille_jeton)
    jeton25 = Images(jeton25_x, jetons_y, "assets/jeton.png")
    jeton25.reshape(taille_jeton, taille_jeton)
    jeton100 = Images(jeton100_x, jetons_y, "assets/jeton.png")
    jeton100.reshape(taille_jeton, taille_jeton)

    return [jeton1, jeton5, jeton10, jeton25, jeton100]
