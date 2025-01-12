import pygame
from Constant_files.SPRITE_GROUPS import *


class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, speed=15, damage=100):
        super().__init__(laser_sprite_group)
        self.timer = 0
        self.x = x
        self.y = y
        self.direction = direction  # Направление лазера ('up', 'down', 'left', 'right')
        self.speed = speed  # Скорость лазера
        self.damage = damage  # Урон от лазера
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA, 32)  # Пример изображения лазера
        pygame.draw.circle(self.image, pygame.Color('red'), (5, 5), 10)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def move(self):
        if self.direction == 'up':
            self.rect = self.rect.move(0, -self.speed)
        elif self.direction == 'down':
            self.rect = self.rect.move(0, self.speed)
        elif self.direction == 'left':
            self.rect = self.rect.move(-self.speed, 0)
        elif self.direction == 'right':
            self.rect = self.rect.move(self.speed, 0)

    def update(self):
        self.move()

        for mirror in mirror_sprites_group:
            if pygame.sprite.collide_mask(self, mirror):
                self.mirror = mirror
                self.mirror.reflect_laser(self)

