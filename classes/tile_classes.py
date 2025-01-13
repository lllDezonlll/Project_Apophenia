import pygame
from Constant_files.CONSTANTS import BOARD_LEFT, BOARD_TOP, CELL_SIZE
from Constant_files.SPRITE_GROUPS import all_sprite_group, tiles_sprite_group
from classes.hitbox_classes import Hitbox
from Constant_files.CONSTANT_OBJECTS import tile_description


class Empty_tile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprite_group, tiles_sprite_group)
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, pygame.Color((247, 243, 195)), (0, 0, CELL_SIZE, CELL_SIZE))
        self.rect = pygame.Rect(BOARD_LEFT + x * CELL_SIZE, BOARD_TOP + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        self.hitbox = Hitbox(self)

    def display_self_description(self):
        tile_description.set_trackable_tile(self)


class Void_tile(Empty_tile):
    def __init__(self, x, y):
        super().__init__(x, y)
        pygame.draw.rect(self.image, pygame.Color((0, 0, 0)), (0, 0, CELL_SIZE, CELL_SIZE))
