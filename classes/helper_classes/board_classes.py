from classes.object_classes.tile_classes import Default_Tile, Void_Tile
from classes.object_classes.mirror_classes import Mirror
from classes.object_classes.wall_classes import Wall
from Constant_files.SPRITE_GROUPS import enemy_sprite_group, game_sprite_group
from Constant_files.CONSTANTS import BOARD_LEFT, BOARD_TOP, CELL_SIZE, CELL_COUNT
from funcs.prom_funcs.Load_func import load_map

from classes.object_classes.enemy_classes import Enemy, Enemy_Shooter

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
                current_data = current_map[y][x][0]
                if current_data == 'empty_tile':
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
                current_data = current_map[y][x][1]
                if 'mirror' in current_data:
                    self.board[y][x] = Mirror(x, y, int(current_data[-3::]), self)
                elif current_data == 'wall':
                    self.board[y][x] = Wall(x, y, self)

    def add_object(self, object, del_previous=False):
        try:
            if del_previous:
                self.del_object(self.board[object.y][object.x])
            self.board[object.y][object.x] = object
            spawner.targeted_cells = {}
            spawner.calculate_spawn()

            for sprite in enemy_sprite_group.sprites().copy():
                sprite.next_move_calculated()

        except Exception:
            pass

    def del_object(self, object, kill_object=False):
        try:
            self.board[object.y][object.x] = '?'
            spawner.targeted_cells = {}
            spawner.calculate_spawn()
            for sprite in enemy_sprite_group.sprites().copy():
                sprite.next_move_calculated()
            if kill_object:
                object.kill_self()
        except AttributeError:
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


class Spawner(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(game_sprite_group)
        self.targeted_cells = {}
        self.points = 6
        self.current_points = self.points
        self.enemy_list = [Enemy]

    def get_empty_cells(self):
        result = []
        for y in range(19):
            for x in range(19):
                if game_objects_board.board[y][x] == '?':
                    result.append((x, y))
        return result

    def update(self, event):
        pass

    def calculate_spawn(self):
        self.targeted_cells = {}
        empty_cells = self.get_empty_cells()
        if len(empty_cells) == 0:
            return

        self.current_points = self.points
        if self.current_points == 0:
            return
        while any([self.current_points >= enemy.cost for enemy in self.enemy_list]):

            if len(self.targeted_cells.keys()) > 6:
                break
            self.current_enemy = choice(self.enemy_list)
            while self.current_enemy.cost > self.current_points:
                self.current_enemy = choice(self.enemy_list)

            while True:
                current_cell = choice(empty_cells)
                if current_cell[0] in range(8, 11) and current_cell[1] in range(8, 11):
                    continue
                if current_cell not in self.targeted_cells.keys():
                    self.targeted_cells[current_cell] = self.current_enemy
                    break
            self.current_points -= self.current_enemy.cost



    def spawn_enemies(self):
        spawn_cells = self.targeted_cells.copy()
        print(spawn_cells, self.points)
        self.points += randrange(1, 4)
        if not enemy_sprite_group.sprites() == []:
            if randrange(0, 4) == 0 and not enemy_sprite_group.sprites() == []:
                return
        if self.targeted_cells == {}:
            return
        for position in spawn_cells:
            spawn_cells[position](position[0], position[1], game_objects_board, tiles_board)
        self.points = 6
        self.targeted_cells = {}
        print(self.targeted_cells)


spawner = Spawner()
