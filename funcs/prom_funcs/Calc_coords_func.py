from math import floor
import pygame
from Constant_files.CONSTANTS import BOARD_LEFT, BOARD_TOP, CELL_SIZE, SIZE


def find_coords_on_board(x, y):
    x = floor((x * 1920 / SIZE[0] - BOARD_LEFT) / CELL_SIZE)
    y = floor((y * 1080 / SIZE[1] - BOARD_TOP) / CELL_SIZE)
    return [x, y]

def find_coords_for_laser(x, y):
    x = floor((x - BOARD_LEFT) / CELL_SIZE)
    y = floor((y - BOARD_TOP) / CELL_SIZE)
    return [x, y]

def get_mouse_pos():
    pos = pygame.mouse.get_pos()
    return pos[0] / SIZE[0] * 1920, pos[1] / SIZE[1] * 1080

def get_fixed_pos(x, y):
    return x * 1920 / SIZE[0], y * 1080 / SIZE[1]