# -*- coding: utf-8 -*-

# Card Game 2 v0.0
# By Arie, Prot (2017)
# protarie@gmail.com
# CC BY-NC-SA 3.0

##########
# import #
##########
import pygame
from cardgame.locals import constants as cnst


def multi_render(display, ft, text):
    t = text
    potion = []

    while len(t) > 23:
        temp = t[:23]
        potion.append(temp)
        t = t[23:]
    potion.append(t)

    h = 0
    for p in potion:
        text_surf = ft.render("%s" % p, True, cnst.white)
        text_rect = text_surf.get_rect()
        text_rect.left = cnst.text_box_rect_g.left + 5
        text_rect.top = cnst.text_box_rect_g.top + h
        display.blit(text_surf, text_rect)
        h += 15


def outlined_render(display, ft, text, c_in, c_out, rect_g):
    text_in_surf = ft.render("%s" % text, True, c_in)
    text_in_rect = text_in_surf.get_rect()
    text_in_rect.center = rect_g.center

    text_out_surf = ft.render("%s" % text, True, c_out)
    text_out_rect = text_out_surf.get_rect()
    text_out_rect.center = rect_g.center

    h = 1

    o1 = text_out_rect.copy()
    o1.left -= h
    o1.top -= h

    o2 = o1.copy()
    o2.left += h

    o3 = o2.copy()
    o3.left += h

    o4 = o3.copy()
    o4.top += h

    o5 = o4.copy()
    o5.top += h

    o6 = o5.copy()
    o6.left -= h

    o7 = o6.copy()
    o7.left -= h

    o8 = o7.copy()
    o8.top -= h

    r = [o1, o2, o3, o4, o5, o6, o7, o8]
    for o in r:
        display.blit(text_out_surf, o)
    display.blit(text_in_surf, text_in_rect)


########
# test #
########
if __name__ == '__main__':
    pygame.init()
