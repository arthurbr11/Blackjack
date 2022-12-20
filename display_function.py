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
FONT = pygame.font.Font(pygame.font.get_default_font(), 36)
CARD_WIDTH, CARD_HEIGHT = 50, 75


class Images:
    def __init__(self, x, y, name_file):
        self._x = x
        self._y = y
        self._image = pygame.image.load(name_file).convert_alpha()

    def reshape(self, width, height):
        self._image = pygame.transform.scale(self._image, (width, height))

    def move(self, new_x, new_y):
        self._x = new_x
        self._y = new_y

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

    def cove_red(self, event):  # true if cover 
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


def init_page_name_player(window_width, window_height):
    button_return = Button(window_width / 10, window_height / 14, window_width / 10, window_height / 14, RED, "RETURN",
                           BLACK, FONT, BLACK_RED)
    button_IA = Button(window_width * (1 / 2 - 1 / 9), window_height / 2, window_width / 8, window_height / 12, GREY,
                       "IA", BLACK, FONT, BLACK_GREY)
    button_human = Button(window_width * (1 / 2 + 1 / 9), window_height / 2, window_width / 8, window_height / 12,
                           GREY, "HUMAN", BLACK, FONT, BLACK_GREY)

    butt_page_nom_player = [button_return, button_IA, button_human]

    rect_num_player = Rectangle(window_width / 2, window_height / 4, window_width / 3, window_height / 10, WHITE,
                                "Player k", BLACK, FONT)
    rect_nom_player = Rectangle(window_width / 2, 3 * window_height / 4, window_width / 3, window_height / 10, GREY,
                                " ", BLACK, FONT)

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
                     f'Argent : {player.owner.money} euros', BLACK, FONT)


def get_bet(player,
            windows_param):  # instead of a question show token in fct of the amount of money we have and make clickable button

    [window, window_height, window_width, white_rect, white_rect_height, background] = windows_param
    # QUESTION  Make look it better

    question_font = FONT
    question = Rectangle(window_width / 2, 2 * window_height / 5, window_width / 3, window_height / 6, WHITE,
                         f'What is your bet {player.name}?', BLACK, question_font)
    rect_argent = show_money(player, windows_param)
    rect_bet = Rectangle(window_width / 2, 3 * window_height / 4, window_width / 3, window_height / 10, GREY,
                         " ", BLACK, FONT)

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


def Image_from_card(x, y, card):
    # loading card
    if card is not None:
        nom_carte = str(card.rank.value) + "_" + card.color.value
        path = "assets/cartes/" + nom_carte + ".png"
        carte_test = Images(x, y, path)
        carte_test.reshape(CARD_WIDTH, CARD_HEIGHT)
        return carte_test
    else:
        # loading card
        path = "assets/dos_carte.png"
        back_card = Images(x, y, path)
        back_card.reshape(CARD_WIDTH, CARD_HEIGHT)
        return back_card


def moveflip_card(windows_param, card, x_ini, y_ini, x_fin, y_fin, to_show):
    [window, window_height, window_width, white_rect, white_rect_height, background] = windows_param

    back_card = Image_from_card(x_ini, y_ini, None)
    time = 800
    nb_steps = 80
    card_x = x_ini
    card_y = y_ini
    dist_x = x_fin - x_ini
    speed_x = dist_x / time
    dist_y = y_fin - y_ini
    speed_y = dist_y / time
    dt = int(time / nb_steps)
    for step in range(nb_steps):
        card_x += speed_x * dt
        card_y += speed_y * dt
        back_card.move(card_x, card_y)
        window.fill(WHITE)
        background.display(window)
        show_deck(windows_param)
        for elem in to_show:
            elem.display(window)
        back_card.display(window)
        pygame.display.flip()
        pygame.time.delay(dt)
    if card is not None:
        time = 100
        nb_steps = 10
        step_width = CARD_WIDTH / nb_steps
        dt = int(time / nb_steps)
        for step in range(nb_steps):
            card_x = card_x + (step_width / 2)
            back_card.move(card_x, card_y)
            back_card.reshape(CARD_WIDTH - (step * step_width), CARD_HEIGHT)
            window.fill(WHITE)
            background.display(window)
            for elem in to_show:
                elem.display(window)
            back_card.display(window)
            pygame.display.flip()
            pygame.time.delay(dt)
        for step in range(nb_steps):
            card_x = card_x - (step_width / 2)
            new_card = Image_from_card(card_x, card_y, card)
            new_card.move(card_x, card_y)
            new_card.reshape((step + 1) * step_width, CARD_HEIGHT)
            window.fill(WHITE)
            background.display(window)
            for elem in to_show:
                elem.display(window)
            new_card.display(window)
            pygame.display.flip()
            pygame.time.delay(dt)
    pygame.time.delay(800)


