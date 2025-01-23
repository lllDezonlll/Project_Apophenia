import pygame

from Constant_files.SPRITE_GROUPS import all_sprite_group, laser_sprite_group, mirror_sprite_group, texture_laser_sprite_group
from Constant_files.CONSTANTS import BOARD_LEFT, BOARD_TOP, CELL_SIZE, CELL_COUNT, FPS
from classes.gui_classes.gui_classes import Following_Texture
from funcs.prom_funcs.Load_func import load_image
from funcs.prom_funcs.Calc_coords_func import find_coords_on_board


# Класс атаки лазером.
class Laser(pygame.sprite.Sprite):
    image = load_image('data/textures', 'laser_test.png')

    def __init__(self, x, y, orientation, speed=900 / FPS, damage=1):
        super().__init__(all_sprite_group, laser_sprite_group)
        self.x, self.y = find_coords_on_board(x, y)
        self.mirror = None
        self.orientation = orientation  # Направление лазера (0, 90, 180, -90)
        self.speed = speed  # Скорость лазера
        self.damage = damage  # Урон от лазера
        self.image = pygame.Surface((8 * CELL_SIZE / 40, 8 * CELL_SIZE / 40), pygame.SRCALPHA, 32)  # Хитбокс для физики лазера.
        self.image.fill(pygame.Color('red'))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.texture = Following_Texture(self, Laser.image, [all_sprite_group, texture_laser_sprite_group],
                                         rotatable=True, offset_x=-36, offset_y=-20)

    # Движение лазера.
    def move(self):
        if self.orientation == -90:
            self.rect = self.rect.move(0, -self.speed)  # Подобные строчки отвечают за само движение лазера.
            self.rect.x = find_coords_on_board(self.rect.x, self.rect.y)[0] * CELL_SIZE + CELL_SIZE / 2 + BOARD_LEFT - self.rect.w / 2 # Подобные строчки отвечают за выравнивание лазера по сетке.
        elif self.orientation == 90:
            self.rect = self.rect.move(0, self.speed)
            self.rect.x = find_coords_on_board(self.rect.x, self.rect.y)[0] * CELL_SIZE + CELL_SIZE / 2 + BOARD_LEFT - self.rect.w / 2
        elif self.orientation == 180:
            self.rect = self.rect.move(-self.speed, 0)
            self.rect.y = find_coords_on_board(self.rect.x, self.rect.y)[1] * CELL_SIZE + CELL_SIZE / 2 + BOARD_TOP - self.rect.w / 2
        elif self.orientation == 0:
            self.rect = self.rect.move(self.speed, 0)
            self.rect.y = find_coords_on_board(self.rect.x, self.rect.y)[1] * CELL_SIZE + CELL_SIZE / 2 + BOARD_TOP - self.rect.w / 2

    # Удаление себя и своей текстуры.
    def kill_self(self):
        self.texture.kill()
        self.kill()

    def update(self, event):
        # Вызов метода kill_self при условии, что лазера за пределами игрового поля.
        if (self.rect.x < BOARD_LEFT or self.rect.y < BOARD_TOP or
                self.rect.x > BOARD_LEFT + CELL_SIZE * CELL_COUNT or self.rect.y > BOARD_TOP + CELL_SIZE * CELL_COUNT):
            self.kill_self()

        # Проверка на наличие касания отражающих объектов.
        for mirror in mirror_sprite_group:
            if pygame.sprite.collide_mask(self, mirror):
                if self.mirror != mirror:   # Нужно для того, чтобы лазер не вызывал реакцию отражающего объекта несколько раз.
                    self.mirror = mirror
                    self.mirror.reflect_laser(self)     # Отражение лазера по правилам найденного отражающего объекта.
        self.move()     # Вызов движения лазера.
