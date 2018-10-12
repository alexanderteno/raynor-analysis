#!/usr/bin/env python3

from enum import Enum
from collections import namedtuple
from functools import reduce

Status = namedtuple('Status', 'status_effect duration')


class StatusEffect(Enum):
    SLOWED = 0


class RaynorTalent(Enum):
    VETERAN_MARKSMAN = 0
    ACE_IN_THE_HOLE = 1
    UNSTABLE_COMPOUND = 2
    RAYNORS_RAIDER = 3


class Enemy:
    def __init__(self):
        self.__statuses = []

    def apply_status_effect(self, status_effect, duration):
        self.__statuses.append(Status(status_effect, duration))

    def has_status(self, status_effect):
        for status in self.__statuses:
            if status.status_effect is status_effect:
                return True
        return False

    def add_damage(self, amount):
        self.__damage += amount


class Raynor:

    BASE_ATTACK = 101
    BASE_SCALE = 0.04
    ACE_IN_THE_HOLE = 0.15
    VETERAN_MARKSMAN = 0.0075
    ATTACK_SPEED = 1.25
    GIVE_EM_SOME_PEPPER = 1.25
    RAIDER_BASE_DAMAGE = 84
    RAIDER_BASE_SCALE = 0.04

    def __init__(self, level, talents):
        self.__level = level
        self.__talents = talents
        self.__attack_count = 0

    def has_veteran_marksman(self):
        return RaynorTalent.VETERAN_MARKSMAN in self.__talents

    def has_ace_in_the_hole(self):
        return RaynorTalent.ACE_IN_THE_HOLE in self.__talents

    def has_raynors_raider(self):
        return RaynorTalent.RAYNORS_RAIDER in self.__talents

    def give_em_same_pepper(self):
        return (self.attack_count + 1 % 4) == 0

    def calculate_damage(self, target):
        pepper_damage = 0 if self.give_em_some_pepper() else 0


def main():

    # vm_raynor_1 = Raynor(1, [RaynorTalent.VETERAN_MARKSMAN])
    enemy = Enemy()
    print(enemy.has_status(StatusEffect.SLOWED))
    enemy.apply_status_effect(StatusEffect.SLOWED, 1)
    print(enemy.has_status(StatusEffect.SLOWED))


if __name__ == '__main__':
    main()
