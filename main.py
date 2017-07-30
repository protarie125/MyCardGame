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

        self.fs_size = 0

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


def get_card_can_see(fs, chs, hs, opfs, opchs):
    ccs = []

    for f in fs:
        ccs.append(f.card)

    ccs.append(chs.card)

    for h in hs:
        ccs.append(h.card)

    for opf in opfs:
        ccs.append(opf.card)

    ccs.append(opchs.card)

    return ccs


def set_up_card_img(file):
    img = pygame.image.load(os.path.join('cardgame//locals', file))
    img_surf = img.convert_alpha()
    img_s = pygame.transform.scale(img_surf, (cnst.card_base_rect.width, cnst.card_base_rect.height))
    img_l = pygame.transform.scale(img_surf, (cnst.img_l_rect.width, cnst.img_l_rect.height))

    return img_s, img_l


def shuffle_hand(you, empty_card):
    for h in you.hand_slot:
        you.deck.card_list.append(h.card)
        h.card = empty_card
        random.shuffle(you.deck.card_list)


def very_start(field_slots, char_slot, hand_slots, op_field_slots, op_char_slot,
               coin, empty_card, you, display_surf, bg_color,
               ft_fs_size, btn_turn_end, btn_shuffle, btn_menu):
    # 게임이 시작되면, 캐릭터 스킬을 사용할 순서를 정한다. #
    # main loop #
    # 마우스 사용 금지
    while cnst.very_first:
        # event handling loop #
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()

        # game logic #
        cards_can_see = get_card_can_see(field_slots, char_slot, hand_slots, op_field_slots, op_char_slot)

        # 카드 사용 금지
        for c in cards_can_see:
            c.use_button.available = False

        for fs in field_slots:
            fs.card.set_rect(fs.rect.copy())

        # 코인 플립으로 선/후공 결정
        if cnst.first_now != 'you' and cnst.first_now != 'opponent':
            who_first = random.randint(0, 2)
            if who_first == 0:
                cnst.first_now = 'you'
            else:
                cnst.first_now = 'opponent'

        # coin update
        if cnst.first_now == 'you':
            coin.set_color(cnst.coin_red)
        elif cnst.first_now == 'opponent':
            coin.set_color(cnst.coin_blue)
        coin.dec_time()

        you.set_fs_size(empty_card)

        # draw game #
        display_surf.fill(bg_color)

        pygame.draw.rect(display_surf, cnst.white, cnst.right_field_border_rect)

        for fs in field_slots:
            fs.draw(display_surf)
            if not fs.card == empty_card:
                fs.card.draw(display_surf)

        for opfs in op_field_slots:
            opfs.draw(display_surf)

        char_slot.draw(display_surf)
        char_slot.card.draw(display_surf)

        op_char_slot.draw(display_surf)
        op_char_slot.card.draw(display_surf)

        for hs in hand_slots:
            hs.draw(display_surf)
            if not hs.card == empty_card:
                hs.card.draw(display_surf)

        pygame.draw.rect(display_surf, cnst.green, cnst.card_name_rect_g, 1)
        pygame.draw.rect(display_surf, cnst.green, cnst.text_box_rect_g, 1)

        pygame.draw.rect(display_surf, cnst.gray, cnst.img_l_rect)

        you.draw_fs_size(display_surf, ft_fs_size)

        btn_turn_end.draw(display_surf)
        btn_shuffle.draw(display_surf)
        btn_menu.draw(display_surf)

        if 0 < coin.time < 90:
            coin.draw(display_surf)
        elif coin.time < -30:
            cnst.very_first = False

        # update #
        pygame.display.update()
        cnst.fps_clock.tick(cnst.fps)


