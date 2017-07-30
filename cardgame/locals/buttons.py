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


###########
# classes #
###########
class Button:
    def __init__(self, rect, font, text):
        self.rect = rect
        self.font = font
        self.text = text
        self.available = False
        self.mouse_over = False

    def check_mouse_over(self, mx, my):
        self.mouse_over = self.rect.collidepoint(mx, my)

    def draw(self, display):
        pygame.draw.rect(display, cnst.white, self.rect, 1)

        text_surf = self.font.render(self.text, True, cnst.white)
        text_rect = text_surf.get_rect()
        text_rect.center = self.rect.center
        display.blit(text_surf, text_rect)


class CardUseButton(Button):
    def __init__(self, rect, mother):
        Button.__init__(self, rect, mother.ft, 'USE')

        self.mother = mother

    def set_rect(self):
        self.rect.centerx = self.mother.rect.centerx
        self.rect.bottom = self.mother.rect.top

    def draw(self, display):
        if self.available:
            self.set_rect()
            pygame.draw.rect(display, cnst.white, self.rect, 1)

            use_text_surf = self.font.render(self.text, True, cnst.white)
            use_text_rect = use_text_surf.get_rect()
            use_text_rect.center = self.rect.center
            display.blit(use_text_surf, use_text_rect)


########
# test #
########
if __name__ == '__main__':
    pygame.init()
