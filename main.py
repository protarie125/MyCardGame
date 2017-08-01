# -*- coding: utf-8 -*-

# Card Game 2 v0.0
# By Arie, Prot (2017)
# protarie@gmail.com
# CC BY-NC-SA 3.0

##########
# import #
##########
import os
import sys
import pygame
from pygame.locals import *
import random
from cardgame.cards import cards
from cardgame.cards import org_koc_cards
from cardgame.cards import deck_mod
from cardgame.locals import constants as cnst
from cardgame.locals import buttons as btns
from cardgame.interface import interface as itf


###########
# classes #
###########
class FieldSlot:
    def __init__(self, pos, empty_card):
        self.pos = pos  # integer 1, 2, 3, 4, or 5
        self.card = empty_card
        self.rect = cnst.card_base_rect.copy()

    def set_rect(self):
        if self.pos == 1:
            self.rect.topleft = (10, 10)
        elif self.pos == 2:
            self.rect.topleft = (10 + self.rect.width + 10, 10)
        elif self.pos == 3:
            self.rect.topleft = (50 + self.rect.width + 15, 10 + self.rect.height + 10)
        elif self.pos == 4:
            self.rect.topleft = (10 + self.rect.width + 10, 30 + 2 * self.rect.height)
        elif self.pos == 5:
            self.rect.topleft = (10, 30 + 2 * self.rect.height)
        else:
            print('ERROR: unknown slot position!')

    def draw(self, display):
        pygame.draw.rect(display, cnst.gray, self.rect, 1)


class CharSlot:
    def __init__(self, empty_card):
        self.card = empty_card
        self.rect = cnst.card_base_rect.copy()
        self.rect.topleft = (50, 10 + self.rect.height + 10)

    def draw(self, display):
        pygame.draw.rect(display, cnst.green, self.rect, 1)


class HandSlot:
    def __init__(self, pos, empty_card):
        self.pos = pos  # integer 0, 1, 2, 3, or 4
        self.card = empty_card
        self.rect = cnst.card_base_rect.copy()
        self.rect.bottomleft = (self.pos * (self.rect.width + 3), cnst.window_y)

    def draw(self, display):
        pygame.draw.rect(display, cnst.gray, self.rect, 1)


class OpFieldSlot:
    def __init__(self, pos, empty_card):
        self.pos = pos  # integer 1, 2, 3, 4, or 5
        self.card = empty_card
        self.rect = cnst.card_base_rect.copy()

    def set_rect(self):
        if self.pos == 1:
            self.rect.topright = (cnst.field_width - 10, 10)
        elif self.pos == 2:
            self.rect.topright = (cnst.field_width - (10 + self.rect.width + 10), 10)
        elif self.pos == 3:
            self.rect.topright = (cnst.field_width - (50 + self.rect.width + 15), 10 + self.rect.height + 10)
        elif self.pos == 4:
            self.rect.topright = (cnst.field_width - (10 + self.rect.width + 10), 30 + 2 * self.rect.height)
        elif self.pos == 5:
            self.rect.topright = (cnst.field_width - 10, 30 + 2 * self.rect.height)
        else:
            print('ERROR: unknown slot position!')

    def draw(self, display):
        pygame.draw.rect(display, cnst.gray, self.rect, 1)


class OpCharSlot:
    def __init__(self, empty_card):
        self.card = empty_card
        self.rect = cnst.card_base_rect.copy()
        self.rect.topright = (cnst.field_width - 50, 10 + self.rect.height + 10)

    def draw(self, display):
        pygame.draw.rect(display, cnst.red, self.rect, 1)


class Player:
    def __init__(self, deck, hand_slot, field_slot, char_slot):
        self.op = None
        self.deck = deck
        self.hand_slot = hand_slot
        self.field_slot = field_slot
        self.char_slot = char_slot
        self.grave = []

        self.fs_size = 0

        self.drew = False

    def set_op(self, op):
        self.op = op

    def set_fs_size(self, empty_card):
        ans = 0
        for f in self.field_slot:
            if not f.card == empty_card:
                ans += f.card.size
        self.fs_size = ans

    def draw_fs_size(self, display, font):
        pygame.draw.circle(display, cnst.white, cnst.fs_size_rect_g.center, int(cnst.card_s_x / 2), 1)

        size_surf = font.render('%d' % self.fs_size, True, cnst.white)
        size_rect = size_surf.get_rect()
        size_rect.center = cnst.fs_size_rect_g.center
        display.blit(size_surf, size_rect)


class CoinFlip:
    def __init__(self, time):
        self.color = cnst.coin_red
        self.time = time

    def set_color(self, c):
        self.color = c

    def set_time(self, t):
        self.time = t

    def dec_time(self):
        t = self.time - 1
        self.set_time(t)

    def draw(self, display):
        if self.time > 0:
            pygame.draw.circle(display, self.color, cnst.coin_flip_pos, cnst.coin_flip_radius)


###############
# definitions #
###############
def terminate():
    pygame.quit()
    sys.exit()


def set_up_card_img(file):
    img = pygame.image.load(os.path.join('cardgame//locals', file))
    img_surf = img.convert_alpha()
    img_s = pygame.transform.scale(img_surf, (cnst.card_base_rect.width, cnst.card_base_rect.height))
    img_l = pygame.transform.scale(img_surf, (cnst.img_l_rect.width, cnst.img_l_rect.height))

    return img_s, img_l


