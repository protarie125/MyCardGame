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


###########
# classes #
###########
class Skill:
    def __init__(self, mother, img):
        self.mother = mother
        self.img = img


class AtkSkill(Skill):
    def __init__(self, mother):
        Skill.__init__(self, mother, 'attack')

    def activate(self, target):
        pass


class DefSkill(Skill):
    def __init__(self, mother):
        Skill.__init__(self, mother, 'defence')

    def activate(self):
        pass


class AtkHpMinus2(AtkSkill):
    def __init__(self, mother):
        AtkSkill.__init__(self, mother)

    def activate(self, target):
        new_hp = target.hp - 2
        target.set_hp(new_hp)
        print("%s: hp -2" % target.name)


class DefHpPlus1(DefSkill):
    def __init__(self, mother):
        DefSkill.__init__(self, mother)

    def activate(self):
        new_hp = self.mother.hp + 1
        self.mother.set_hp(new_hp)
        print("%s: hp +1" % self.mother.name)


class DefDpPlus1(DefSkill):
    def __init__(self, mother):
        DefSkill.__init__(self, mother)

    def activate(self):
        new_dp = self.mother.dp + 1
        self.mother.set_dp(new_dp)
        print("%s: dp +1" % self.mother.name)


########
# test #
########
if __name__ == '__main__':
    pygame.init()
