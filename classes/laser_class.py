from math import ceil

from Constant_files.SPRITE_GROUPS import *
from Constant_files.CONSTANTS import BOARD_LEFT, BOARD_TOP, CELL_SIZE, CELL_COUNT


class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, speed=15, damage=1):
        super().__init__(all_sprite_group, laser_sprite_group)
        self.x = x
        self.y = y
        self.direction = direction  # Направление лазера ('up', 'down', 'left', 'right')
        self.speed = speed  # Скорость лазера
        self.damage = damage  # Урон от лазера
        self.image = pygame.Surface((8, 8), pygame.SRCALPHA, 32)  # Пример изображения лазера
        self.image.fill(pygame.Color('red'))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def move(self):
        if self.direction == 'up':
            self.rect = self.rect.move(0, -self.speed)
            self.rect.x = ceil((self.rect.x - BOARD_LEFT) / CELL_SIZE) * CELL_SIZE - CELL_SIZE / 2 + BOARD_LEFT
        elif self.direction == 'down':
            self.rect = self.rect.move(0, self.speed)
            self.rect.x = ceil((self.rect.x - BOARD_LEFT) / CELL_SIZE) * CELL_SIZE - CELL_SIZE / 2 + BOARD_LEFT
        elif self.direction == 'left':
            self.rect = self.rect.move(-self.speed, 0)
            self.rect.y = ceil((self.rect.y - BOARD_TOP) / CELL_SIZE) * CELL_SIZE - CELL_SIZE / 2 + BOARD_TOP
        elif self.direction == 'right':
            self.rect = self.rect.move(self.speed, 0)
            self.rect.y = ceil((self.rect.y - BOARD_TOP) / CELL_SIZE) * CELL_SIZE - CELL_SIZE / 2 + BOARD_TOP

    def kill_self(self):
        self.kill()

    def update(self):
        self.move()
        if (self.rect.x < BOARD_LEFT or self.rect.y < BOARD_TOP or
            self.rect.x > BOARD_LEFT + CELL_SIZE * CELL_COUNT or self.rect.y > BOARD_TOP + CELL_SIZE * CELL_COUNT):
            self.kill_self()

        for mirror in mirror_sprite_group:
            if pygame.sprite.collide_mask(self, mirror):
                self.mirror = mirror
                self.mirror.reflect_laser(self)
