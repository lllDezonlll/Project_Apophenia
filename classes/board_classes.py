from classes.tile_classes import Default_Tile, Void_Tile
from classes.mirror_classes import Mirror


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
                    self.board[y][x] = Default_Tile(x, y)
                elif current_data == 'void_tile':
                    self.board[y][x] = Void_Tile(x, y)


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
                    self.board[y][x] = Mirror(x, y, int(current_data[-3::]))