def show_deck(windows_param):
    [window, window_height, window_width, white_rect, white_rect_height, background] = windows_param
    return Image_from_card(CARD_WIDTH, (window_height - CARD_HEIGHT) / 2, None)


def show_hand_dealer(game, windows_param):
    [window, window_height, window_width, white_rect, white_rect_height, background] = windows_param
    window.fill(WHITE)
    background.display(window)
    to_show=[show_deck(windows_param)]
    for i in range(len(game.dealer.hand) - 1):
        to_show+=[Image_from_card(2 * window_width / 5 + i * CARD_WIDTH, window_height / 10, game.dealer.hand[i])]
    for elem in to_show:
        elem.display(window)
    moveflip_card(windows_param, game.dealer.hand[-1], CARD_WIDTH, (window_height - CARD_HEIGHT) / 2,
                  2 * window_width / 5 + (len(game.dealer.hand) - 1) * CARD_WIDTH,
                  window_height / 10, to_show)

def show_hand_dealer_with_black_instant(game, windows_param):

    [window, window_height, window_width, white_rect, white_rect_height, background] = windows_param
    card1 = Image_from_card(2 * window_width / 5, window_height / 10, game.dealer.hand[0])
    card2 = Image_from_card(2 * window_width / 5 + (window_width * 300) / (726 * 10), window_height / 10, None)
    return [card1, card2]


def show_hand_dealer_instant(game, windows_param):
    [window, window_height, window_width, white_rect, white_rect_height, background] = windows_param

    for i in range(len(game.dealer.hand)):
        Image_from_card(2 * window_width / 5 + i * CARD_WIDTH, window_height / 10, game.dealer.hand[i]).display(window)
    pygame.display.flip()


def show_hand_player(player, game, windows_param):
    [window, window_height, window_width, white_rect, white_rect_height, background] = windows_param

    rect_name_player = Rectangle(window_width / 2, window_height / 3, window_width / 3, window_height / 10, WHITE,
                                 player.name, BLACK, FONT)

    window.fill(WHITE)
    background.display(window)
    to_show = [rect_name_player, show_deck(windows_param), show_money(player, windows_param)] + show_hand_dealer_with_black_instant(game,
                                                                                                             windows_param)

    for i in range(len(player.hand) - 1):
        to_show += [Image_from_card(2 * window_width / 5 + i * CARD_WIDTH, window_height / 2 - CARD_HEIGHT,
                                    player.hand[i])]
    for elem in to_show:
        elem.display(window)

    moveflip_card(windows_param, player.hand[-1], CARD_WIDTH, (window_height - CARD_HEIGHT) / 2,
                  2 * window_width / 5 + (len(player.hand) - 1) * CARD_WIDTH,
                  window_height / 2 - CARD_HEIGHT, to_show)


def init_rect_name(game, windows_param):
    [window, window_height, window_width, white_rect, white_rect_height, background] = windows_param
    rect_name = []
    names = []
    for i in range(len(game.players)):
        if 'hand' not in game.players[i].name:
            rect_name += [
                Rectangle(window_width / 10 + (3 * i + 1) * CARD_WIDTH, 3 * window_height / 5 + 3 * CARD_HEIGHT / 2,
                          2 * CARD_WIDTH, CARD_HEIGHT / 4, WHITE,
                          game.players[i].name, BLACK, FONT)]
            names += [game.players[i].name]
        else:
            name = game.players[i].name.split(" ")[0]
            if name not in names:
                rect_name += [
                    Rectangle(window_width / 10 + (3 * i + 1) * CARD_WIDTH, 3 * window_height / 5 + 3 * CARD_HEIGHT / 2,
                              2 * CARD_WIDTH, CARD_HEIGHT / 4, WHITE,
                              name, BLACK, FONT)]
                names += [game.players[i].name]

    return rect_name


