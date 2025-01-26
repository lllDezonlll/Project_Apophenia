import pygame
from Constant_files.SPRITE_GROUPS import main_menu_sprite_group
from classes.gui_classes.gui_classes import Button, Parallax_Image
from funcs.prom_funcs.Load_func import load_image

play_button = Button(200, 400, 1, [main_menu_sprite_group])
escape_button = Button(200, 600, 1, [main_menu_sprite_group])

main_menu_eye = Parallax_Image(806, 428, load_image('data/images', 'main_menu_eye.png'), (6, 8), (150, 108))
main_menu_cracks_main_mirror = Parallax_Image(750, 172, load_image('data/images', 'main_menu_cracks_main_mirror.png'), (0, 0), (0, 0))