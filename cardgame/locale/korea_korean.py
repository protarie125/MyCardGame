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
# Original - Knights of Consecration
CARD_NAME_ORIGINAL_SOLAR = u'축성 기사단 신입 솔라'
CARD_TEXT_ORIGINAL_SOLAR = u'턴개시시: 무작위 아군 필드 추종자 1의 방/체 +1/+1'

CARD_NAME_NEW_RECRUITS = u'신참 기사단원'
CARD_TEXT_NEW_RECRUITS = u''

CARD_NAME_BRAVE_LITTLE_KNIGHT = u'용감한 작은 기사단원'
CARD_TEXT_BRAVE_LITTLE_KNIGHT = u'방어시: 이 추종자의 방어력 +1'

CARD_NAME_RADIANT_SISTER = u'찬란한 수녀'
CARD_TEXT_RADIANT_SISTER = u'방어시: 이 추종자의 양옆에 있는 추종자들의 공/방 +1/+1'

########
# test #
########
if __name__ == '__main__':
    pygame.init()
