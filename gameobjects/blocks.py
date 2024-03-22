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


class BrickBlock(GameObject):
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

    def damage(self, value, rank=None):
        """Applies damage to the Block."""
        sound_effects["block_hit"].play()
        self.hit_points -= value
        if self.hit_points <= 0:
            self.objects_list.remove(self)

    def draw(self):
        """Draws the Block on the gaming interface."""
        screen.blit(image_brick[0], self.rect)

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
            if not BrickBlock.is_colliding(rect, objects_list):
                return BrickBlock((x, y), grid_size, objects_list)


class ArmorBlock(BrickBlock):

    def __init__(self, obj_coordinates, size, objects_list):
        """Initialize the attributes of the ArmorBlock."""
        super().__init__(obj_coordinates, size, objects_list)
        self.hit_points = 1

    def damage(self, value, rank=None):
        """Applies damage to the Block."""
        if rank >= 3:
            self.hit_points -= value
            if self.hit_points <= 0:
                self.objects_list.remove(self)
        else:
            pass

    def draw(self):
        """Draws the Block on the gaming interface."""
        screen.blit(image_brick[1], self.rect)

    @staticmethod
    def create_if_no_collision(objects_list, grid_size):
        """Creates an instance of ArmorBlock if there's no collision."""
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
            if not BrickBlock.is_colliding(rect, objects_list):
                return ArmorBlock((x, y), grid_size, objects_list)