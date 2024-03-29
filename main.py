import sys
from random import randint
from typing import List

import pygame

from gameobjects.base import GameObject
from gameobjects.blocks import BrickBlock, ArmorBlock
from gameobjects.gameobjects import Bonus
from settings.settings import Settings
from gameobjects.pygame_ui import (
    UI,
    PLAYER1_INPUT,
    PLAYER2_INPUT,
    image_bonuses
)
from gameobjects.tank import Tank

settings = Settings()

game_objects = []
ui = UI(game_objects)


def create_objects():
    """
    Create objects for the game.

    This method creates instances of the Tank and BrickBlock classes and
    adds them to the game_objects list. It initializes two Tank objects with
    the given color, initial position, input * type, game_objects list,
    and movement speed. It also creates a number of BrickBlock objects based
    on the BLOCKS_COUNT constant and the size of the game grid.

    Parameters:
    None

    Returns:
    None
    """
    Tank(
        settings.RED_COLOR,
        settings.PLAYER1_INIT_POSITION,
        0,
        PLAYER1_INPUT,
        game_objects,
        4
    )
    Tank(
        settings.BLUE_COLOR,
        settings.PLAYER2_INIT_POSITION,
        0,
        PLAYER2_INPUT,
        game_objects,
        3
    )
    for _ in range(settings.BLOCKS_COUNT):
        BrickBlock.create_if_no_collision(game_objects, settings.GRID_SIZE)


def update_objects(timer: int) -> None:
    """

    Update Objects

    Updates the game objects based on the given timer.

    :param timer: The current timer value in milliseconds.
    :type timer: int

    """
    if timer % (60 * settings.FPS) == 0:  # Каждую минуту
        bricks_to_replace = [block for block in game_objects if
                             isinstance(block, BrickBlock)]
        for brick in bricks_to_replace:
            game_objects.remove(brick)
            if randint(0, 100) < 30:
                ArmorBlock.create_if_no_collision(game_objects,
                                                  settings.GRID_SIZE)
            else:
                BrickBlock.create_if_no_collision(game_objects,
                                                  settings.GRID_SIZE)


def handle_game_over(objects: List[GameObject]) -> None:
    """
    Handles the game over logic.

    Parameters:
        objects (list): The list of game objects.

        Returns:
            None
    """
    for obj in objects:
        if obj.type == 'tank' and obj.color == settings.RED_COLOR:
            win = 'Player 2'
        else:
            win = 'Player 2'
        ui.game_over(win)


def handle_gameplay_events(event, gameplay):
    """
    Handle gameplay events.

    This method is responsible for handling various events that occur during
    gameplay.

    Parameters:
    - event: The event object representing the specific event that occurred.
    - gameplay: The current gameplay state.

    Returns:
    - gameplay: The updated gameplay state after handling the event.

    """
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    elif event.type == pygame.KEYDOWN:
        game_objects.clear()
        gameplay = True
        create_objects()
    return gameplay


def handle_title_screen_events(event, game_status, title_screen):
    """Handle title screen events.

    Parameters:
    - event (pygame.event.Event): The event object representing the event being
      handled.
    - game_status (bool): The current status of the game.
    - title_screen (bool): The current status of the title screen.

    Returns:
    - game_status (bool): The updated status of the game.
    - title_screen (bool): The updated status of the title screen.

    This method is responsible for handling events that occur on the
    title screen. It checks the type of the event and performs different
    actions accordingly. If the event type is pygame

    *.QUIT, it sets the game_status to False, indicating that the game should
      quit. If the event type is pygame.KEYDOWN,
      it sets the title_screen to False, indicating that the title screen
    * should be closed.

    Note: Make sure you have imported the pygame module before using this
          method.

    Example usage:
    ```
    import pygame

    game_status = True
    title_screen = True

    while game_status:
        for event in pygame.event.get():
            game_status, title_screen = handle_title_screen_events(
            event,
            game_status,
            title_screen
            )
    ```
    """
    if event.type == pygame.QUIT:
        game_status = False
    elif event.type == pygame.KEYDOWN:
        title_screen = False
    return game_status, title_screen


def generate_bonus():
    """

    Generate a bonus object and set a random timer for the next bonus.

    Returns:
        int: The randomly generated bonus timer.

    """
    Bonus(randint(50, settings.SCREEN_WIDTH - 50),
          randint(50, settings.SCREEN_HEIGHT - 50),
          randint(0, len(image_bonuses) - 1),
          game_objects
          )
    bonus_timer = randint(120, 240)
    return bonus_timer


def main():
    """Entry point of the game, setting up initial state and running the
    game loop."""
    bonus_timer = 1
    title_screen = True
    game_status = True
    gameplay = True
    game_timer = 0
    create_objects()
    music_started = False

    while game_status:
        if title_screen:
            ui.draw_title_screen()
            pygame.display.update()
            music_started = False

            for event in pygame.event.get():
                (game_status,
                 title_screen) = handle_title_screen_events(
                    event,
                    game_status,
                    title_screen
                )
        else:
            if not music_started:
                pygame.mixer.music.load("sounds/main.mp3")
                pygame.mixer.music.play()
                music_started = True

            if gameplay:
                game_timer += 1
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                if bonus_timer > 0:
                    bonus_timer -= 1
                else:
                    bonus_timer = generate_bonus()

                update_objects(game_timer)

                for obj in game_objects:
                    obj.update()

                ui.update()
                ui.screen.fill(settings.BOARD_BACKGROUND_COLOR)

                for obj in game_objects:
                    obj.draw()

                ui.draw()

                for obj in game_objects:
                    if obj.type == 'tank' and obj.lives < 1:
                        gameplay = False

            else:
                handle_game_over(game_objects)
                for event in pygame.event.get():
                    gameplay = handle_gameplay_events(event, gameplay)
            pygame.display.update()
            ui.clock.tick(settings.FPS)


if __name__ == '__main__':
    main()
