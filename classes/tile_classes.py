import pygame
from Constant_files.CONSTANTS import BOARD_LEFT, BOARD_TOP, CELL_SIZE
from Constant_files.SPRITE_GROUPS import all_sprite_group, tiles_sprite_group
from classes.hitbox_classes import Hitbox
from Constant_files.CONSTANT_OBJECTS import tile_description


# Обычный тайл, не имеющий никаких эффектов.
class Default_Tile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprite_group, tiles_sprite_group)
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, pygame.Color((210, 247, 217)), (0, 0, CELL_SIZE, CELL_SIZE))
        self.rect = pygame.Rect(BOARD_LEFT + x * CELL_SIZE, BOARD_TOP + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        self.hitbox = Hitbox(self)

    # Отображает своё описание в специальном информационном поле, при получении сигнала от своего хитбокса.
    def display_self_description(self):
        tile_description.set_trackable_tile(self)


# Пустой тайл. Просто клетка, на которой ничего нельзя расположить.
class Void_Tile(Default_Tile):
    def __init__(self, x, y):
        super().__init__(x, y)
        pygame.draw.rect(self.image, pygame.Color((0, 0, 0)), (0, 0, CELL_SIZE, CELL_SIZE))
