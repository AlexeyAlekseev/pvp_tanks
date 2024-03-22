from gameobjects.base import GameObject
import pygame

from settings.settings import Settings
from gameobjects.gameobjects import Bang
from gameobjects.pygame_IU import screen


class Bullet(GameObject):
    """Manage the state and behavior of a Bullet in the game."""

    def __init__(self, parent, parent_x, parent_y, bullet_x, bullet_y, damage,
                 objects_list):
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
        """Update the state of the Bullet."""
        self.parent_x += self.bullet_x
        self.parent_y += self.bullet_y
        self.rect.x = self.parent_x
        self.rect.y = self.parent_y
        self.collision()

    def collision(self):
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
                    if obj.type is not 'block':
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
