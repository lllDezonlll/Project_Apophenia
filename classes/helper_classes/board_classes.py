from classes.object_classes.tile_classes import Default_Tile, Void_Tile
from classes.object_classes.mirror_classes import Mirror
from classes.object_classes.wall_classes import Wall
from Constant_files.SPRITE_GROUPS import enemy_sprite_group, game_sprite_group
from Constant_files.CONSTANTS import BOARD_LEFT, BOARD_TOP, CELL_SIZE, CELL_COUNT
from funcs.prom_funcs.Load_func import load_map

from classes.object_classes.enemy_classes import Enemy, Enemy_Shooter, Enemy_Ghost, Enemy_Tomb_Wrecker

from random import choice, randrange

import pygame


# Базовый и удобный класс доски.
class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [['?'] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for i in range(self.width):
            for j in range(self.height):
                width = 1
                if self.board[j][i] == 1:
                    width = 0
                pygame.draw.rect(screen, (255, 255, 255), (i * self.cell_size + self.left,
                                                           j * self.cell_size + self.top,
                                                           self.cell_size, self.cell_size), width=width)

    def print_objects(self):
        print(type(self))
        print(self.board)


# Класс доски тайлов.
class Tiles_Board(Board):
    def __init__(self, width, height):
        super().__init__(width, height)

    # Заполнение доски тайлами из мапфайла.
    def fill_board(self, current_map):
        for y in range(len(current_map)):
            for x in range(len(current_map[y])):
                current_data = current_map[y][x]
                if current_data == 'Default_Tile':
                    self.board[y][x] = Default_Tile(x, y, self)
                elif current_data == 'void_tile':
                    self.board[y][x] = Void_Tile(x, y, self)

    def add_tile(self, tile, del_previous=False):
        if del_previous:
            self.del_tile(tile)
        self.board[tile.y][tile.x] = tile

    def del_tile(self, tile):
        try:
            self.board[tile.y][tile.x].kill_self()
        except Exception:
            pass


# Класс доски объектов.
class Game_Objects_Board(Board):
    def __init__(self, width, height):
        super().__init__(width, height)

    # Заполнение доски объектами из мапфайла.
    def fill_board(self, current_map):
        for y in range(len(current_map)):
            for x in range(len(current_map[y])):
                current_data = current_map[y][x]
                if 'mirror' in current_data:
                    self.board[y][x] = Mirror(x, y, int(current_data[-3::]), self)
                elif current_data == 'Wall':
                    self.board[y][x] = Wall(x, y, self)
                elif current_data == 'enemy':
                    self.board[y][x] = Enemy(x, y, self, tiles_board, 0)
                elif current_data == 'shooter':
                    self.board[y][x] = Enemy_Shooter(x, y, self, tiles_board, 0)
                elif current_data == 'tomb_wrecker':
                    self.board[y][x] = Enemy_Tomb_Wrecker(x, y, self, tiles_board, 0)
                elif current_data == 'ghost':
                    self.board[y][x] = Enemy_Ghost(x, y, self, tiles_board, 0)
                elif current_data == 'graveter':
                    self.board[y][x] = Graveter(x, y, self, tiles_board, 0)
                """elif current_data == 'big_boneser':
                    self.board[y][x] = Big_boneser(x, y, self, tiles_board, 0)"""

    def add_object(self, object, del_previous=False):
        try:
            if del_previous:
                self.del_object(self.board[object.y][object.x])
            self.board[object.y][object.x] = object

            for sprite in enemy_sprite_group.sprites().copy():
                sprite.next_move_calculated()

        except Exception:
            pass

    def del_object(self, object, kill_object=False):
        try:
            self.board[object.y][object.x] = '?'
            for sprite in enemy_sprite_group.sprites().copy():
                sprite.next_move_calculated()
            if kill_object:
                object.kill_self()
        except AttributeError:
            pass



tile_map, object_map = load_map('test.csv')  # Загрузка карты.

# Создание доски тайлов.
tiles_board = Tiles_Board(CELL_COUNT, CELL_COUNT)
tiles_board.set_view(BOARD_LEFT, BOARD_TOP, CELL_SIZE)
tiles_board.fill_board(tile_map)
tiles_board.print_objects()

# Создание доски объектов.
game_objects_board = Game_Objects_Board(CELL_COUNT, CELL_COUNT)
game_objects_board.set_view(BOARD_LEFT, BOARD_TOP, CELL_SIZE)
game_objects_board.fill_board(object_map)
game_objects_board.print_objects()
