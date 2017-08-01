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
                 display, bg_color,
                 ft_stat, ft_fs_size,
                 btn_turn_end, btn_shuffle, btn_menu):
        self.you = you
        self.opponent = opponent

        self.empty_card = empty_card
        self.selected_card = self.empty_card

        self.coin = coin

        self.display = display
        self.bg_color = bg_color

        self.ft_stat = ft_stat
        self.ft_fs_size = ft_fs_size

        self.btn_turn_end = btn_turn_end
        self.btn_shuffle = btn_shuffle
        self.btn_menu = btn_menu

        self.phase = cnst.ph_very_start

        self.cards_can_see = []

        self.use_btns = []

        self.y_order = []
        self.o_order = []

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

    def arrange_hand(self):
        for n in range(5):
            if self.you.hand_slot[n].card == self.empty_card:
                if n < 4:
                    self.you.hand_slot[n].card = self.you.hand_slot[n + 1].card
                    self.you.hand_slot[n].card.set_rect(self.you.hand_slot[n].rect.copy())
                    self.you.hand_slot[n + 1].card = self.empty_card
                else:
                    break

    def shuffle_hand(self):
        count = 0

        for h in self.you.hand_slot:
            if not h.card == self.empty_card:
                self.you.deck.card_list.append(h.card)
                h.card = self.empty_card
                count += 1
        random.shuffle(self.you.deck.card_list)

        while count > 0:
            for h in self.you.hand_slot:
                if h.card == self.empty_card:
                    h.card = self.you.deck.card_list[-1]
                    h.card.set_rect(h.rect.copy())
                    self.you.deck.card_list = self.you.deck.card_list[:-1]
                    count -= 1
                    break

    def get_random_target(self, field):
        temp = []
        for f in field:
            if not f.card == self.empty_card:
                if f.card.ctype == 'follower':
                    temp.append(f)
        random.shuffle(temp)

        if len(temp) > 0:
            return temp[0].card
        else:
            return self.empty_card

    def go_to_grave(self):
        # go to grave
        for f in self.you.field_slot:
            if not f.card == self.empty_card:
                if f.card.ctype == 'follower':
                    if f.card.hp <= 0:
                        new_life = self.you.char_slot.card.life - f.card.size
                        self.you.char_slot.card.set_life(new_life)
                        self.you.grave.append(f.card)
                        f.card = self.empty_card
        for f in self.opponent.field_slot:
            if not f.card == self.empty_card:
                if f.card.ctype == 'follower':
                    if f.card.hp <= 0:
                        new_life = self.opponent.char_slot.card.life - f.card.size
                        self.opponent.char_slot.card.set_life(new_life)
                        self.opponent.grave.append(f.card)
                        f.card = self.empty_card

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
                # turn end (only main)
                if self.btn_turn_end.available and self.phase == cnst.ph_main:
                    if self.btn_turn_end.rect.collidepoint(cnst.mouse_x, cnst.mouse_y):
                        self.phase = cnst.ph_battle
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

        # disable card use buttons
        for c in self.cards_can_see:
            c.use_button.available = False

        # clear use button list
        self.use_btns = []

        # set card rect
        for f in self.you.field_slot:
            f.card.set_rect(f.rect.copy())
        for f in self.opponent.field_slot:
            f.card.set_rect(f.rect.copy())

        # set available menu button
        self.btn_menu.available = True

        # arrange your hand
        self.arrange_hand()

        # check phase: very start -> loop[start -> main -> battle -> end]
        if self.phase == cnst.ph_very_start:
            # disable shuffle button
            self.btn_shuffle.available = False

            # disable turn end button
            self.btn_turn_end.available = False

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
            # disable shuffle button
            self.btn_shuffle.available = False

            # disable turn end button
            self.btn_turn_end.available = False

            # use character skills and start skills of followers
            if cnst.first_now == 'you':
                # 1
                self.you.char_slot.card.effect(self.you)
                self.go_to_grave()
                # 2
                f_temp = []
                for f in self.you.field_slot:
                    f_temp.append(f)
                random.shuffle(f_temp)
                for f in f_temp:
                    if f.card.ctype == 'follower':
                        for s in f.card.when_start_skills:
                            s.activate()
                            self.go_to_grave()
                # 3
                self.opponent.char_slot.card.effect(self.opponent)
                self.go_to_grave()
                # 4
                f_temp = []
                for f in self.opponent.field_slot:
                    f_temp.append(f)
                random.shuffle(f_temp)
                for f in f_temp:
                    if f.card.ctype == 'follower':
                        for s in f.card.when_start_skills:
                            s.activate()
                            self.go_to_grave()
            elif cnst.first_now == 'opponent':
                # 1
                self.opponent.char_slot.card.effect(self.opponent)
                self.go_to_grave()
                # 2
                f_temp = []
                for f in self.opponent.field_slot:
                    f_temp.append(f)
                random.shuffle(f_temp)
                for f in f_temp:
                    if f.card.ctype == 'follower':
                        for s in f.card.when_start_skills:
                            s.activate()
                            self.go_to_grave()
                # 3
                self.you.char_slot.card.effect(self.you)
                self.go_to_grave()
                # 4
                f_temp = []
                for f in self.you.field_slot:
                    f_temp.append(f)
                random.shuffle(f_temp)
                for f in f_temp:
                    if f.card.ctype == 'follower':
                        for s in f.card.when_start_skills:
                            s.activate()
                            self.go_to_grave()

            # break loop
            self.phase = cnst.ph_main
        elif self.phase == cnst.ph_main:
            # draw cards from deck
            if not self.you.drew:
                for hs in self.you.hand_slot:
                    if hs.card == self.empty_card:
                        if len(self.you.deck.card_list) > 0:
                            new_draw = self.you.deck.card_list[-1]
                            new_draw.set_rect(hs.rect.copy())
                            new_deck = self.you.deck.card_list[:-1]

                            hs.card = new_draw
                            self.you.deck.card_list = new_deck
                self.you.drew = True

            # collect use buttons
            for h in self.you.hand_slot:
                self.use_btns.append(h.card.use_button)

            # begin AI #
            # draw card and use if possible #
            # AI draw cards from deck
            if not self.opponent.drew:
                for hs in self.opponent.hand_slot:
                    if hs.card == self.empty_card:
                        if len(self.opponent.deck.card_list) > 0:
                            new_draw = self.opponent.deck.card_list[-1]
                            new_draw.set_rect(hs.rect.copy())
                            new_deck = self.opponent.deck.card_list[:-1]
                            hs.card = new_draw
                            self.opponent.deck.card_list = new_deck
                self.opponent.drew = True
            # AI play card
            self.opponent.set_fs_size(self.empty_card)
            for h in self.opponent.hand_slot:
                if self.opponent.fs_size + h.card.size <= 10:
                    for f in self.opponent.field_slot:
                        if f.card == self.empty_card:
                            f.card = h.card
                            f.card.set_rect(f.rect.copy())
                            self.opponent.set_fs_size(self.empty_card)
                            h.card = self.empty_card
            # end AI #

            # set available shuffle button
            self.btn_shuffle.available = True

            # set available turn end button
            self.btn_turn_end.available = True

            # set field size
            self.you.set_fs_size(self.empty_card)

            # set available for the selected card
            if not self.selected_card == self.empty_card:
                for h in self.you.hand_slot:
                    if self.selected_card == h.card:
                        h.card.use_button.available = True
        elif self.phase == cnst.ph_battle:
            # disable shuffle button
            self.btn_shuffle.available = False

            # disable turn end button
            self.btn_turn_end.available = False

            # 코인으로 선/후공 결정 (battle)
            if not cnst.battle_first_determined:
                who_first = random.randint(0, 2)
                if who_first == 0:
                    cnst.battle_first = 'you'
                else:
                    cnst.battle_first = 'opponent'
                cnst.battle_first_determined = True

            # begin 카드 발동 순서 결정 #
            if not cnst.order_determined:
                # collect your spell cards
                y_spell = []
                for n in range(5):
                    if not self.you.field_slot[n].card == self.empty_card:
                        if self.you.field_slot[n].card.ctype == 'spell':
                            y_spell.append(n)
                random.shuffle(y_spell)
                # collect opponent's spell cards
                o_spell = []
                for n in range(5):
                    if not self.you.field_slot[n].card == self.empty_card:
                        if self.opponent.field_slot[n].card.ctype == 'spell':
                            o_spell.append(n)
                random.shuffle(o_spell)
                # collect your follower cards
                y_follower = []
                for n in range(5):
                    if not self.you.field_slot[n].card == self.empty_card:
                        if self.you.field_slot[n].card.ctype == 'follower':
                            y_follower.append(n)
                random.shuffle(y_follower)
                # collect opponent's follower cards
                o_follower = []
                for n in range(5):
                    if not self.you.field_slot[n].card == self.empty_card:
                        if self.opponent.field_slot[n].card.ctype == 'follower':
                            o_follower.append(n)
                random.shuffle(o_follower)
                # your card order
                self.y_order = y_spell + y_follower
                # opponent's card order
                self.o_order = o_spell + o_follower
                # done
                cnst.order_determined = True
            # end 카드 발동 순서 결정 #

            # begin 순서대로 발동 #
            while len(self.y_order) > 0 or len(self.o_order) > 0:
                # you first
                if cnst.battle_first == 'you':
                    # you
                    if len(self.y_order) > 0:
                        na = self.you.field_slot[self.y_order[0]].card
                        if na.ctype == 'follower':
                            target = self.get_random_target(self.opponent.field_slot)
                            if not target == self.empty_card:
                                na.attack(target)
                                self.go_to_grave()
                            else:
                                new_life = self.opponent.char_slot.card.life - na.size
                                self.opponent.char_slot.card.set_life(new_life)
                        elif na.ctype == 'spell':
                            na.effect(self.you)
                            self.you.grave.append(na)
                            self.you.field_slot[self.y_order[0]].card = self.empty_card
                            self.go_to_grave()
                        self.y_order = self.y_order[1:]
                    # then opponent
                    if len(self.o_order) > 0:
                        na = self.opponent.field_slot[self.o_order[0]].card
                        if na.ctype == 'follower':
                            target = self.get_random_target(self.you.field_slot)
                            if not target == self.empty_card:
                                na.attack(target)
                                self.go_to_grave()
                            else:
                                new_life = self.you.char_slot.card.life - na.size
                                self.you.char_slot.card.set_life(new_life)
                        elif na.ctype == 'spell':
                            na.effect(self.opponent)
                            self.opponent.grave.append(na)
                            self.opponent.field_slot[self.o_order[0]].card = self.empty_card
                            self.go_to_grave()
                        self.o_order = self.o_order[1:]
                # opponent first
                elif cnst.battle_first == 'opponent':
                    # opponent
                    if len(self.o_order) > 0:
                        na = self.opponent.field_slot[self.o_order[0]].card
                        if na.ctype == 'follower':
                            target = self.get_random_target(self.you.field_slot)
                            if not target == self.empty_card:
                                na.attack(target)
                                self.go_to_grave()
                            else:
                                new_life = self.you.char_slot.card.life - na.size
                                self.you.char_slot.card.set_life(new_life)
                        elif na.ctype == 'spell':
                            na.effect(self.opponent)
                            self.opponent.grave.append(na)
                            self.opponent.field_slot[self.o_order[0]].card = self.empty_card
                            self.go_to_grave()
                        self.o_order = self.o_order[1:]
                    # then you
                    if len(self.y_order) > 0:
                        na = self.you.field_slot[self.y_order[0]].card
                        if na.ctype == 'follower':
                            target = self.get_random_target(self.opponent.field_slot)
                            if not target == self.empty_card:
                                na.attack(target)
                                self.go_to_grave()
                            else:
                                new_life = self.opponent.char_slot.card.life - na.size
                                self.opponent.char_slot.card.set_life(new_life)
                        elif na.ctype == 'spell':
                            na.effect(self.you)
                            self.you.grave.append(na)
                            self.you.field_slot[self.y_order[0]].card = self.empty_card
                            self.go_to_grave()
                        self.y_order = self.y_order[1:]
            # end 순서대로 발동 #

            # break loop
            self.phase = cnst.ph_end
        elif self.phase == cnst.ph_end:
            # disable shuffle button
            self.btn_shuffle.available = False

            # disable turn end button
            self.btn_turn_end.available = False

            # reset constants
            cnst.battle_first_determined = False
            cnst.battle_first = None
            cnst.order_determined = False

            self.you.drew = False
            self.opponent.drew = False

            # start skill order swap
            if cnst.first_now == 'you':
                cnst.first_now = 'opponent'
            else:
                cnst.first_now = 'you'

            # loop break
            self.phase = cnst.ph_start
        else:
            pass

    def draw_game(self):
        # display initialize
        self.display.fill(self.bg_color)

        # draw the game components #
        # right field border
        pygame.draw.rect(self.display, cnst.white, cnst.right_field_border_rect)

        # player status
        pygame.draw.rect(self.display, cnst.white, cnst.rect_your_deck_left, 1)
        yd_surf = self.ft_stat.render('%d' % len(self.you.deck.card_list), True, cnst.white)
        yd_rect = yd_surf.get_rect()
        yd_rect.center = cnst.rect_your_deck_left.center
        self.display.blit(yd_surf, yd_rect)

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
