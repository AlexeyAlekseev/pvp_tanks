import sys
from random import randint

import pygame

BOARD_BACKGROUND_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)
RED_COLOR = (255, 0, 0)
BLUE_COLOR = (0, 0, 255)
GREEN_COLOR = (0, 255, 0)
CYAN_COLOR = (0, 255, 255)

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SCREEN_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
PLAYER1_INIT_POSITION = (round(SCREEN_WIDTH * 0.1), SCREEN_HEIGHT // 1.7)
PLAYER2_INIT_POSITION = (round(SCREEN_WIDTH * 0.9), SCREEN_HEIGHT // 2.3)

HP = 3
SPEED = 2
FPS = 60

MOVES_INPUT = [[0, -1], [1, 0], [0, 1], [-1, 0]]
PLAYER1_INPUT = (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE)
PLAYER2_INPUT = (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_KP_ENTER)

clock = pygame.time.Clock()

pygame.init()
fontUI = pygame.font.Font(None, 30)
image_brick = pygame.image.load("images/block_brick.png")
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
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)


class UI:
    def __init__(self):
        pass

    def update(self):
        pass

    def draw(self):
        i = 0
        for obj in objects:
            if obj.type == 'tank':
                pygame.draw.rect(screen, obj.color, (5 + i * 70, 5, 22, 22))

                text = fontUI.render(str(obj.hit_points), 1, obj.color)
                rect = text.get_rect(center=(5 + i * 70 + 32, 5 + 11))
                screen.blit(text, rect)
                i += 1


class Tank:
    def __init__(self, color, obj_coordinates, direct, move_input):
        """Инициализирует базовые атрибуты объекта."""
        objects.append(self)
        self.type = 'tank'
        self.color = color
        self.rank = 0
        self.direct = direct
        self.rect = pygame.Rect(obj_coordinates[0], obj_coordinates[1], GRID_SIZE, GRID_SIZE)
        self.image = pygame.transform.rotate(image_tank[self.rank], -self.direct * 90)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.speed = SPEED
        self.hit_points = HP

        self.move_left = move_input[0]
        self.move_right = move_input[1]
        self.move_up = move_input[2]
        self.move_down = move_input[3]
        self.key_shoot = move_input[4]

        self.shoot_timer = 0
        self.shoot_delay = FPS
        self.bullet_speed = 5
        self.bullet_damage = 1

    def update(self):
        self.image = pygame.transform.rotate(image_tank[self.rank], -self.direct * 90)
        self.image = pygame.transform.scale(self.image, (self.image.get_width() - 5, self.image.get_height() - 5))
        self.rect = self.image.get_rect(center=self.rect.center)

        origin_x, origin_y = self.rect.topleft
        keys = pygame.key.get_pressed()
        if keys[self.move_left]:
            self.rect.x -= self.speed
            self.direct = 3
        elif keys[self.move_right]:
            self.rect.x += self.speed
            self.direct = 1
        elif keys[self.move_up]:
            self.rect.y -= self.speed
            self.direct = 0
        elif keys[self.move_down]:
            self.rect.y += self.speed
            self.direct = 2

        for obj in objects:
            if obj != self and self.rect.colliderect(obj.rect):
                self.rect.topleft = origin_x, origin_y

        if keys[self.key_shoot] and self.shoot_timer == 0:
            bullet_x = MOVES_INPUT[self.direct][0] * self.bullet_speed
            bullet_y = MOVES_INPUT[self.direct][1] * self.bullet_speed
            Bullet(self, self.rect.centerx, self.rect.centery, bullet_x, bullet_y, self.bullet_damage)
            self.shoot_timer = self.shoot_delay

        if self.shoot_timer > 0:
            self.shoot_timer -= 1

    def draw(self):
        """Отрисовывает объект на экране."""
        # pygame.draw.rect(screen, self.color, self.rect)
        #
        # x = self.rect.centerx + MOVES_INPUT[self.direct][0] * 30
        # y = self.rect.centery + MOVES_INPUT[self.direct][1] * 30
        # pygame.draw.line(screen, 'white', self.rect.center, (x, y), 4)
        screen.blit(self.image, self.rect)

    def damage(self, value):
        self.hit_points -= value
        if self.hit_points <= 0:
            objects.remove(self)


class Bullet:
    def __init__(self, parent, parent_x, parent_y, bullet_x, bullet_y, damage):
        bullets.append(self)
        self.parent = parent
        self.parent_x, self.parent_y = parent_x, parent_y
        self.bullet_x, self.bullet_y = bullet_x, bullet_y
        self.damage = damage
        self.hit_points = 1
        self.rect = pygame.Rect(parent_x, parent_y, 10, 10)

    def update(self):
        self.parent_x += self.bullet_x
        self.parent_y += self.bullet_y
        self.rect.x = self.parent_x  # update the rect position too
        self.rect.y = self.parent_y

        to_remove = []

        if not (0 <= self.parent_x <= SCREEN_WIDTH) or not (0 <= self.parent_y <= SCREEN_HEIGHT):
            to_remove.append(self)
        else:
            for obj in objects:
                if obj != self.parent and obj.rect.collidepoint(self.parent_x, self.parent_y):
                    obj.damage(self.damage)
                    to_remove.append(self)
                    break

        for bullet in bullets:
            if bullet != self and self.rect.colliderect(bullet.rect):
                to_remove.append(self)
                to_remove.append(bullet)

        for bullet in to_remove:
            if bullet in bullets:
                bullets.remove(bullet)

    def damage(self, value):
        self.hit_points -= value
        if self.hit_points <= 0:
            objects.remove(self)

    def draw(self):
        pygame.draw.circle(screen, 'yellow', (self.parent_x, self.parent_y), 2)


class Block:
    def __init__(self, obj_coordinates, size):
        objects.append(self)
        self.type = 'block'
        self.rect = pygame.Rect(obj_coordinates[0], obj_coordinates[1], size, size)
        self.hit_points = 1

    def update(self):
        pass

    def damage(self, value):
        self.hit_points -= value
        if self.hit_points <= 0:
            objects.remove(self)

    def draw(self):
        pygame.draw.rect(screen, GREEN_COLOR, self.rect)
        pygame.draw.rect(screen, CYAN_COLOR, self.rect, 2)

    @staticmethod
    def is_colliding(rect, objects):
        for obj in objects:
            if rect.colliderect(obj.rect):
                return True
        return False

    @staticmethod
    def create_if_no_collision(objects, grid_size):
        while True:
            x = randint(0, SCREEN_WIDTH // GRID_SIZE - 1) * GRID_SIZE
            y = randint(0, SCREEN_HEIGHT // GRID_SIZE - 1) * GRID_SIZE
            rect = pygame.Rect(x, y, grid_size, grid_size)
            if not Block.is_colliding(rect, objects):
                return Block((x, y), grid_size)


objects = []
bullets = []
Tank(RED_COLOR, PLAYER1_INIT_POSITION, 0, PLAYER1_INPUT)
Tank(BLUE_COLOR, PLAYER2_INIT_POSITION, 0, PLAYER2_INPUT)
ui = UI()

for _ in range(90):
    block = Block.create_if_no_collision(objects, GRID_SIZE)


def main():
    game_status = True

    while game_status:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        for bullet in bullets:
            bullet.update()

        for obj in objects:
            obj.update()
        ui.update()

        screen.fill(BOARD_BACKGROUND_COLOR)

        for bullet in bullets:
            bullet.draw()

        for obj in objects:
            obj.draw()
        ui.draw()

        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
