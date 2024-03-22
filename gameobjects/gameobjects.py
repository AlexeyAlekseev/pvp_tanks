from random import randint

import pygame

from gameobjects.base import GameObject
from gameobjects.pygame_IU import (
    screen,
    image_brick,
    image_bangs,
    image_bonuses,
    image_tank
)
from settings.settings import Settings


class Block(GameObject):
    """Manages the state and behavior of a Block in the game."""

    def __init__(self, obj_coordinates, size, objects_list):
        """Initialize the attributes of the Block."""
        super().__init__(objects_list)
        self.type = 'block'
        self.rect = pygame.Rect(obj_coordinates[0], obj_coordinates[1], size,
                                size)
        self.hit_points = 1

    def update(self):
        """Updates the state of the Block."""
        pass

    def damage(self, value):
        """Applies damage to the Block."""
        self.hit_points -= value
        if self.hit_points <= 0:
            self.objects_list.remove(self)

    def draw(self):
        """Draws the Block on the gaming interface."""
        screen.blit(image_brick, self.rect)

    @staticmethod
    def is_colliding(rect, objects_list):
        """Checks for collision between the Block and other objects."""
        for obj in objects_list:
            if rect.colliderect(obj.rect):
                return True
        return False

    @staticmethod
    def create_if_no_collision(objects_list, grid_size):
        """Creates an instance of Block if there's no collision."""
        while True:
            x = randint(
                0,
                Settings.SCREEN_WIDTH // Settings.GRID_SIZE - 1
            ) * Settings.GRID_SIZE
            y = randint(
                2,
                Settings.SCREEN_HEIGHT // Settings.GRID_SIZE - 1
            ) * Settings.GRID_SIZE
            rect = pygame.Rect(x, y, grid_size, grid_size)
            if not Block.is_colliding(rect, objects_list):
                return Block((x, y), grid_size, objects_list)


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

        self.timer = 600
        self.bonus_index = bonus_index

    def update(self):
        if self.timer > 0:
            self.timer -= 1
        else:
            self.objects_list.remove(self)

        for obj in self.objects_list:
            if obj.type == 'tank' and self.rect.colliderect(obj.rect):
                if self.bonus_index == 0 and obj.rank < 3:
                    if obj.rank < len(image_tank):
                        obj.rank += 1
                        obj.speed += 0.3
                        obj.shoot_delay -= 10
                        obj.hit_points += 1
                        self.objects_list.remove(self)
                        break

    def draw(self):
        if self.timer % 30 < 15:
            screen.blit(self.image, self.rect)

    def damage(self, value):
        pass
