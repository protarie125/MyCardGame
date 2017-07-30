# -*- coding: utf-8 -*-

# Card Game 2 v0.0
# By Arie, Prot (2017)
# protarie@gmail.com
# CC BY-NC-SA 3.0

##########
# import #
##########
import pygame
from cardgame.cards import skills as skl
import random
from cardgame.locals import constants as cnst
from cardgame.locals import buttons as btns


###########
# classes #
###########
class Card:
    def __init__(self, cid, region, name, text, ctype,
                 ft, ft2,
                 img_card_frame_s, img_card_frame_l,
                 img_card_s, img_card_l):
        self.cid = cid
        self.region = region
        self.name = name
        self.text = text
        self.ctype = ctype

        self.size = 0

        self.rect = cnst.card_base_rect.copy()
        self.card_name_rect_g = cnst.card_name_rect_g
        self.text_rect_g = cnst.text_box_rect_g

        self.img_card_frame_s = img_card_frame_s
        self.img_card_frame_l = img_card_frame_l
        self.img_card_s = img_card_s
        self.img_card_l = img_card_l

        self.ft = ft
        self.ft2 = ft2

        self.selected = False

        self.use_button = btns.CardUseButton(cnst.use_button_rect.copy(), self)

    def set_rect(self, rect):
        self.rect = rect

    def draw(self, display):
        pygame.draw.rect(display, cnst.blue, self.rect)

        if self.img_card_s:
            display.blit(self.img_card_s, self.rect)
            display.blit(self.img_card_frame_s, self.rect)

    def selected_draw(self, display):
        pygame.draw.rect(display, cnst.blue, cnst.img_l_rect)

        if self.img_card_s:
            display.blit(self.img_card_l, cnst.img_l_rect)
            display.blit(self.img_card_frame_l, cnst.img_l_rect)

        card_name_surf = self.ft.render("%s" % self.name, True, cnst.white)
        card_name_rect = card_name_surf.get_rect()
        card_name_rect.center = self.card_name_rect_g.center
        display.blit(card_name_surf, card_name_rect)

        text_surf = self.ft.render("%s" % self.text, True, cnst.white)
        text_rect = text_surf.get_rect()
        text_rect.left = self.text_rect_g.left + 5
        text_rect.top = self.text_rect_g.top
        display.blit(text_surf, text_rect)

    def check_clicked(self, mx, my):
        return self.rect.collidepoint(mx, my)

    def effect(self, you):
        pass


