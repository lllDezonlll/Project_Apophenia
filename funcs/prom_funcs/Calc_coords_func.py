from math import floor
from Constant_files.CONSTANTS import BOARD_LEFT, BOARD_TOP, CELL_SIZE


def find_coords_on_board(x, y):
    x = floor((x - BOARD_LEFT) / CELL_SIZE)
    y = floor((y - BOARD_TOP) / CELL_SIZE)
    return [x, y]
