import pygame
from classes.gui_classes.description_classes import Tile_description, Object_descriptiom
from Constant_files.CONSTANTS import SIZE

# Настройки по умолчанию и константные объекты, которые создаются всего один раз.

pygame.init()

clock = pygame.time.Clock()  # Основной таймер игры.
screen = pygame.display.set_mode(SIZE)  # Основной экран игры.

# Создание описания полей информации о тайлах и объектах соответственно.
tile_description = Tile_description(1, 28, 28, 196, 266)
object_description = Object_descriptiom(1, 224, 28, 196, 266)