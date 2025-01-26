import pygame
from funcs.prom_funcs.Calc_coords_func import find_coords_on_board
from Constant_files.SPRITE_GROUPS import game_sprite_group, object_sprite_group, base_sprite_group, laser_sprite_group, cannon_sprite_group
from Constant_files.CONSTANTS import BOARD_LEFT, BOARD_TOP, CELL_SIZE
from classes.helper_classes.hitbox_classes import Hitbox
from classes.gui_classes.description_classes import Base_description
from classes.object_classes.laser_class import Laser
from classes.gui_classes.gui_classes import Following_Texture
from funcs.prom_funcs.Load_func import load_image
from Constant_files.CONSTANTS import BASE_DESCRIPTION_LEFT, BASE_DESCRIPTION_TOP


class Base(pygame.sprite.Sprite):
    def __init__(self, cannons):
        super().__init__(game_sprite_group, base_sprite_group)
        self.x = 8  # Координата X базы на клеточном поле.
        self.y = 8  # Координата Y базы на клеточном поле.

        self.description = Base_description(1, BASE_DESCRIPTION_LEFT, BASE_DESCRIPTION_TOP, 396, 266, self)
        self.cannons = cannons
        self.active_cannon = self.cannons[0]
        self.active_cannon.switch_activity(True)
        self.state = 'normal'
        self.laser = None
        self.health = 100  # Здоровье базы.
        self.width = CELL_SIZE * 3  # Ширина базы.
        self.height = CELL_SIZE * 3  # Высота бызы.
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        self.rect = pygame.Rect(BOARD_LEFT + self.x * CELL_SIZE, BOARD_TOP + self.y * CELL_SIZE, self.width,
                                self.height)  # Прямоугольник для взаимодействия.
        self.image.fill(pygame.Color('blue'))

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.state = 'destroyed'
            self.image.fill((255, 0, 0))  # Изменяем цвет на красный для визуализации разрушенного состояния

    # Восстановление здоровья.
    def heal(self, amount):
        """ Восстановление здоровья зеркала """
        if self.state != 'destroyed':
            self.health += amount
            if self.health > 100:
                self.health = 100

    def update(self, event):
        # Получает урон от лазера и уничтожает его при касании.
        if laser := pygame.sprite.spritecollideany(self, laser_sprite_group):
            if laser != self.laser:
                self.laser = laser
                self.take_damage(laser.damage)
                laser.kill_self()
        if (pygame.mouse.get_pressed()[0] and
            pygame.mouse.get_pos()[0] in range(self.rect.x, self.rect.x + self.rect.w) and
            pygame.mouse.get_pos()[1] in range(self.rect.y, self.rect.y + self.rect.h)):
            self.change_active_cannon(*pygame.mouse.get_pos())

    def change_active_cannon(self, x, y):
        x, y = find_coords_on_board(x, y)
        if (x, y) not in [(9, 8), (9, 10), (8, 9), (10, 9)]:
            return
        for cannon in self.cannons:
            if cannon.x == x and cannon.y == y:
                cannon.switch_activity(True)
                self.active_cannon = cannon
            else:
                cannon.switch_activity(False)


class Cannon(pygame.sprite.Sprite):
    enabled_cannon = load_image('data/textures', 'test_cannon_enabled.png', colorkey=-1)
    disabled_cannon = load_image('data/textures', 'test_cannon_disabled.png', colorkey=-1)

    def __init__(self, x, y, orientation):
        super().__init__(game_sprite_group, cannon_sprite_group)
        self.x = x  # Координата X пушки на клеточном поле.
        self.y = y  # Координата Y пушки на клеточном поле.

        self.orientation = orientation
        self.health = 100
        self.width = CELL_SIZE
        self.height = CELL_SIZE
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        self.rect = pygame.Rect(BOARD_LEFT + self.x * CELL_SIZE, BOARD_TOP + self.y * CELL_SIZE, self.width,
                                self.height)  # Прямоугольник для взаимодействия.

        self.is_active = False

    def switch_activity(self, activity):
        self.is_active = activity

    def fire_laser(self, damage=1):
        x = find_coords_on_board(self.rect.x, self.rect.y)[0] * CELL_SIZE + CELL_SIZE / 2 + BOARD_LEFT - self.rect.w / 2
        y = find_coords_on_board(self.rect.x, self.rect.y)[1] * CELL_SIZE + CELL_SIZE / 2 + BOARD_TOP - self.rect.w / 2
        if self.orientation == 0:
            y += CELL_SIZE / 2 - 4
            x += CELL_SIZE + 3
        if self.orientation == 90:
            y += CELL_SIZE + 3
            x += CELL_SIZE / 4 + 8
        if self.orientation == 180:
            y += CELL_SIZE / 2 - 4
            x -= CELL_SIZE / 2 - 12
        if self.orientation == -90:
            y -= CELL_SIZE / 4
            x += CELL_SIZE / 2 - 4
        Laser(x, y, self.orientation, damage=damage)

    def update(self, event):
        if self.is_active:
            self.image = pygame.transform.rotate(Cannon.enabled_cannon, -self.orientation)
        else:
            self.image = pygame.transform.rotate(Cannon.disabled_cannon, -self.orientation)


base = Base([Cannon(9, 8, -90),
             Cannon(9, 10, 90),
             Cannon(8, 9, 180),
             Cannon(10, 9, 0)])
