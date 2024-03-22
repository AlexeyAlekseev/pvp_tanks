"""
bullet.py: This module is part of the gameobjects package.

This module provides the implementation for the bullets used in the game. It
contains classes and functions for creating and manipulating game bullets,
including their speed, direction, damage, and interactions when they hit
other game objects.
"""
from typing import NoReturn
import pygame

from settings.settings import Settings
from gameobjects.base import GameObject
from gameobjects.gameobjects import Bang
from gameobjects.pygame_ui import screen


class Bullet(GameObject):
    """Manage the state and behavior of a Bullet in the game."""

    def __init__(self,
                 parent: GameObject,
                 parent_x: int,
                 parent_y: int,
                 bullet_x: int,
                 bullet_y: int,
                 damage: int,
                 objects_list: list) -> NoReturn:
        """Initialize the attributes of the Bullet."""
        super().__init__(objects_list)
        self.type = 'bullet'
        self.parent = parent
        self.parent_x, self.parent_y = parent_x, parent_y
        self.bullet_x, self.bullet_y = bullet_x, bullet_y
        self._damage = damage
        self.hit_points = 1
        self.rect = pygame.Rect(parent_x, parent_y, 10, 10)

    def update(self):
        """
        Updates the position of the object.

        This method updates the position of the object based on the values
        of `bullet_x` and `bullet_y`. It increments the `parent_x` value by
        `bullet_x` and increments the `parent_y` value * by `bullet_y`. Then
        it updates the `rect` attributes `x` and `y` with the new values of
        `parent_x` and `parent_y`. Finally, it calls the `collision` method
        to handle any collisions * that might have occurred.

        """
        self.parent_x += self.bullet_x
        self.parent_y += self.bullet_y
        self.rect.x = self.parent_x
        self.rect.y = self.parent_y
        self.collision()

    def collision(self):
        """
        Check for collisions and handle the consequences.

        Checks if the parent object is within the boundaries of the screen.
        If it is not, the parent object will be removed from the objects list.

        If the parent object is within the boundaries, it loops over all
        objects in the objects list and checks for collisions. It skips over
        the parent object and any objects with types 'bonus *' or 'bang'. If
        a collision is detected with an object of type 'block', it calls the
        `damage` method on the object with the damage value and the parent's
        rank as arguments. If a collision * is detected with any other
        object, it calls the `damage` method on the object with the damage
        value and the parent as arguments. It then adds the parent object to
        the to_remove list *, creates a 'Bang' object at the parent's
        coordinates, and breaks out of the loop.

        After checking for collisions, if there are any objects in the
        to_remove list, it removes each object from the objects list.

        Parameters:
            self: The instance of the class.

        Returns:
            None
        """
        to_remove = []
        if not (
                0 <= self.parent_x <= Settings.SCREEN_WIDTH and
                0 <= self.parent_y <= Settings.SCREEN_HEIGHT
        ):
            to_remove.append(self)
        else:
            for obj in self.objects_list:
                if (obj is not self and
                        obj is not self.parent and
                        obj.type not in (
                        'bonus', 'bang') and self.rect.colliderect(
                            obj.rect)):
                    if obj.type != 'block':
                        obj.damage(self._damage, self)
                    else:
                        obj.damage(self._damage, rank=self.parent.rank)
                    to_remove.append(self)
                    Bang(self.parent_x, self.parent_y, self.objects_list)
                    break

        if to_remove:
            for bullet in to_remove:
                self.objects_list.remove(bullet)

    def damage(self, value, rank=None):
        """Apply damage to what the Bullet hits."""
        self.hit_points -= value
        if self.hit_points <= 0:
            self.objects_list.remove(self)

    def draw(self):
        """Draw the Bullet on the gaming interface."""
        pygame.draw.circle(screen, 'yellow', (self.parent_x,
                                              self.parent_y), 2)
