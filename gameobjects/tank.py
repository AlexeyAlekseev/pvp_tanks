from random import randint

import pygame
from gameobjects.base import GameObject
from gameobjects.bullet import Bullet
from gameobjects.gameobjects import Block
from settings.settings import Settings
from gameobjects.pygame_IU import image_tank, screen


class Tank(GameObject):
    """Manage the state and behavior of a Tank in the game."""

    def __init__(
            self,
            color: tuple[int, int, int],
            obj_coordinates: tuple[int, int],
            direct: int,
            move_input: tuple[int, int, int, int, int],
            objects_list: list
    ):
        """Initialize the attributes of the Tank."""
        super().__init__(objects_list)
        self.type = 'tank'
        self.color = color
        self.rank = 0
        self.direct = direct
        self.rect = pygame.Rect(obj_coordinates[0], obj_coordinates[1],
                                Settings.GRID_SIZE, Settings.GRID_SIZE)
        self.image = pygame.transform.rotate(image_tank[self.rank],
                                             -self.direct * 90)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.speed = Settings.SPEED
        self.hit_points = Settings.HP
        self.lives = Settings.LIVES

        self.move_left = move_input[0]
        self.move_right = move_input[1]
        self.move_up = move_input[2]
        self.move_down = move_input[3]
        self.key_shoot = move_input[4]

        self.shoot_timer = 0
        self.shoot_delay = 60
        self.bullet_speed = 5
        self.bullet_damage = 1

    def update(self):
        """Update the state of the Tank."""
        self.change_tank_state()
        new_x, new_y = self.check_boundaries()
        self.update_position(new_x, new_y)
        self.check_collisions(new_x, new_y)
        self.shoot_bullet()

    def check_boundaries(self):
        """Checks and adjusts for boundaries"""
        keys = pygame.key.get_pressed()

        # Initialize new_x and new_y as the original positions
        new_x, new_y = self.rect.topleft

        if keys[self.move_left]:
            new_x -= self.speed
            if new_x < 0:
                new_x = 0
            self.direct = 3
        elif keys[self.move_right]:
            new_x += self.speed
            if new_x > Settings.SCREEN_WIDTH - self.rect.width:
                new_x = Settings.SCREEN_WIDTH - self.rect.width
            self.direct = 1
        elif keys[self.move_up]:
            new_y -= self.speed
            if new_y < 0:
                new_y = 0
            self.direct = 0
        elif keys[self.move_down]:
            new_y += self.speed
            if new_y > (Settings.SCREEN_HEIGHT - 2) - self.rect.height:
                new_y = (Settings.SCREEN_HEIGHT - 2) - self.rect.height
            self.direct = 2

        return new_x, new_y

    def update_position(self, new_x: int, new_y: int) -> None:
        """Updates the position if not in the top row of the grid"""
        if new_y < 2 * Settings.GRID_SIZE:
            new_y = 2 * Settings.GRID_SIZE
        self.rect.x, self.rect.y = new_x, new_y

    def check_collisions(self, new_x: int, new_y: int) -> None:
        """Checks for collision with other objects"""
        for obj in self.objects_list:
            if obj != self and obj.type != 'bonus' and self.rect.colliderect(
                    obj.rect):
                self.rect.topleft = new_x, new_y

    def shoot_bullet(self):
        """Checks if shooting is possible and shoots"""
        keys = pygame.key.get_pressed()
        if keys[self.key_shoot] and self.shoot_timer == 0:
            bullet_x = Settings.MOVES_INPUT[self.direct][0] * self.bullet_speed
            bullet_y = Settings.MOVES_INPUT[self.direct][1] * self.bullet_speed
            Bullet(self, self.rect.centerx, self.rect.centery, bullet_x,
                   bullet_y, self.bullet_damage, self.objects_list)
            self.shoot_timer = self.shoot_delay

        if self.shoot_timer > 0:
            self.shoot_timer -= 1

    def change_tank_state(self):
        """Change image and direction based on the Tank state"""
        self.image = pygame.transform.rotate(
            image_tank[self.rank],
            -self.direct * 90
        )
        self.image = pygame.transform.scale(
            self.image,
            (
                self.image.get_width() - 5,
                self.image.get_height() - 5
            )
        )
        self.rect = self.image.get_rect(center=self.rect.center)

    def draw(self):
        """Draw the Tank on the gaming interface."""
        screen.blit(self.image, self.rect)

    def damage(self, value):
        """Apply damage to the Tank."""
        self.hit_points -= value
        if self.rank > 0:
            self.rank -= value
        else:
            self.rank = 0
        if self.hit_points <= 0:
            self.reset()

    @staticmethod
    def create_if_no_collision(objects_list, grid_size):
        """Create the tank if there's no collision."""
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
                return x, y

    def reset(self):
        """Reset the tank's state."""
        x, y = self.create_if_no_collision(
            self.objects_list,
            Settings.GRID_SIZE
        )
        self.rect = pygame.Rect(x, y, Settings.GRID_SIZE, Settings.GRID_SIZE)

        self.rank = 0
        self.speed = Settings.SPEED
        self.hit_points = Settings.HP
        self.shoot_timer = 0
        self.shoot_delay = Settings.FPS
        self.bullet_speed = 5
        self.bullet_damage = 1
        self.lives -= 1
