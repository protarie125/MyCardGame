# -*- coding: utf-8 -*-

# Card Game 2 v0.0
# By Arie, Prot (2017)
# protarie@gmail.com
# CC BY-NC-SA 3.0

##########
# import #
##########
import pygame
from cardgame.cards import cards
from cardgame.cards import skills as skl
import random
from cardgame.locals import constants as cnst
from cardgame.locale import korea_korean as lang


###########
# classes #
###########
# character #
class OriginalSolar(cards.Character):
    def __init__(self, ft, ft2,
                 img_card_frame_s, img_card_frame_l,
                 img_card_s, img_card_l,):
        cards.Character.__init__(self, 'ORG001', 'Knights of Consecration',
                                 lang.CARD_NAME_ORIGINAL_SOLAR, lang.CARD_TEXT_ORIGINAL_SOLAR,
                                 ft, ft2,
                                 img_card_frame_s, img_card_frame_l,
                                 img_card_s, img_card_l,
                                 30)
        self.skills = []

    def effect(self, you):
        l = [0, 1, 2, 3, 4]
        random.shuffle(l)

        fds = you.field_slot
        fds_shuffle = []

        target = []

        for n in l:
            fds_shuffle.append(fds[n])

        for fs in fds_shuffle:
            c = fs.card
            if c.ctype == 'follower':
                target.append(c)
                if len(target) == 2:
                    break

        for t in target:
            new_dp = t.dp + 1
            new_hp = t.hp + 1
            t.set_dp(new_dp)
            t.set_hp(new_hp)


# follower #
class NewRecruits(cards.Follower):
    def __init__(self, ft, ft2, ft_numeric_large,
                 img_card_frame_s, img_card_frame_l,
                 img_card_s, img_card_l):
        cards.Follower.__init__(self, 'ORG002', 'Knights of Consecration',
                                lang.CARD_NAME_NEW_RECRUITS, lang.CARD_TEXT_NEW_RECRUITS,
                                ft, ft2, ft_numeric_large,
                                1, 2, 0, 10,
                                img_card_frame_s, img_card_frame_l,
                                img_card_s, img_card_l)
        self.when_attack_skills = []
        self.when_defence_skills = []


class BraveLittleKnight(cards.Follower):
    def __init__(self, ft, ft2, ft_numeric_large,
                 img_card_frame_s, img_card_frame_l,
                 img_card_s, img_card_l):
        cards.Follower.__init__(self, 'ORG003', 'Knights of Consecration',
                                lang.CARD_NAME_BRAVE_LITTLE_KNIGHT, lang.CARD_TEXT_BRAVE_LITTLE_KNIGHT,
                                ft, ft2, ft_numeric_large,
                                2, 4, 1, 6,
                                img_card_frame_s, img_card_frame_l,
                                img_card_s, img_card_l)
        self.when_attack_skills = []
        self.when_defence_skills = [skl.DefDpPlus1(self)]


########
# test #
########
if __name__ == '__main__':
    pygame.init()
