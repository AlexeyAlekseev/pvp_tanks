from random import randint

import pygame

from gameobjects.base import GameObject
from gameobjects.pygame_IU import (
    screen,
    image_brick,
    image_bangs,
    image_bonuses,
    image_tank, sound_effects
)
from settings.settings import Settings


class Bang(GameObject):
    def __init__(self, px, py, objects_list: list):
        super().__init__(objects_list)
        self.type = 'bang'
        self.px, self.py = px, py
        self.frame = 0
        self.image = image_bangs[0]
        self.rect = self.image.get_rect(center=(self.px, self.py))

    def get_rect(self):
        self.rect = self.image.get_rect(center=(self.px, self.py))

    def update(self):
        self.frame += 0.3
        if self.frame >= 3:
            self.objects_list.remove(self)

    def draw(self):
        image = image_bangs[int(self.frame)]
        rect = image.get_rect(center=(self.px, self.py))
        screen.blit(image, rect)

    def damage(self, value):
        pass


class Bonus(GameObject):
    def __init__(self, px, py, bonus_index, objects_list: list):
        super().__init__(objects_list)
        self.type = 'bonus'

        self.image = image_bonuses[bonus_index]
        self.rect = self.image.get_rect(center=(px, py))

        self.timer = 400
        self.bonus_index = bonus_index

    def update(self):
        if self.timer > 0:
            self.timer -= 1
        else:
            self.objects_list.remove(self)

        bonus_actions = {
            0: self.star,
            1: self.bonus_tank,
            2: self.bonus_helmet
        }

        if self.bonus_index in bonus_actions:
            bonus_actions[self.bonus_index]()

    def star(self):
        for obj in self.objects_list:
            if obj.type == 'tank' and self.rect.colliderect(obj.rect):
                sound_effects["star"].play()
                if obj.rank < len(image_tank) - 1:
                    obj.rank += 1
                    obj.speed += 0.3
                    obj.shoot_delay -= 10
                else:
                    pass
                self.objects_list.remove(self)

    def bonus_tank(self):
        for obj in self.objects_list:
            if obj.type == 'tank' and self.rect.colliderect(obj.rect):
                sound_effects["bonus"].play()
                if obj.lives < 6:
                    obj.lives += 1
                else:
                    pass
                self.objects_list.remove(self)

    def bonus_helmet(self):
        for obj in self.objects_list:
            if obj.type == 'tank' and self.rect.colliderect(obj.rect):
                sound_effects["bonus"].play()
                if obj.hit_points < 9:
                    obj.hit_points += 1
                else:
                    pass
                self.objects_list.remove(self)

    def draw(self):
        if self.timer % 30 < 15:
            screen.blit(self.image, self.rect)

    def damage(self, value):
        pass