class Follower(Card):
    def __init__(self, cid, region, name, text,
                 ft, ft2, ft_numeric_large,
                 size, ap, dp, hp,
                 img_card_frame_s, img_card_frame_l,
                 img_card_s, img_card_l):
        Card.__init__(self, cid, region, name, text, 'follower',
                      ft, ft2,
                      img_card_frame_s, img_card_frame_l,
                      img_card_s, img_card_l)
        self.ft_numeric_large = ft_numeric_large

        self.size = size
        self.ap = ap
        self.dp = dp
        self.hp = hp

        self.size_radius = int(self.rect.width / 8)
        self.size_rect_g = pygame.Rect(0, 0, 2 * self.size_radius, 2 * self.size_radius)
        self.size_rect_g.topright = self.rect.topright

        self.size_surf = self.ft_numeric_large.render("%d" % self.size, True, cnst.white)
        self.size_rect = self.size_surf.get_rect()
        self.size_rect.center = self.size_rect_g.center

        self.ap_rect_g = pygame.Rect(0, 0, int(self.rect.width / 3), 30)
        self.ap_rect_g.bottomleft = self.rect.bottomleft
        self.dp_rect_g = pygame.Rect(0, 0, int(self.rect.width / 3), 30)
        self.dp_rect_g.midbottom = self.rect.midbottom
        self.hp_rect_g = pygame.Rect(0, 0, int(self.rect.width / 3), 30)
        self.hp_rect_g.bottomright = self.rect.bottomright

        self.ap_surf = self.ft.render("%d" % self.ap, True, cnst.white)
        self.ap_surf_b = self.ft2.render("%d" % self.ap, True, cnst.black)
        self.ap_rect = self.ap_surf.get_rect()
        self.ap_rect.center = self.ap_rect_g.center
        self.ap_rect_b = self.ap_surf_b.get_rect()
        self.ap_rect_b.center = self.ap_rect_g.center

        self.dp_surf = self.ft.render("%d" % self.dp, True, cnst.white)
        self.dp_surf_b = self.ft2.render("%d" % self.dp, True, cnst.black)
        self.dp_rect = self.dp_surf.get_rect()
        self.dp_rect.center = self.dp_rect_g.center
        self.dp_rect_b = self.dp_surf_b.get_rect()
        self.dp_rect_b.center = self.dp_rect_g.center

        self.hp_surf = self.ft.render("%d" % self.hp, True, cnst.white)
        self.hp_surf_b = self.ft2.render("%d" % self.hp, True, cnst.black)
        self.hp_rect = self.hp_surf.get_rect()
        self.hp_rect.center = self.hp_rect_g.center
        self.hp_rect_b = self.hp_surf_b.get_rect()
        self.hp_rect_b.center = self.hp_rect_g.center

        self.when_attack_skills = []
        self.when_defence_skills = []

    def set_rect(self, rect):
        Card.set_rect(self, rect)

        self.size_rect_g.topright = self.rect.topright

        self.size_rect.center = self.size_rect_g.center

        self.ap_rect_g.bottomleft = self.rect.bottomleft
        self.dp_rect_g.midbottom = self.rect.midbottom
        self.hp_rect_g.bottomright = self.rect.bottomright

        self.ap_rect.center = self.ap_rect_g.center
        self.ap_rect_b.center = self.ap_rect_g.center
        self.dp_rect.center = self.dp_rect_g.center
        self.dp_rect_b.center = self.dp_rect_g.center
        self.hp_rect.center = self.hp_rect_g.center
        self.hp_rect_b.center = self.hp_rect_g.center

    def set_size(self, size):
        self.size = size
        self.size_surf = self.ft_numeric_large.render("%d" % self.size, True, cnst.white)
        self.size_rect = self.size_surf.get_rect()
        self.size_rect.center = self.size_rect_g.center

    def set_ap(self, ap):
        self.ap = ap
        self.ap_surf = self.ft.render("%d" % self.ap, True, cnst.white)
        self.ap_surf_b = self.ft2.render("%d" % self.ap, True, cnst.black)
        self.ap_rect = self.ap_surf.get_rect()
        self.ap_rect.center = self.ap_rect_g.center
        self.ap_rect_b = self.ap_surf_b.get_rect()
        self.ap_rect_b.center = self.ap_rect_g.center

    def set_dp(self, dp):
        self.dp = dp
        self.dp_surf = self.ft.render("%d" % self.dp, True, cnst.white)
        self.dp_surf_b = self.ft2.render("%d" % self.dp, True, cnst.black)
        self.dp_rect = self.dp_surf.get_rect()
        self.dp_rect.center = self.dp_rect_g.center
        self.dp_rect_b = self.dp_surf_b.get_rect()
        self.dp_rect_b.center = self.dp_rect_g.center

    def set_hp(self, hp):
        self.hp = hp
        self.hp_surf = self.ft.render("%d" % self.hp, True, cnst.white)
        self.hp_surf_b = self.ft2.render("%d" % self.hp, True, cnst.black)
        self.hp_rect = self.hp_surf.get_rect()
        self.hp_rect.center = self.hp_rect_g.center
        self.hp_rect_b = self.hp_surf_b.get_rect()
        self.hp_rect_b.center = self.hp_rect_g.center

    def draw(self, display):
        Card.draw(self, display)

        pygame.draw.circle(display, cnst.blue, self.size_rect_g.center, self.size_radius)
        display.blit(self.size_surf, self.size_rect)

        display.blit(self.ap_surf_b, self.ap_rect)
        display.blit(self.dp_surf_b, self.dp_rect)
        display.blit(self.hp_surf_b, self.hp_rect)
        display.blit(self.ap_surf, self.ap_rect)
        display.blit(self.dp_surf, self.dp_rect)
        display.blit(self.hp_surf, self.hp_rect)

    def attack(self, target):
        for skill in self.when_attack_skills:
            skill.activate(target)

        for skill in target.when_defence_skills:
            skill.activate()

        new_hp = target.hp - (self.ap - target.dp)
        target.set_hp(new_hp)
        print("%s attacked %s." % (self.name, target.name))


