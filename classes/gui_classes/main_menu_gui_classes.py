import pygame
from Constant_files.SPRITE_GROUPS import main_menu_sprite_group
from classes.gui_classes.gui_classes import Button, Parallax_Image
from funcs.prom_funcs.Load_func import load_image

play_button = Button(1400, 400, 1, [main_menu_sprite_group])
escape_button = Button(1400, 600, 1, [main_menu_sprite_group])

main_menu_eye = Parallax_Image(806, 428, load_image('data/images', 'main_menu_eye.png'), (6, 8), (150, 108))
main_menu_cracks_main_mirror = Parallax_Image(750, 172, load_image('data/images', 'main_menu_cracks_main_mirror.png'), (0, 0), (0, 0))
menu_mirror_fone = Parallax_Image(758, 180, pygame.transform.scale2x(load_image('data/images', 'menu_mirror_fone.png')), (0, 0), (0, 0))
menu_background = Parallax_Image(0, 0, load_image('data/images', 'menu_background.png'), (0, 0), (0, 0))
title = Parallax_Image(550, 42, load_image('data/images', 'Title.png'), (-0.5, -0.5), (960, 540))

shards_2_1 = Parallax_Image(1200, -100, load_image('data/images', 'Shards_2_1.png'), (-10, 30), (160, 140))
shards_2_2 = Parallax_Image(100, -50, load_image('data/images', 'Shards_2_2.png'), (10, 30), (1860, 140))

shards_4_1 = Parallax_Image(500, 0, load_image('data/images', 'Shards_4_1.png'), (3, -5), (960, 140))
shards_4_2 = Parallax_Image(10, 0, load_image('data/images', 'Shards_4_2.png'), (-3, 5), (960, 840))
shards_4_3 = Parallax_Image(1200, 0, load_image('data/images', 'Shards_4_3.png'), (5, -7), (960, 840))
shards_4_4 = Parallax_Image(1400, 80, load_image('data/images', 'Shards_4_4.png'), (-5, 7), (960, 140))