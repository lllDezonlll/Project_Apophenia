import sys
import os
import pygame
import csv

# Функция загрузки изображений.
def load_image(path, name, colorkey=None):
    fullname = os.path.join(path, name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    image = image.convert_alpha()

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


def fullname(path, name):
    fullname = os.path.join(path, name)
    if not os.path.isfile(fullname):
        print(f"Файл с именем '{fullname}' не найден")
        sys.exit()
    return fullname

# Функция загрузки карты.
def load_map(filename):
    filename = "data/maps/" + filename

    with open(filename, 'r', encoding='UTF-8') as mapFile:
        reader = csv.reader(mapFile, delimiter=';', quotechar='"')
        tile_map, object_map = [], []

        for row in reader:
            if row == []:
                continue
            tile_map.append([i.split(' ||| ')[0] for i in row])
            object_map.append([i.split(' ||| ')[1] for i in row])

        print(tile_map)

        print(object_map)

    return tile_map, object_map