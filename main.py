import sys

import pygame

BOARD_BACKGROUND_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)
RED_COLOR = (255, 0, 0)
BLUE_COLOR = (0, 0, 255)
CYAN_COLOR = (93, 216, 228)
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
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)


class Tank:
    def __init__(self, color, obj_coordinates, direct, move_input):
        """Инициализирует базовые атрибуты объекта."""
        objects.append(self)
        self.type = 'tank'
        self.color = color
        self.rect = pygame.Rect(obj_coordinates[0], obj_coordinates[1], GRID_SIZE, GRID_SIZE)
        self.direct = direct
        self.speed = SPEED
        self.hit_point = HP

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

        if keys[self.key_shoot] and self.shoot_timer == 0:
            bullet_x = MOVES_INPUT[self.direct][0] * self.bullet_speed
            bullet_y = MOVES_INPUT[self.direct][1] * self.bullet_speed
            Bullet(self, self.rect.centerx, self.rect.centery, bullet_x, bullet_y, self.bullet_damage)
            self.shoot_timer = self.shoot_delay

        if self.shoot_timer > 0:
            self.shoot_timer -= 1

    def draw(self):
        """Отрисовывает объект на экране."""
        pygame.draw.rect(screen, self.color, self.rect)

        x = self.rect.centerx + MOVES_INPUT[self.direct][0] * 30
        y = self.rect.centery + MOVES_INPUT[self.direct][1] * 30
        pygame.draw.line(screen, 'white', self.rect.center, (x, y), 4)

    def damage(self, value):
        self.hit_point -= value
        if self.hit_point <= 0:
            objects.remove(self)


class Bullet:
    def __init__(self, parent, parent_x, parent_y, bullet_x, bullet_y, damage):
        bullets.append(self)
        self.parent = parent
        self.parent_x, self.parent_y = parent_x, parent_y
        self.bullet_x, self.bullet_y = bullet_x, bullet_y
        self.damage = damage

    def update(self):
        self.parent_x += self.bullet_x
        self.parent_y += self.bullet_y

        if self.parent_x < 0 or self.parent_x > SCREEN_WIDTH or self.parent_y < 0 or self.parent_y > SCREEN_HEIGHT:
            bullets.remove(self)
        else:
            for obj in objects:
                if obj != self.parent and obj.rect.collidepoint(self.parent_x, self.parent_y):
                    obj.damage(self.damage)
                    bullets.remove(self)
                    break

    def draw(self):
        pygame.draw.circle(screen, 'yellow', (self.parent_x, self.parent_y), 2)


objects = []
bullets = []
Tank(RED_COLOR, PLAYER1_INIT_POSITION, 0, PLAYER1_INPUT)
Tank(BLUE_COLOR, PLAYER2_INIT_POSITION, 0, PLAYER2_INPUT)


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

        screen.fill(BOARD_BACKGROUND_COLOR)

        for bullet in bullets:
            bullet.draw()

        for obj in objects:
            obj.draw()

        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
