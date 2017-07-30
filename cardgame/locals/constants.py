# -*- coding: utf-8 -*-

# Card Game 2 v0.0
# By Arie, Prot (2017)
# protarie@gmail.com
# CC BY-NC-SA 3.0

##########
# import #
##########
import pygame

###########
# globals #
###########
# fps
fps = 60
fps_clock = pygame.time.Clock()
delta_time = 1 / fps

# window
window_x = 1050
window_y = 800

# sizes
card_s_x = 126
card_s_y = 176

card_l_x = 252
card_l_y = 352

half_card_l_x = int(card_l_x / 2)

card_base_rect = pygame.Rect(0, 0, card_s_x, card_s_y)

img_l_rect = pygame.Rect(0, 0, card_l_x, card_l_y)
img_l_rect.right = window_x

right_field_border_rect = pygame.Rect(0, 0, 20, window_y)
right_field_border_rect.right = window_x - img_l_rect.width

field_width = window_x - img_l_rect.width - right_field_border_rect.width

card_name_rect_g = pygame.Rect(0, card_l_y, card_l_x, 50)
card_name_rect_g.right = window_x

use_button_rect = pygame.Rect(0, 0, 80, 30)

turn_end_button_rect = pygame.Rect(0, 0, card_s_x, card_s_y - card_s_x)
turn_end_button_rect.right = window_x - card_l_x - right_field_border_rect.width
turn_end_button_rect.bottom = window_y

fs_size_rect_g = pygame.Rect(0, 0, card_s_x, card_s_x)
fs_size_rect_g.bottomright = turn_end_button_rect.topright

menu_button_rect = pygame.Rect(0, 0, half_card_l_x, 30)
menu_button_rect.bottomright = (window_x, window_y)

shuffle_button_rect = pygame.Rect(0, 0, half_card_l_x, 30)
shuffle_button_rect.bottomright = (menu_button_rect.left, window_y)

text_box_rect_g = pygame.Rect(0, 0, 252, window_y - card_l_y - 140)
text_box_rect_g.right = window_x
text_box_rect_g.bottom = window_y - 30

coin_flip_pos = (int((window_x - card_l_x - right_field_border_rect.width) / 2), int(10 + 1.5 * card_s_y))
coin_flip_radius = 100

# mouse
mouse_x = 0
mouse_y = 0

# colors
white = (255, 255, 255, 255)
black = (35, 31, 32, 255)
red = (255, 0, 0, 255)
green = (0, 255, 0, 255)
gray = (122, 122, 122, 255)
blue = (20, 70, 200, 255)
violet = (230, 50, 210, 255)
coin_red = (241, 115, 172, 200)
coin_blue = (0, 192, 243, 200)

# others
first_now = None
very_first = True

########
# test #
########
if __name__ == '__main__':
    pygame.init()
