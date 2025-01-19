from classes.object_classes.tile_classes import Default_Tile, Void_Tile, Wall_Tile
from classes.object_classes.mirror_classes import Mirror
from Constant_files.CONSTANTS import BOARD_LEFT, BOARD_TOP, CELL_SIZE, CELL_COUNT
from funcs.prom_funcs.Load_func import load_map
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
        print(self.board)


# Класс доски тайлов.
class Tiles_Board(Board):
    def __init__(self, width, height):
        super().__init__(width, height)

    # Заполнение доски тайлами из мапфайла.
    def fill_board(self, current_map):
        for y in range(len(current_map)):
            for x in range(len(current_map[y])):
                current_data = current_map[y][x][0]
                if current_data == 'empty_tile':
                    self.board[y][x] = Default_Tile(x, y, self)
                elif current_data == 'void_tile':
                    self.board[y][x] = Void_Tile(x, y, self)
                elif current_data == 'wall_tile':
                    self.board[y][x] = Wall_Tile(x, y, self)

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
                current_data = current_map[y][x][1]
                if 'mirror' in current_data:
                    self.board[y][x] = Mirror(x, y, int(current_data[-3::]), self)

    def add_object(self, object, del_previous=False):
        if del_previous:
            self.del_object(object)
        self.board[object.y][object.x] = object

    def del_object(self, object):
        try:
            self.board[object.y][object.x].kill_self()
        except Exception:
            pass


map = load_map('map.txt')  # Загрузка карты.

# Создание доски тайлов.
tiles_board = Tiles_Board(CELL_COUNT, CELL_COUNT)
tiles_board.set_view(BOARD_LEFT, BOARD_TOP, CELL_SIZE)
tiles_board.fill_board(map)
tiles_board.print_objects()

# Создание доски объектов.
game_objects_board = Game_Objects_Board(CELL_COUNT, CELL_COUNT)
game_objects_board.set_view(BOARD_LEFT, BOARD_TOP, CELL_SIZE)
game_objects_board.fill_board(map)
game_objects_board.print_objects()