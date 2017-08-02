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


class StartSkill(Skill):
    def __init__(self, mother):
        Skill.__init__(self, mother, 'img_start')

    def activate(self):
        pass


class AtkSkill(Skill):
    def __init__(self, mother):
        Skill.__init__(self, mother, 'img_attack')

    def activate(self, target):
        pass


class DefSkill(Skill):
    def __init__(self, mother):
        Skill.__init__(self, mother, 'img_defence')

    def activate(self):
        pass


class AtkHpMinus2(AtkSkill):
    def __init__(self, mother):
        AtkSkill.__init__(self, mother)

    def activate(self, target):
        new_hp = target.hp - 2
        target.set_hp(new_hp)
        print("%s: hp -2 (by %s who controlled by %s)"
              % (target.name, self.mother.name, self.mother.control.name))


class DefHpPlus1(DefSkill):
    def __init__(self, mother):
        DefSkill.__init__(self, mother)

    def activate(self):
        new_hp = self.mother.hp + 1
        self.mother.set_hp(new_hp)
        print("%s: hp +1 (by %s who controlled by %s)"
              % (self.mother.name, self.mother.name, self.mother.control.name))


class DefDpPlus1(DefSkill):
    def __init__(self, mother):
        DefSkill.__init__(self, mother)

    def activate(self):
        new_dp = self.mother.dp + 1
        self.mother.set_dp(new_dp)
        print("%s: dp +1 (by %s who controlled by %s)"
              % (self.mother.name, self.mother.name, self.mother.control.name))


class DefAdjApPlus1DpPlus1(DefSkill):
    def __init__(self, mother):
        DefSkill.__init__(self, mother)

    def activate(self):
        you = self.mother.control
        field = you.field_slot
        n = 0
        for i in range(5):
            if field[n].card == self.mother:
                break
            else:
                n += 1
        if n == 0:
            t1 = field[1].card
            if t1.ctype == 'follower':
                new_ap1 = t1.ap + 1
                t1.set_ap(new_ap1)
                new_dp1 = t1.dp + 1
                t1.set_dp(new_dp1)
                print("%s: ap/dp +1/+1 (by %s who controlled by %s)"
                      % (t1.name, self.mother.name, self.mother.control.name))
        if n == 4:
            t1 = field[3].card
            if t1.ctype == 'follower':
                new_ap1 = t1.ap + 1
                t1.set_ap(new_ap1)
                new_dp1 = t1.dp + 1
                t1.set_dp(new_dp1)
                print("%s: ap/dp +1/+1 (by %s who controlled by %s)"
                      % (t1.name, self.mother.name, self.mother.control.name))
        else:
            t1 = field[n - 1].card
            t2 = field[n + 1].card
            if t1.ctype == 'follower':
                new_ap1 = t1.ap + 1
                t1.set_ap(new_ap1)
                new_dp1 = t1.dp + 1
                t1.set_dp(new_dp1)
                print("%s: ap/dp +1/+1 (by %s who controlled by %s)"
                      % (t1.name, self.mother.name, self.mother.control.name))
            if t2.ctype == 'follower':
                new_ap2 = t2.ap + 1
                t2.set_ap(new_ap2)
                new_dp2 = t2.dp + 1
                t2.set_dp(new_dp2)
                print("%s: ap/dp +1/+1 (by %s who controlled by %s)"
                      % (t2.name, self.mother.name, self.mother.control.name))

########
# test #
########
if __name__ == '__main__':
    pygame.init()
