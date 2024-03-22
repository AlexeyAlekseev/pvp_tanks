"""
blocks.py: This module is part of the gameobjects package.

This module contains the implementation of various kinds of blocks
used in the game. It provides classes and functions for creating,
manipulating, and interacting with game blocks.

Each block class defined in this module further extends the game's
interactive environment and controls the behavior of individual blocks.
"""

from random import randint
import pygame


from gameobjects.base import GameObject
from gameobjects.pygame_ui import (
    screen,
    image_brick,
    sound_effects
)
from settings.settings import Settings


class BrickBlock(GameObject):
    """A class representing a brick block.

    Attributes
    ----------
    type : str
        type of the block
    rect : Rect
        rectangle representing the block
    hit_points : int
        hit points of the block

    Methods
    -------
    update()
        Updates the state of the block.
    damage(value, rank=None)
        Applies damage to the block.
    draw()
        Draws the block on the gaming interface.
    is_colliding(rect, objects_list)
        Checks for collision between the block and other objects.
    create_if_no_collision(objects_list, grid_size)
        Creates an instance of block if there's no collision.
    """
    def __init__(self, obj_coordinates, size, objects_list):
        """Initialize the attributes of the Block."""
        super().__init__(objects_list)
        self.type = 'block'
        self.rect = pygame.Rect(obj_coordinates[0], obj_coordinates[1], size,
                                size)
        self.hit_points = 1

    def damage(self, value, rank=None):
        """Applies damage to the Block."""
        sound_effects["block_hit"].play()
        self.hit_points -= value
        if self.hit_points <= 0:
            self.objects_list.remove(self)

    def update(self):
        pass

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
    """

    ArmorBlock class is a subclass of BrickBlock class. It represents an
    Armor block in a game.

    Attributes:
        obj_coordinates (tuple): The coordinates of the ArmorBlock object.
        size (int): The size of the ArmorBlock object.
        objects_list (list): The list of all objects in the game.
        hit_points (int): The remaining hit points of the ArmorBlock object.

    Methods:
        __init__(self, obj_coordinates, size, objects_list)
            Initializes the attributes of the ArmorBlock object.
        damage(self, value, rank=None)
            Applies damage to the ArmorBlock object.
        draw(self)
            Draws the ArmorBlock on the gaming interface.
        create_if_no_collision(objects_list, grid_size)
            Creates an instance of ArmorBlock if there's no collision.
    """
    def __init__(self, obj_coordinates, size, objects_list):
        """Initialize the attributes of the ArmorBlock."""
        super().__init__(obj_coordinates, size, objects_list)
        self.hit_points = 1

    def damage(self, value, rank=None):
        """Applies damage to the Block."""
        sound_effects["block_hit"].play()
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
    def create_if_no_collision(objects_list: list, grid_size: int):
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
                return ArmorBlock(
                    (x, y),
                    grid_size,
                    objects_list
                )