#################
# main function #
#################
def main():
    # set up #
    pygame.init()
    m_left = 1

    # display
    display_surf = pygame.display.set_mode((cnst.window_x, cnst.window_y))
    pygame.display.set_caption('Card Game')

    # fonts
    pygame.font.init()
    nanum_barun_gothic = os.path.join('cardgame//locals//font', 'NanumBarunGothic.ttf')
    ft_fs_size = pygame.font.Font(nanum_barun_gothic, 40)
    ft_btn_l = pygame.font.Font(nanum_barun_gothic, 23)
    ft_numeric_s = pygame.font.Font(nanum_barun_gothic, 14)
    ft_numeric_s_b = pygame.font.Font(nanum_barun_gothic, 16)
    ft_numeric_s_b.set_bold(True)
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
                            ft_numeric_s, ft_numeric_s_b,
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
        deck1.card_list.append(org_koc_cards.NewRecruits(ft_numeric_s, ft_numeric_s_b, ft_numeric_l,
                                                         img_card_frame_s, img_card_frame_l,
                                                         img_missing_s, img_missing_l))
    for i in range(3):
        deck1.card_list.append(org_koc_cards.BraveLittleKnight(ft_numeric_s, ft_numeric_s_b, ft_numeric_l,
                                                               img_card_frame_s, img_card_frame_l,
                                                               img_missing_s, img_missing_l))
    for n in range(24):
        if n % 3 == 1:
            deck1.card_list.append(cards.TheTester(ft_numeric_s, ft_numeric_s_b, ft_numeric_l,
                                                   img_card_frame_s, img_card_frame_l,
                                                   img_the_tester_s, img_the_tester_l))
        elif n % 3 == 0:
            deck1.card_list.append(cards.TheVanilla(ft_numeric_s, ft_numeric_s_b, ft_numeric_l,
                                                    img_card_frame_s, img_card_frame_l,
                                                    img_the_vanilla_s, img_the_vanilla_l))
        else:
            deck1.card_list.append(cards.SimpleBuff(ft_numeric_s, ft_numeric_s_b, ft_numeric_l,
                                                    img_card_frame_s, img_card_frame_l,
                                                    img_simple_buff_s, img_simple_buff_l))
    random.shuffle(deck1.card_list)

    deck2 = deck_mod.Deck()
    for n in range(30):
        if n % 2 == 0:
            deck2.card_list.append(cards.TheTester(ft_numeric_s, ft_numeric_s_b, ft_numeric_l,
                                                   img_card_frame_s, img_card_frame_l,
                                                   img_the_tester_s, img_the_tester_l))
        else:
            deck2.card_list.append(cards.TheVanilla(ft_numeric_s, ft_numeric_s_b, ft_numeric_l,
                                                    img_card_frame_s, img_card_frame_l,
                                                    img_the_vanilla_s, img_the_vanilla_l))

    you = Player(deck1, hand_slots, field_slots, char_slot)
    opponent = Player(deck2, op_hand_slots, op_field_slots, op_char_slot)

    you.set_op(opponent)
    opponent.set_op(you)

    selected_card = empty_card

    cards_can_see = []

    use_btns = []

    btn_turn_end = btns.Button(cnst.turn_end_button_rect, ft_btn_l, 'TURN END')
    btn_shuffle = btns.Button(cnst.shuffle_button_rect, ft_btn_l, 'SHUFFLE')
    btn_menu = btns.Button(cnst.menu_button_rect, ft_btn_l, 'MENU')

    btn_turn_end.available = False
    btn_shuffle.available = True
    btn_menu.available = True

    coin = CoinFlip(120)

    cnst.first_now = None

    # main game loop #
    while True:
        # event handling loop #
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
            elif event.type == MOUSEMOTION:
                (cnst.mouse_x, cnst.mouse_y) = pygame.mouse.get_pos()
            elif event.type == MOUSEBUTTONUP and event.button == m_left:
                (cnst.mouse_x, cnst.mouse_y) = pygame.mouse.get_pos()
                for b in use_btns:
                    b.check_mouse_over(cnst.mouse_x, cnst.mouse_y)
                    if b.available and b.mouse_over:
                        for hs in hand_slots:
                            if not hs.card == empty_card:
                                if hs.card == b.mother:
                                    for fs in field_slots:
                                        if fs.card == empty_card:
                                            if you.fs_size + hs.card.size <= 10:
                                                fs.card = b.mother
                                                hs.card = empty_card
                                                use_btns.remove(b)
                                                break
                if btn_shuffle.available:
                    if btn_shuffle.rect.collidepoint(cnst.mouse_x, cnst.mouse_y):
                        shuffle_hand(you, empty_card)

                for fs in field_slots:
                    if fs.card.rect.collidepoint(cnst.mouse_x, cnst.mouse_y):
                        if fs.card.ctype == 'spell':
                            fs.card.effect(you)
            elif event.type == MOUSEBUTTONDOWN and event.button == m_left:
                (cnst.mouse_x, cnst.mouse_y) = pygame.mouse.get_pos()
                for c in cards_can_see:
                    if not c == empty_card:
                        if c.check_clicked(cnst.mouse_x, cnst.mouse_y):
                            selected_card = c

        # game logic #
        cards_can_see = get_card_can_see(field_slots, char_slot, hand_slots, op_field_slots, op_char_slot)

        for c in cards_can_see:
            c.use_button.available = False

        for fs in field_slots:
            fs.card.set_rect(fs.rect.copy())

        # 게임 개시 루프
        if cnst.very_first:
            very_start(field_slots, char_slot, hand_slots, op_field_slots, op_char_slot,
                       coin, empty_card, you, display_surf, bg_color,
                       ft_fs_size, btn_turn_end, btn_shuffle, btn_menu)

        # 스타트 페이즈 루프
        if cnst.first_now == 'you':
            char_slot.card.effect(you)
            op_char_slot.card.effect(opponent)
        elif cnst.first_now == 'opponent':
            op_char_slot.card.effect(opponent)
            char_slot.card.effect(you)

        # 메인 페이즈 루프
        # 배틀 페이즈 루프
        # 클린업

        for hs in hand_slots:
            if hs.card == empty_card:
                new_draw = deck1.card_list[-1]
                new_draw.set_rect(hs.rect.copy())
                new_deck = deck1.card_list[:-1]

                hs.card = new_draw
                use_btns.append(new_draw.use_button)
                deck1.card_list = new_deck

        you.set_fs_size(empty_card)

        # draw game #
        display_surf.fill(bg_color)

        pygame.draw.rect(display_surf, cnst.white, cnst.right_field_border_rect)

        for fs in field_slots:
            fs.draw(display_surf)
            if not fs.card == empty_card:
                fs.card.draw(display_surf)

        for opfs in op_field_slots:
            opfs.draw(display_surf)

        char_slot.draw(display_surf)
        char_slot.card.draw(display_surf)

        op_char_slot.draw(display_surf)
        op_char_slot.card.draw(display_surf)

        for hs in hand_slots:
            hs.draw(display_surf)
            if not hs.card == empty_card:
                hs.card.draw(display_surf)

        pygame.draw.rect(display_surf, cnst.green, cnst.card_name_rect_g, 1)
        pygame.draw.rect(display_surf, cnst.green, cnst.text_box_rect_g, 1)

        pygame.draw.rect(display_surf, cnst.gray, cnst.img_l_rect)

        if not selected_card == empty_card:
            selected_card.selected_draw(display_surf)

            for h in hand_slots:
                if selected_card == h.card:
                    h.card.use_button.available = True
                    h.card.use_button.draw(display_surf)

        you.draw_fs_size(display_surf, ft_fs_size)

        btn_turn_end.draw(display_surf)
        btn_shuffle.draw(display_surf)
        btn_menu.draw(display_surf)

        coin.draw(display_surf)

        # update #
        pygame.display.update()
        cnst.fps_clock.tick(cnst.fps)

#######
# run #
#######
if __name__ == '__main__':
    main()
