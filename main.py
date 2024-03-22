import sys
from random import randint

import pygame

from gameobjects.gameobjects import Block, Bonus
from settings.settings import Settings
from gameobjects.pygame_IU import UI, PLAYER1_INPUT, PLAYER2_INPUT, \
    image_bonuses
from gameobjects.tank import Tank

settings = Settings()

game_objects = []
bullets = []
ui = UI(game_objects)

def create_objects():
    Tank(
        settings.RED_COLOR,
        settings.PLAYER1_INIT_POSITION,
        0,
        PLAYER1_INPUT,
        game_objects
    )
    Tank(
        settings.BLUE_COLOR,
        settings.PLAYER2_INIT_POSITION,
        0,
        PLAYER2_INPUT,
        game_objects
    )
    for _ in range(settings.BLOCKS_COUNT):
        Block.create_if_no_collision(game_objects, settings.GRID_SIZE)


def handle_game_over(objects):
    for obj in objects:
        if obj.type == 'tank' and obj.color == settings.RED_COLOR:
            win = 'Player 2'
        else:
            win = 'Player 2'
        ui.game_over(win)


def handle_gameplay_events(event, gameplay):
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    elif event.type == pygame.KEYDOWN:
        game_objects.clear()
        bullets.clear()
        gameplay = True
        create_objects()
    return gameplay


def handle_title_screen_events(event, game_status, title_screen):
    if event.type == pygame.QUIT:
        game_status = False
    elif event.type == pygame.KEYDOWN:
        title_screen = False
    return game_status, title_screen


def generate_bonus():
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
    create_objects()
    print(game_objects)
    print('*' * 120)
    print(bullets)
    print('*' * 120)
    for obj in game_objects:
        print(obj)

    while game_status:
        if title_screen:
            ui.draw_title_screen()
            pygame.display.update()

            for event in pygame.event.get():
                (game_status,
                 title_screen) = handle_title_screen_events(
                    event,
                    game_status,
                    title_screen
                )
        else:
            if gameplay:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                if bonus_timer > 0:
                    bonus_timer -= 1
                else:
                    generate_bonus()

                for bullet in bullets:
                    bullet.update()
                for obj in game_objects:
                    obj.update()

                ui.update()
                ui.screen.fill(settings.BOARD_BACKGROUND_COLOR)

                for bullet in bullets:
                    bullet.draw()

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
    running = True
    main()
