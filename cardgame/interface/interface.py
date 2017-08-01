# -*- coding: utf-8 -*-

# Card Game 2 v0.0
# By Arie, Prot (2017)
# protarie@gmail.com
# CC BY-NC-SA 3.0

##########
# import #
##########
import sys
import random
import pygame
from pygame.locals import *
from cardgame.locals import constants as cnst


###########
# classes #
###########
class Interface:
    def __init__(self, you, opponent, empty_card, coin,
                 display, bg_color, ft_fs_size,
                 btn_turn_end, btn_shuffle, btn_menu):
        self.you = you
        self.opponent = opponent

        self.empty_card = empty_card
        self.selected_card = self.empty_card

        self.coin = coin

        self.display = display
        self.bg_color = bg_color
        self.ft_fs_size = ft_fs_size

        self.btn_turn_end = btn_turn_end
        self.btn_shuffle = btn_shuffle
        self.btn_menu = btn_menu

        self.phase = cnst.ph_very_start

        self.cards_can_see = []

        self.use_btns = []

    def get_card_can_see(self):
        ccs = []

        for f in self.you.field_slot:
            ccs.append(f.card)

        ccs.append(self.you.char_slot.card)

        for h in self.you.hand_slot:
            ccs.append(h.card)

        for opf in self.opponent.field_slot:
            ccs.append(opf.card)

        ccs.append(self.opponent.char_slot.card)

        return ccs

    def shuffle_hand(self):
        for h in self.you.hand_slot:
            self.you.deck.card_list.append(h.card)
            h.card = self.empty_card
            random.shuffle(self.you.deck.card_list)

    def run(self):
        # main loop #
        while True:
            # event handling #
            self.event_handling()

            # game logic #
            self.game_logic()

            # draw game #
            self.draw_game()

            # update #
            pygame.display.update()
            cnst.fps_clock.tick(cnst.fps)

    def event_handling(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
            elif event.type == MOUSEMOTION:
                (cnst.mouse_x, cnst.mouse_y) = pygame.mouse.get_pos()
            elif event.type == MOUSEBUTTONUP and event.button == cnst.m_left:
                # use a card (only main)
                if self.phase == cnst.ph_main:
                    for b in self.use_btns:
                        b.check_mouse_over(cnst.mouse_x, cnst.mouse_y)
                        if b.available and b.mouse_over:
                            for hs in self.you.hand_slot:
                                if not hs.card == self.empty_card:
                                    if hs.card == b.mother:
                                        for fs in self.you.field_slot:
                                            if fs.card == self.empty_card:
                                                if self.you.fs_size + hs.card.size <= 10:
                                                    fs.card = b.mother
                                                    hs.card = self.empty_card
                                                    self.use_btns.remove(b)
                                                    break
                # shuffle hand (only main)
                if self.btn_shuffle.available and self.phase == cnst.ph_main:
                    if self.btn_shuffle.rect.collidepoint(cnst.mouse_x, cnst.mouse_y):
                        self.shuffle_hand()
                # use a spell card - debug (only main)
                if self.phase == cnst.ph_main:
                    for fs in self.you.field_slot:
                        if fs.card.rect.collidepoint(cnst.mouse_x, cnst.mouse_y):
                            if fs.card.ctype == 'spell':
                                fs.card.effect(self.you)
            elif event.type == MOUSEBUTTONDOWN and event.button == cnst.m_left:
                for c in self.cards_can_see:
                    if not c == self.empty_card:
                        if c.check_clicked(cnst.mouse_x, cnst.mouse_y):
                            self.selected_card = c

    def game_logic(self):
        # 보이는 카드 콜렉트
        self.cards_can_see = self.get_card_can_see()

        # 카드 사용 금지
        for c in self.cards_can_see:
            c.use_button.available = False

        # set card rect
        for f in self.you.field_slot:
            f.card.set_rect(f.rect.copy())
        for f in self.opponent.field_slot:
            f.card.set_rect(f.rect.copy())

        # check phase: very start -> loop[start -> main -> battle -> end]
        if self.phase == cnst.ph_very_start:
            # 코인 플립으로 선/후공 결정
            if cnst.first_now != 'you' and cnst.first_now != 'opponent':
                who_first = random.randint(0, 2)
                if who_first == 0:
                    cnst.first_now = 'you'
                else:
                    cnst.first_now = 'opponent'

            # coin update
            if cnst.first_now == 'you':
                self.coin.set_color(cnst.coin_red)
            elif cnst.first_now == 'opponent':
                self.coin.set_color(cnst.coin_blue)
            self.coin.dec_time()

            self.you.set_fs_size(self.empty_card)

            # 루프 탈출 체크
            if self.coin.time < -30:
                cnst.very_first = False
                self.phase = cnst.ph_start
        elif self.phase == cnst.ph_start:
            # use character skills and start skills of followers
            if cnst.first_now == 'you':
                # 1
                self.you.char_slot.card.effect(self.you)
                # 2
                for f in self.you.field_slot:
                    if f.card.ctype == 'follower':
                        for s in f.card.when_start_skills:
                            s.activate()
                # 3
                self.opponent.char_slot.card.effect(self.opponent)
                # 4
                for f in self.opponent.field_slot:
                    if f.card.ctype == 'follower':
                        for s in f.card.when_start_skills:
                            s.activate()
            elif cnst.first_now == 'opponent':
                # 1
                self.opponent.char_slot.card.effect(self.opponent)
                # 2
                for f in self.opponent.field_slot:
                    if f.card.ctype == 'follower':
                        for s in f.card.when_start_skills:
                            s.activate()
                # 3
                self.you.char_slot.card.effect(self.you)
                # 4
                for f in self.you.field_slot:
                    if f.card.ctype == 'follower':
                        for s in f.card.when_start_skills:
                            s.activate()

            # break loop
            self.phase = cnst.ph_main
        elif self.phase == cnst.ph_main:
            # disable card use buttons
            for c in self.cards_can_see:
                c.use_button.available = False

            # draw cards
            for hs in self.you.hand_slot:
                if hs.card == self.empty_card:
                    new_draw = self.you.deck.card_list[-1]
                    new_draw.set_rect(hs.rect.copy())
                    new_deck = self.you.deck.card_list[:-1]

                    hs.card = new_draw
                    self.use_btns.append(new_draw.use_button)
                    self.you.deck.card_list = new_deck

            # set field size
            self.you.set_fs_size(self.empty_card)

            # set available for the selected card
            for h in self.you.hand_slot:
                if self.selected_card == h.card:
                    h.card.use_button.available = True
                    h.card.use_button.draw(self.display)
        elif self.phase == cnst.ph_battle:
            pass
        elif self.phase == cnst.ph_end:
            pass
        else:
            pass

    def draw_game(self):
        # display initialize
        self.display.fill(self.bg_color)

        # draw the game components #
        # right field border
        pygame.draw.rect(self.display, cnst.white, cnst.right_field_border_rect)

        # field slots and its card
        for f in self.you.field_slot:
            f.draw(self.display)
            if not f.card == self.empty_card:
                f.card.draw(self.display)
        for f in self.opponent.field_slot:
            f.draw(self.display)
            if not f.card == self.empty_card:
                f.card.draw(self.display)

        # character slots and its card
        self.you.char_slot.draw(self.display)
        self.you.char_slot.card.draw(self.display)
        self.opponent.char_slot.draw(self.display)
        self.opponent.char_slot.card.draw(self.display)

        # your hand slot
        for hs in self.you.hand_slot:
            hs.draw(self.display)
            if not hs.card == self.empty_card:
                hs.card.draw(self.display)

        # your field slot size
        self.you.draw_fs_size(self.display, self.ft_fs_size)

        # card information component
        pygame.draw.rect(self.display, cnst.green, cnst.card_name_rect_g, 1)
        pygame.draw.rect(self.display, cnst.green, cnst.text_box_rect_g, 1)
        pygame.draw.rect(self.display, cnst.gray, cnst.img_l_rect)

        # draw the selected card
        if not self.selected_card == self.empty_card:
            self.selected_card.selected_draw(self.display)
            for h in self.you.hand_slot:
                if self.selected_card == h.card:
                    h.card.use_button.available = True
                    h.card.use_button.draw(self.display)

        # general buttons
        self.btn_turn_end.draw(self.display)
        self.btn_shuffle.draw(self.display)
        self.btn_menu.draw(self.display)

        # components for each phase
        if self.phase == cnst.ph_very_start:
            # draw the coin
            if 0 < self.coin.time < 90:
                self.coin.draw(self.display)
        elif self.phase == cnst.ph_start:
            pass
        elif self.phase == cnst.ph_main:
            pass
        elif self.phase == cnst.ph_battle:
            pass
        elif self.phase == cnst.ph_end:
            pass
        else:
            pass


###############
# definitions #
###############
def terminate():
    pygame.quit()
    sys.exit()

########
# test #
########
if __name__ == '__main__':
    pygame.init()
