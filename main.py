#!/usr/bin/env python3

from enum import Enum
from collections import namedtuple

Status = namedtuple('Status', 'status_effect duration')


class StatusEffect(Enum):
    SLOWED = 0


class EnemyType(Enum):
    HERO = 0
    MINION = 1


class RaynorTalent(Enum):
    VETERAN_MARKSMAN = 0
    ACE_IN_THE_HOLE = 1
    UNSTABLE_COMPOUND = 2
    RAYNORS_RAIDER = 3


class Enemy:
    def __init__(self, enemy_type):
        self.__statuses = []
        self.__enemy_type = enemy_type
        self.__damage = 0

    def __repr__(self):
        return 'Enemy(statuses={},enemy_type={},damage={})'.format(
            self.__statuses, self.__enemy_type, self.__damage)

    def apply_status_effect(self, status_effect, duration):
        self.__statuses.append(Status(status_effect, duration))

    def has_status(self, status_effect):
        for status in self.__statuses:
            if status.status_effect is status_effect:
                return True
        return False

    def is_hero(self):
        return self.__enemy_type is EnemyType.HERO

    def add_damage(self, amount):
        self.__damage += amount

    def increment_time(self, amount):
        filtered_statuses = filter(
            lambda status: (status.duration - amount) > 0, self.__statuses)
        self.__statuses = list(
            map(lambda status: Status(status.status_effect, status.duration - amount),
                filtered_statuses))


class Raynor:

    BASE_ATTACK = 101
    BASE_SCALE = 0.04
    ACE_IN_THE_HOLE = 0.15
    VETERAN_MARKSMAN = 0.0075
    ATTACK_SPEED = 1.25
    GIVE_EM_SOME_PEPPER = 1.25
    RAIDER_BASE_DAMAGE = 84
    RAIDER_BASE_SCALE = 0.04
    UNSTABLE_COMPOUND_DURATION = 2.5

    def __init__(self, level, talents):
        self.__level = level
        self.__talents = talents
        self.__pepper_counter = 0
        self.__veteran_marksman_count = 0

    def __repr__(self):
        return (
            'Raynor(level={},talents={},veteran_marksman_count={},pepper_count'
            'er={})').format(self.__level, self.__talents,
                             self.__veteran_marksman_count,
                             self.__pepper_counter)

    def has_veteran_marksman(self):
        return RaynorTalent.VETERAN_MARKSMAN in self.__talents

    def has_ace_in_the_hole(self):
        return RaynorTalent.ACE_IN_THE_HOLE in self.__talents

    def has_raynors_raider(self):
        return RaynorTalent.RAYNORS_RAIDER in self.__talents

    def has_unstable_compound(self):
        return RaynorTalent.UNSTABLE_COMPOUND in self.__talents

    def attack_will_pepper(self):
        return (self.attack_count + 1 % 4) == 0

    def increment_pepper_counter(self, target):
        self.__pepper_counter = (self.__pepper_counter + 1) % 4
        if self.__pepper_counter == 0 and self.has_veteran_marksman() and \
                target.is_hero():
            self.__veteran_marksman_count += 1
        if (self.__pepper_counter == 0 and self.has_unstable_compound()):
            target.apply_status_effect(StatusEffect.SLOWED,
                                       Raynor.UNSTABLE_COMPOUND_DURATION)

    def get_pepper_damage(self):
        if self.__pepper_counter != 0:
            return 0
        pepper_modifier = Raynor.GIVE_EM_SOME_PEPPER + \
            self.__veteran_marksman_count * Raynor.VETERAN_MARKSMAN
        return Raynor.BASE_ATTACK * pepper_modifier

    def get_ace_in_the_hole_modifier(self, target):
        return Raynor.ACE_IN_THE_HOLE if self.has_ace_in_the_hole(
        ) and target.has_status(StatusEffect.SLOWED) else 0

    def scale_attack(self, amount):
        return amount * (1 + Raynor.BASE_SCALE)**self.__level

    def attack(self, target):
        self.increment_pepper_counter(target)
        ace_in_the_hole_modifier = 1 + self.get_ace_in_the_hole_modifier(target)
        damage = (Raynor.BASE_ATTACK + self.get_pepper_damage()
                  ) * ace_in_the_hole_modifier
        target.add_damage(self.scale_attack(damage))


def main():

    vm_raynor_1 = Raynor(1, [RaynorTalent.VETERAN_MARKSMAN])
    vm_raynor_7 = Raynor(
        7, [RaynorTalent.VETERAN_MARKSMAN, RaynorTalent.UNSTABLE_COMPOUND])
    aith_raynor_1 = Raynor(1, [RaynorTalent.ACE_IN_THE_HOLE])
    aith_raynor_7 = Raynor(
        7, [RaynorTalent.ACE_IN_THE_HOLE, RaynorTalent.UNSTABLE_COMPOUND])

    vm_enemy_1 = Enemy(EnemyType.HERO)
    vm_enemy_7 = Enemy(EnemyType.HERO)
    aith_enemy_1 = Enemy(EnemyType.HERO)
    aith_enemy_7 = Enemy(EnemyType.HERO)

    pairs = [
        (vm_raynor_1, vm_enemy_1),
        (vm_raynor_7, vm_enemy_7),
        (aith_raynor_1, aith_enemy_1),
        (aith_raynor_7, aith_enemy_7),
    ]

    for attack_number in range(500):
        print_attack = attack_number % 50 == 0
        if print_attack:
            print('ATTACK NUMBER: {}'.format(attack_number))
        for (raynor, enemy) in pairs:
            enemy.increment_time(Raynor.ATTACK_SPEED)
            raynor.attack(enemy)
            if print_attack:
                print(raynor)
                print(enemy)
                print('\n')


if __name__ == '__main__':
    main()
