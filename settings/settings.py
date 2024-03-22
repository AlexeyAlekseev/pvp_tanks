from dataclasses import dataclass, field
import pygame


@dataclass()
class Settings:
    """

    This class represents the settings for a game. It contains various attributes that define the configuration of the game.

    Attributes:
    - BOARD_BACKGROUND_COLOR: The color of the game board's background as an RGB tuple of integers.
    - WHITE_COLOR: The color white as an RGB tuple of integers.
    - RED_COLOR: The color red as an RGB tuple of integers.
    - BLUE_COLOR: The color blue as an RGB tuple of integers.
    - GREEN_COLOR: The color green as an RGB tuple of integers.
    - CYAN_COLOR: The color cyan as an RGB tuple of integers.
    - FONT_SIZE: The font size for text in the game.
    - SMALL_FONT_SIZE: The smaller font size for text in the game.
    - SCREEN_WIDTH: The width of the game screen in pixels.
    - SCREEN_HEIGHT: The height of the game screen in pixels.
    - GRID_SIZE: The size of the grid in the game.
    - GRID_WIDTH: The number of grid squares horizontally on the game screen.
    - GRID_HEIGHT: The number of grid squares vertically on the game screen.
    - SCREEN_CENTER: The coordinates of the center point of the game screen.
    - PLAYER1_INIT_POSITION: The initial position of player 1 on the game screen.
    - PLAYER2_INIT_POSITION: The initial position of player 2 on the game screen.
    - HP: The number of health points for each player.
    - LIVES: The number of lives for each player.
    - SPEED: The speed of the players in the game.
    - FPS: The frames per second for the game.
    - BLOCKS_COUNT: The number of blocks in the game.
    - MOVES_INPUT: The valid moves input for the players as a list of coordinate changes.
    - SPACING: The spacing between elements in the game.
    - MAX_ATTEMPTS: The maximum number of attempts for a certain action in the game.

    """
    BOARD_BACKGROUND_COLOR: tuple[int, int, int] = (0, 0, 0)
    WHITE_COLOR: tuple[int, int, int] = (255, 255, 255)
    RED_COLOR: tuple[int, int, int] = (255, 0, 0)
    BLUE_COLOR: tuple[int, int, int] = (0, 0, 255)
    GREEN_COLOR: tuple[int, int, int] = (0, 255, 0)
    CYAN_COLOR: tuple[int, int, int] = (0, 255, 255)

    FONT_SIZE: int = 55
    SMALL_FONT_SIZE: int = 25

    SCREEN_WIDTH: int = 800
    SCREEN_HEIGHT: int = 602
    GRID_SIZE: int = 32
    GRID_WIDTH: int = SCREEN_WIDTH // GRID_SIZE
    GRID_HEIGHT: int = SCREEN_HEIGHT // GRID_SIZE
    SCREEN_CENTER: tuple[int, int] = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    PLAYER1_INIT_POSITION: tuple[int, int] = (
        round(SCREEN_WIDTH * 0.1),
        SCREEN_HEIGHT // 1.7
    )
    PLAYER2_INIT_POSITION: tuple[int, int] = (
        round(SCREEN_WIDTH * 0.9),
        SCREEN_HEIGHT // 2.3
    )

    HP: int = 5
    LIVES: int = 3
    SPEED: int = 2
    FPS: int = 60

    BLOCKS_COUNT: int = 150

    MOVES_INPUT = [[0, -1], [1, 0], [0, 1], [-1, 0]]

    SPACING: int = 5
    MAX_ATTEMPTS: int = 1000
