"""
pygame_UI.py: This module is part of the game package.

This module utilizes Pygame, an open-source library designed for making
video games, to create and manage the User Interface (UI) of the game. It
establishes the controls, display settings, and game states, and handles
events such as user inputs.

This module may contain classes and functions to setup the game window,
draw graphics, and deal with elements like the main menu, game screens,
buttons, labels, and other interactive components.
"""

import pygame
from settings.settings import Settings

pygame.mixer.init()
settings = Settings()
screen = pygame.display.set_mode(
    (
        Settings.SCREEN_WIDTH,
        Settings.SCREEN_HEIGHT
    ),
    flags=0,
    depth=32
)
PLAYER1_INPUT = (
    pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE
)
PLAYER2_INPUT = (
    pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_RETURN
)

image_brick = [
    pygame.image.load("images/block_brick.png"),
    pygame.image.load("images/block_armor.png")
]

image_tank = [
    pygame.image.load("images/tank_level_0.png"),
    pygame.image.load("images/tank_level_1.png"),
    pygame.image.load("images/tank_level_2.png"),
    pygame.image.load("images/tank_level_3.png"),
    pygame.image.load("images/tank_level_4.png"),
    pygame.image.load("images/tank_level_5.png"),
    pygame.image.load("images/tank_level_6.png"),
    pygame.image.load("images/tank_level_7.png")
]
image_bangs = [
    pygame.image.load("images/bang_0.png"),
    pygame.image.load("images/bang_1.png"),
    pygame.image.load("images/bang_2.png")
]

image_bonuses = [
    pygame.image.load("images/bonus_star.png"),
    pygame.image.load("images/bonus_tank.png"),
    pygame.image.load("images/bonus_helmet.png"),
    # pygame.image.load("images/bonus_bomb.png"),
    # pygame.image.load("images/bonus_time.png"),
    # pygame.image.load("images/bonus_shovel.png")
]

sound_effects = {
    "star": pygame.mixer.Sound("sounds/star.wav"),
    "bonus": pygame.mixer.Sound("sounds/bonus.wav"),
    "impact": pygame.mixer.Sound("sounds/impact.wav"),
    "shoot": pygame.mixer.Sound("sounds/shoot.wav"),
    "track_long": pygame.mixer.Sound("sounds/track_long.wav"),
    "tank_hit": pygame.mixer.Sound("sounds/tank_hit.wav"),
    "block_hit": pygame.mixer.Sound("sounds/block_hit.wav")
}


class UI:
    """Manage and update the User Interface (UI) elements of the game."""

    def __init__(self, objects_list):
        """Initialize the UI elements."""
        pygame.init()
        self.objects = objects_list
        self.screen = pygame.display.set_mode(
            (
                settings.SCREEN_WIDTH,
                settings.SCREEN_HEIGHT
            ),
            0,
            32
        )
        self.font_ui = pygame.font.Font(None, 30)
        self.clock = pygame.time.Clock()

    def update(self):
        pass

    def draw_tank(self, obj, index):
        """Draw the tank on the gaming interface."""
        pygame.draw.rect(
            self.screen, obj.color,
            (5 + index * 500, 5, 22, 22)
        )

        tank_life_img = pygame.transform.scale(
            image_tank[0],
            (
                image_tank[0].get_width() - 15,
                image_tank[0].get_height() - 15
            )
        )

        tank_life_img_width = tank_life_img.get_width()
        lives = getattr(obj, 'lives')
        for i in range(lives):
            life_position = (
                i * (tank_life_img.get_width() + 2) + 5 + index * 500,
                5 + tank_life_img.get_height() + 2)
            self.screen.blit(tank_life_img, life_position)

        text = self.font_ui.render(str(getattr(obj, 'hit_points')), 1,
                                   obj.color)
        rect = text.get_rect(
            center=(5 + index * 500 + 32 + 22, 5 + 11))
        self.screen.blit(text, rect)

        # Draw tank rank
        rank_text = self.font_ui.render(f"Rank: {getattr(obj, 'rank')}", 1,
                                        obj.color)
        rank_rect = rank_text.get_rect(
            center=(5 + index * 500 + tank_life_img_width + 90, 5 + 11))
        self.screen.blit(rank_text, rank_rect)

    def draw_text(self, text, font, color, location):
        """
        Draws the specified text on the screen using the given font, color,
        and location.

        Parameters:
            text (str): The text to be displayed on the screen.
            font (pygame.font.Font): The font used for rendering the text.
            color (tuple): The color of the text, specified as a tuple of RGB
            values (red, green, blue).
            location (tuple): The location on the screen where the text should
            be drawn, specified as a tuple of x and y coordinates.

        Returns:
            None
        """
        render = font.render(text, True, color)
        rect = render.get_rect(center=location)
        self.screen.blit(render, rect)

    def draw_title_screen(self):
        """

        Draws the title screen for the game.

        Parameters:
            self: The current instance of the class.

        Returns:
            None

        """

        font_name = pygame.font.get_default_font()

        self.screen.fill(settings.BOARD_BACKGROUND_COLOR)
        logo = pygame.image.load("images/game_logo.jpg")
        logo = pygame.transform.scale(
            logo,
            (
                settings.SCREEN_WIDTH,
                settings.SCREEN_HEIGHT
            )
        )
        rect = logo.get_rect(
            center=(
                settings.SCREEN_WIDTH // 2,
                settings.SCREEN_HEIGHT // 2
            )
        )
        self.screen.blit(logo, rect.topleft)

        font = pygame.font.Font(font_name, settings.FONT_SIZE)
        self.draw_text(
            'Tanks Duel',
            font,
            settings.CYAN_COLOR,
            (
                settings.SCREEN_WIDTH // 2,
                settings.SCREEN_HEIGHT // 2 + 100
            )
        )

        font = pygame.font.Font(font_name, settings.SMALL_FONT_SIZE)
        self.draw_text(
            'Press Any Key to Start',
            font, settings.BLUE_COLOR,
            (
                settings.SCREEN_WIDTH // 2,
                settings.SCREEN_HEIGHT // 2 + 200
            )
        )
        pygame.display.update()

    def game_over(self, winner):
        """Perform actions when the game is over."""
        font_name = pygame.font.get_default_font()
        font = pygame.font.Font(font_name, 55)
        self.screen.fill(settings.BOARD_BACKGROUND_COLOR)  # black color
        # Game Over Text
        self.draw_text(
            'Game Over',
            font,
            settings.WHITE_COLOR,
            (
                settings.SCREEN_WIDTH // 2,
                settings.SCREEN_HEIGHT // 2 + 5
            )
        )

        self.draw_text(
            f'{winner} Won!',
            font,
            settings.WHITE_COLOR,
            (
                settings.SCREEN_WIDTH // 2,
                settings.SCREEN_HEIGHT // 2 + 80
            )
        )

        font = pygame.font.Font(font_name, 25)
        self.draw_text(
            'Press Any Key to restart',
            font,
            settings.WHITE_COLOR,
            (
                settings.SCREEN_WIDTH // 2,
                settings.SCREEN_HEIGHT // 2 + 200
            )
        )

    def draw(self):
        """Draw the UI elements on the gaming interface."""
        for i, obj in enumerate(self.objects):
            if obj.type == 'tank':
                self.draw_tank(obj, i)
        pygame.draw.line(
            self.screen,
            settings.WHITE_COLOR,
            (0, 3 * settings.GRID_HEIGHT),
            (settings.SCREEN_WIDTH, 3 * settings.GRID_HEIGHT)
        )
