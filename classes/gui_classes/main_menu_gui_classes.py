import pygame
from Constant_files.SPRITE_GROUPS import main_menu_sprite_group
from classes.gui_classes.gui_classes import Button


play_button = Button(200, 400, 1, [main_menu_sprite_group])
escape_button = Button(200, 600, 1, [main_menu_sprite_group])