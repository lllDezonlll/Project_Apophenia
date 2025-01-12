import sys
import os
import pygame


def load_image(name, colorkey=None):
    fullname = os.path.join('../../data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_map(filename):
    filename = "data/maps/" + filename

    with open(filename, 'r') as mapFile:
        level_map = [[i.split('|') for i in line.strip().split()] for line in mapFile][:-1:]

    print(level_map)

    return level_map