class Spell(Card):
    def __init__(self, cid, region, name, text,
                 ft, ft2, ft_numeric_large,
                 size,
                 img_card_frame_s, img_card_frame_l,
                 img_card_s, img_card_l):
        Card.__init__(self, cid, region, name, text, 'spell',
                      ft, ft2,
                      img_card_frame_s, img_card_frame_l,
                      img_card_s, img_card_l)
        self.ft_numeric_large = ft_numeric_large

        self.size = size

        self.size_radius = int(self.rect.width / 8)
        self.size_rect_g = pygame.Rect(0, 0, 2 * self.size_radius, 2 * self.size_radius)
        self.size_rect_g.topright = self.rect.topright

        self.size_surf = self.ft_numeric_large.render("%d" % self.size, True, cnst.white)
        self.size_rect = self.size_surf.get_rect()
        self.size_rect.center = self.size_rect_g.center

    def set_rect(self, rect):
        Card.set_rect(self, rect)

        self.size_rect_g.topright = self.rect.topright

        self.size_rect.center = self.size_rect_g.center

    def set_size(self, size):
        self.size = size
        self.size_surf = self.ft_numeric_large.render("%d" % self.size, True, cnst.white)
        self.size_rect = self.size_surf.get_rect()
        self.size_rect.center = self.size_rect_g.center

    def draw(self, display):
        Card.draw(self, display)

        pygame.draw.circle(display, cnst.blue, self.size_rect_g.center, self.size_radius)
        display.blit(self.size_surf, self.size_rect)

    def effect(self, you):
        pass


class Character(Card):
    def __init__(self, cid, region, name, text,
                 ft, ft2,
                 img_card_frame_s, img_card_frame_l,
                 img_card_s, img_card_l,
                 life):
        Card.__init__(self, cid, region, name, text, 'character',
                      ft, ft2,
                      img_card_frame_s, img_card_frame_l,
                      img_card_s, img_card_l)

        self.life = life
        self.life_rect_g = pygame.Rect(0, 0, 40, 30)
        self.life_surf = self.ft2.render('%d' % self.life, True, cnst.violet)
        self.life_rect = self.life_surf.get_rect()
        self.life_rect.center = self.life_rect_g.center

        self.skills = []

    def set_rect(self, rect):
        Card.set_rect(self, rect)

        self.life_rect_g.bottomright = self.rect.bottomright

        self.life_rect.center = self.life_rect_g.center

    def set_life(self, life):
        self.life = life
        self.life_surf = self.ft2.render('%d' % self.life, True, cnst.violet)
        self.life_rect = self.life_surf.get_rect()
        self.life_rect.center = self.life_rect_g.center

    def draw(self, display):
        Card.draw(self, display)

        display.blit(self.life_surf, self.life_rect)

    def effect(self, you):
        pass


class TheTester(Follower):
    def __init__(self, ft, ft2, ft_numeric_large,
                 img_card_frame_s, img_card_frame_l,
                 img_card_s, img_card_l):
        Follower.__init__(self, 'TST001', 'test',
                          'CARD_NAME_THE_TESTER', 'CARD_TEXT_THE_TESTER',
                          ft, ft2, ft_numeric_large,
                          4, 5, 1, 7,
                          img_card_frame_s, img_card_frame_l,
                          img_card_s, img_card_l)

        self.when_attack_skills = [skl.AtkHpMinus2(self)]
        self.when_defence_skills = [skl.DefHpPlus1(self)]


class TheVanilla(Follower):
    def __init__(self, ft, ft2, ft_numeric_large,
                 img_card_frame_s, img_card_frame_l,
                 img_card_s, img_card_l):
        Follower.__init__(self, 'TST002', 'test',
                          'CARD_NAME_THE_VANILLA', 'CARD_TEXT_THE_VANILLA',
                          ft, ft2, ft_numeric_large,
                          3, 4, 0, 12,
                          img_card_frame_s, img_card_frame_l,
                          img_card_s, img_card_l)

        self.when_attack_skills = []
        self.when_defence_skills = []


class SimpleBuff(Spell):
    def __init__(self, ft, ft2, ft_numeric_large,
                 img_card_frame_s, img_card_frame_l,
                 img_card_s, img_card_l):
        Spell.__init__(self, 'TEST003', 'test',
                       'CARD_NAME_SIMPLE_BUFF', 'CARD_TEXT_SIMPLE_BUFF',
                       ft, ft2, ft_numeric_large,
                       3,
                       img_card_frame_s, img_card_frame_l,
                       img_card_s, img_card_l)

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
            new_ap = t.ap + 2
            new_hp = t.hp + 2
            t.set_ap(new_ap)
            t.set_hp(new_hp)


########
# test #
########
if __name__ == '__main__':
    pygame.init()