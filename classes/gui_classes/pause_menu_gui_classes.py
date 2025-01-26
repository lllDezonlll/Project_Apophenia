import pygame
from Constant_files.SPRITE_GROUPS import pause_menu_sprite_group
from classes.gui_classes.gui_classes import Button



pause_play_button = Button(800, 400, 1, [pause_menu_sprite_group])
pause_escape_button = Button(800, 520, 1, [pause_menu_sprite_group])