#################
# main function #
#################
def main():
    # set up #
    pygame.init()

    # display
    display_surf = pygame.display.set_mode((cnst.window_x, cnst.window_y))
    pygame.display.set_caption('Card Game')

    # fonts
    pygame.font.init()
    nanum_barun_gothic = os.path.join('cardgame//locals//font', 'NanumBarunGothic.ttf')
    ft_stat = pygame.font.Font(nanum_barun_gothic, 30)
    ft_fs_size = pygame.font.Font(nanum_barun_gothic, 40)
    ft_btn_l = pygame.font.Font(nanum_barun_gothic, 23)
    ft_numeric_s = pygame.font.Font(nanum_barun_gothic, 15)
    ft_numeric_l = pygame.font.Font(nanum_barun_gothic, 27)
    ft_numeric_v = pygame.font.Font(nanum_barun_gothic, 35)

    # images
    img_missing_s, img_missing_l = set_up_card_img('missing.png')
    img_card_frame_s, img_card_frame_l = set_up_card_img('card_frame.png')
    img_the_tester_s, img_the_tester_l = set_up_card_img('the_tester.png')
    img_the_vanilla_s, img_the_vanilla_l = set_up_card_img('the_vanilla.png')
    img_simple_buff_s, img_simple_buff_l = set_up_card_img('simple_buff.png')

    # locals #
    bg_color = cnst.black
    empty_card = cards.Card('DUMMY_EMPTY', '', 'DUMMY_EMPTY', '', 'dummy',
                            ft_numeric_s,
                            img_card_frame_s, img_card_frame_l,
                            None, None)

    field_slots = []
    for i in range(1, 6):
        field_slots.append(FieldSlot(i, empty_card))

    for fs in field_slots:
        fs.set_rect()

    op_field_slots = []
    for i in range(1, 6):
        op_field_slots.append(OpFieldSlot(i, empty_card))

    for opfs in op_field_slots:
        opfs.set_rect()

    char_slot = CharSlot(empty_card)
    char_slot.card = org_koc_cards.OriginalSolar(ft_numeric_s, ft_numeric_v,
                                                 img_card_frame_s, img_card_frame_l,
                                                 img_missing_s, img_missing_l)
    char_slot.card.set_rect(char_slot.rect.copy())

    op_char_slot = OpCharSlot(empty_card)
    op_char_slot.card = org_koc_cards.OriginalSolar(ft_numeric_s, ft_numeric_v,
                                                    img_card_frame_s, img_card_frame_l,
                                                    img_missing_s, img_missing_l)
    op_char_slot.card.set_rect(op_char_slot.rect.copy())

    hand_slots = []
    for i in range(5):
        hand_slots.append(HandSlot(i, empty_card))

    op_hand_slots = []
    for i in range(5):
        op_hand_slots.append(HandSlot(i, empty_card))

    # make deck1
    deck1 = deck_mod.Deck()
    for i in range(3):
        deck1.card_list.append(org_koc_cards.NewRecruits(ft_numeric_s, ft_numeric_l,
                                                         img_card_frame_s, img_card_frame_l,
                                                         img_missing_s, img_missing_l))
    for i in range(3):
        deck1.card_list.append(org_koc_cards.BraveLittleKnight(ft_numeric_s, ft_numeric_l,
                                                               img_card_frame_s, img_card_frame_l,
                                                               img_missing_s, img_missing_l))
    for n in range(24):
        if n % 3 == 1:
            deck1.card_list.append(cards.TheTester(ft_numeric_s, ft_numeric_l,
                                                   img_card_frame_s, img_card_frame_l,
                                                   img_the_tester_s, img_the_tester_l))
        elif n % 3 == 0:
            deck1.card_list.append(cards.TheVanilla(ft_numeric_s, ft_numeric_l,
                                                    img_card_frame_s, img_card_frame_l,
                                                    img_the_vanilla_s, img_the_vanilla_l))
        else:
            deck1.card_list.append(cards.SimpleBuff(ft_numeric_s, ft_numeric_l,
                                                    img_card_frame_s, img_card_frame_l,
                                                    img_simple_buff_s, img_simple_buff_l))
    random.shuffle(deck1.card_list)

    deck2 = deck_mod.Deck()
    for n in range(30):
        if n % 2 == 0:
            deck2.card_list.append(cards.TheTester(ft_numeric_s, ft_numeric_l,
                                                   img_card_frame_s, img_card_frame_l,
                                                   img_the_tester_s, img_the_tester_l))
        else:
            deck2.card_list.append(cards.TheVanilla(ft_numeric_s, ft_numeric_l,
                                                    img_card_frame_s, img_card_frame_l,
                                                    img_the_vanilla_s, img_the_vanilla_l))

    you = Player(deck1, hand_slots, field_slots, char_slot)
    opponent = Player(deck2, op_hand_slots, op_field_slots, op_char_slot)

    you.set_op(opponent)
    opponent.set_op(you)

    btn_turn_end = btns.Button(cnst.turn_end_button_rect, ft_btn_l, 'TURN END')
    btn_shuffle = btns.Button(cnst.shuffle_button_rect, ft_btn_l, 'SHUFFLE')
    btn_menu = btns.Button(cnst.menu_button_rect, ft_btn_l, 'MENU')

    btn_turn_end.available = False
    btn_shuffle.available = False
    btn_menu.available = False

    coin = CoinFlip(120)

    cnst.first_now = None

    the_game = itf.Interface(you, opponent, empty_card, coin, display_surf, bg_color,
                             ft_stat, ft_fs_size,
                             btn_turn_end, btn_shuffle, btn_menu)
    # main game loop #
    while True:
        # event handling loop #
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()

        # run game
        the_game.run()

        # update #
        pygame.display.update()
        cnst.fps_clock.tick(cnst.fps)

#######
# run #
#######
if __name__ == '__main__':
    main()