def show_first_distribution(game, windows_param):
    [window, window_height, window_width, white_rect, white_rect_height, background] = windows_param

    rect_name = init_rect_name(game, windows_param)

    window.fill(WHITE)
    background.display(window)
    to_show = rect_name + [show_deck(windows_param)]
    for elem in to_show:
        elem.display(window)

    nb_player = len(game.players)
    for c in range(2 * nb_player + 2):
        if c == 0:
            moveflip_card(windows_param, game.dealer.hand[0], CARD_WIDTH, (window_height - CARD_HEIGHT) / 2,
                          2 * window_width / 5, window_height / 10, to_show)
            to_show += [Image_from_card(2 * window_width / 5, window_height / 10, game.dealer.hand[0])]
        elif c == 2 * nb_player + 1:
            moveflip_card(windows_param, None, CARD_WIDTH,
                          (window_height - CARD_HEIGHT) / 2, 2 * window_width / 5 + CARD_WIDTH,
                          window_height / 10, to_show)
            to_show += [Image_from_card(2 * window_width / 5 + CARD_WIDTH,
                                        window_height / 10, None)]
        elif c < 2 * nb_player + 1:
            moveflip_card(windows_param, game.players[(c - 1) % nb_player].hand[(c - 1) // nb_player], CARD_WIDTH,
                          (window_height - CARD_HEIGHT) / 2,
                          window_width / 10 + 3 * CARD_WIDTH * ((c - 1) % nb_player) + (
                                  (c - 1) // nb_player) * CARD_WIDTH, 3 * window_height / 5, to_show)
            to_show += [Image_from_card(window_width / 10 + 3 * CARD_WIDTH * ((c - 1) % nb_player) + (
                    (c - 1) // nb_player) * CARD_WIDTH, 3 * window_height / 5,
                                        game.players[(c - 1) % nb_player].hand[(c - 1) // nb_player])]
    return


def round_of(player, game, windows_param):
    [window, window_height, window_width, white_rect, white_rect_height, background] = windows_param

    rect_name_player = Rectangle(window_width / 2, window_height / 3, window_width / 3, window_height / 10, WHITE,
                                 player.name, BLACK, FONT)
    window.fill(WHITE)
    background.display(window)
    to_show = [show_deck(windows_param), rect_name_player,
               show_money(player, windows_param)] + show_hand_dealer_with_black_instant(game, windows_param)
    for i, card in enumerate(player.hand):
        to_show += [Image_from_card(2 * window_width / 5 + i * CARD_WIDTH, window_height / 2 - CARD_HEIGHT, card)]
    for elem in to_show:
        elem.display(window)
    return


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

    button_hit = Button(button_hit_x, button_y, button_width, button_height, GREY, "HIT", BLACK, FONT, BLACK_GREY)
    button_stand = Button(button_stand_x, button_y, button_width, button_height, GREY, "STAND", BLACK, FONT,
                          BLACK_GREY)
    button_double = Button(button_double_x, button_y, button_width, button_height, GREY, "DOUBLE", BLACK, FONT,
                           BLACK_GREY)
    button_split = Button(button_split_x, button_y, button_width, button_height, GREY, "SPLIT", BLACK, FONT, BLACK_GREY)

    return [button_stand, button_hit, button_double, button_split]


def show_possibilities(player, windows_param):
    [window, window_height, window_width, white_rect, white_rect_height, background] = windows_param
    buttons = button_possibilities(windows_param)
    if player.owner.money < player.bet:
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


def show_results(game, results, windows_param):
    [window, window_height, window_width, white_rect, white_rect_height, background] = windows_param
    window.fill(WHITE)
    background.display(window)
    show_hand_dealer_instant(game, windows_param)
    show_deck(windows_param).display(window)
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
                                Image_from_card(2 * window_width / 5 + i * CARD_WIDTH, window_height / 2 - CARD_HEIGHT,
                                                game.players[count].hand[i]).display(window)
                            rect_name_player = Rectangle(window_width / 2, window_height / 3, window_width / 3,
                                                         window_height / 10,
                                                         WHITE,
                                                         player_name + " " + results[player_name], BLACK, FONT)
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


def ask_want_to_continue(windows_param):
    [window, window_height, window_width, white_rect, white_rect_height, background] = windows_param
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


def init_token(windows_param):
    [window, window_height, window_width, white_rect, white_rect_height, background] = windows_param
    # dim token
    size_token = white_rect_height / 2
    tokens_y = white_rect.y + (white_rect_height / 4)
    token1_x = white_rect_height / 2
    token5_x = white_rect_height * 5 / 4
    token10_x = white_rect_height * 2
    token25_x = white_rect_height * 11 / 4
    token100_x = white_rect_height * 7 / 2

    # tokens
    # 1
    token1 = Images(token1_x, tokens_y, "assets/token.png")
    token1.reshape(size_token, size_token)
    token5 = Images(token5_x, tokens_y, "assets/token.png")
    token5.reshape(size_token, size_token)
    token10 = Images(token10_x, tokens_y, "assets/token.png")
    token10.reshape(size_token, size_token)
    token25 = Images(token25_x, tokens_y, "assets/token.png")
    token25.reshape(size_token, size_token)
    token100 = Images(token100_x, tokens_y, "assets/token.png")
    token100.reshape(size_token, size_token)

    return [token1, token5, token10, token25, token100]
