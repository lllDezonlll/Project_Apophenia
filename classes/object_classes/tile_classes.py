import pygame
from Constant_files.CONSTANTS import BOARD_LEFT, BOARD_TOP, CELL_SIZE
from Constant_files.SPRITE_GROUPS import game_sprite_group, tiles_sprite_group, laser_sprite_group
from classes.helper_classes.hitbox_classes import Hitbox
from Constant_files.CONSTANT_OBJECTS import tile_description
from funcs.prom_funcs.Load_func import load_image
from random import choice, randrange


# Обычный тайл, не имеющий никаких эффектов.
class Default_Tile(pygame.sprite.Sprite):
    image_1 = load_image('data/textures', 'grass_tile_1.png')
    image_2 = load_image('data/textures', 'grass_tile_2.png')
    image_3 = load_image('data/textures', 'grass_tile_3.png')
    image_4 = load_image('data/textures', 'grass_tile_4.png')

    images = [image_1, image_2, image_3, image_4]

    def __init__(self, x, y, board):
        self.x, self.y, self.board = x, y, board
        self.value = 0
        super().__init__(game_sprite_group, tiles_sprite_group)
        self.image = pygame.transform.rotate(choice(Default_Tile.images), 180 * randrange(0, 2))
        self.rect = pygame.Rect(BOARD_LEFT + x * CELL_SIZE, BOARD_TOP + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        self.hitbox = Hitbox(self)

    # Отображает своё описание в специальном информационном поле, при получении сигнала от своего хитбокса.
    def display_self_description(self):
        tile_description.set_trackable_tile(self)

    def kill_self(self):
        self.kill()

    def update(self, event):
        pass


# Пустой тайл. Просто клетка, на которой ничего нельзя расположить.
class Void_Tile(Default_Tile):
    def __init__(self, x, y, board):
        super().__init__(x, y, board)
        pygame.draw.rect(self.image, pygame.Color((0, 0, 0)), (0, 0, CELL_SIZE, CELL_SIZE))


