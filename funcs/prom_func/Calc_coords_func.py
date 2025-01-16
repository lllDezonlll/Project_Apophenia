from math import ceil
from Constant_files.CONSTANTS import BOARD_LEFT, BOARD_TOP, CELL_SIZE


def find_coords_on_board(x, y):
    x = ceil((x - BOARD_LEFT) / CELL_SIZE) - 1
    y = ceil((y - BOARD_TOP) / CELL_SIZE) - 1
    return [x, y]
