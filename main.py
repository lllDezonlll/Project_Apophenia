import sys

import pygame.display

from Constant_files.CONSTANTS import *
from Constant_files.SPRITE_GROUPS import *
from Constant_files.CONSTANT_OBJECTS import screen, clock

from classes.helper_classes.board_classes import tiles_board, game_objects_board
from classes.helper_classes.deck_and_cards_classes import deck_active, deck_hand, deck_discard, energy
from classes.helper_classes.object_deck_classes import object_manager

from classes.object_classes.laser_class import Laser
from classes.object_classes.enemy_classes import Enemy
from classes.object_classes.mirror_classes import Mirror
from classes.object_classes.tile_classes import Default_Tile, Void_Tile
from classes.object_classes.wall_classes import Wall
from classes.object_classes.base_class import base

from classes.gui_classes.gui_classes import Button
from classes.gui_classes.main_menu_gui_classes import play_button, escape_button, main_menu_eye
from classes.gui_classes.pause_menu_gui_classes import pause_play_button, pause_escape_button

from funcs.prom_funcs.Calc_coords_func import find_coords_on_board


def terminate():    # Закончить работу программы.
    pygame.quit()
    sys.exit()


def main_menu():
    if __name__ == '__main__':
        pygame.init()
        pygame.mouse.set_visible(False)
        running = True

        while running:
            screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()

            if escape_button.update():
                terminate()

            running = not play_button.update()

            cursor_sprite_group.update(1)
            texture_cursor_sprite_group.update(1)
            parallax_image_sprite_group.update(1)

            main_menu_sprite_group.draw(screen)

            pygame.draw.rect(screen, (53, 51, 86), (752, 178, 410, 752))
            parallax_image_sprite_group.draw(screen)

            cursor_sprite_group.draw(screen)
            texture_cursor_sprite_group.draw(screen)

            pygame.display.flip()

        game()


def game():
    if __name__ == '__main__':
        pause = False
        running = True
        return_to_main_menu = False
        next_turn_init = True
        current_turn = 'Player'

        while running:  # Основной игровой цикл.
            screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Закончить программу если игрок нажал на крестик.
                    terminate()

                if event.type == pygame.KEYDOWN:  # Выпустить лазер, нажимая wasd, в соответствующие стороны из позиции курсора.
                    x, y = find_coords_on_board(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                    laser_x, laser_y = pygame.mouse.get_pos()
                    if event.key == pygame.K_ESCAPE:
                        pause = not pause
                    if event.key == pygame.K_SPACE:
                        base.active_cannon.fire_laser(damage=10)
                    if event.key == pygame.K_c:
                        deck_active.draw_card()
                    if event.key == pygame.K_s:
                        Laser(laser_x, laser_y, 90)
                    if event.key == pygame.K_w:
                        Laser(laser_x, laser_y, -90)
                    if event.key == pygame.K_a:
                        Laser(laser_x, laser_y, 180)
                    if event.key == pygame.K_d:
                        Laser(laser_x, laser_y, 0)
                    if event.key == pygame.K_r:
                        object_manager.rotate_objects('left')
                    if event.key == pygame.K_t:
                        object_manager.rotate_objects('right')
                    if event.key == pygame.K_1:
                        Mirror(x, y, 0, game_objects_board)
                    if event.key == pygame.K_2:
                        Mirror(x, y, 90, game_objects_board)
                    if event.key == pygame.K_3:
                        Mirror(x, y, 180, game_objects_board)
                    if event.key == pygame.K_4:
                        Mirror(x, y, -90, game_objects_board)
                    if event.key == pygame.K_q:
                        tiles_board.add_tile(Default_Tile(x, y, tiles_board), del_previous=True)
                        game_objects_board.del_object(game_objects_board.board[y][x])
                    if event.key == pygame.K_e:
                        tiles_board.add_tile(Wall(x, y, game_objects_board), del_previous=True)

            if pause:
                result = pause_menu(current_turn)
                pause, return_to_main_menu = not result[0], result[1]
                print(1)
            else:
                if end_turn_button.update():
                    current_turn = 'Enemy'
                    next_turn_init = True

                if current_turn == 'Enemy':
                    for sprite in enemy_sprite_group.sprites().copy():
                        sprite.do_action()
                        sprite.next_move_calculated()

                    game_objects_board.print_objects()

                game_sprite_group.update(current_turn)  # Обновление всех спрайтов.

            if return_to_main_menu:
                running = False

            if next_turn_init:
                for card in deck_hand.cards.copy():
                    deck_hand.discard_card(card)
                deck_active.draw_card(5)
                energy.return_to_default_count()
                next_turn_init = False



            # Отрисовка спрайтов в правильном порядке.
            tiles_sprite_group.draw(screen)

            base_sprite_group.draw(screen)

            mirror_sprite_group.draw(screen)
            texture_mirror_sprite_group.draw(screen)

            wall_sprite_group.draw(screen)

            texture_enemy_sprite_group.draw(screen)

            laser_sprite_group.draw(screen)
            texture_laser_sprite_group.draw(screen)

            cannon_sprite_group.draw(screen)

            description_sprite_group.draw(screen)

            energy_sprite_group.draw(screen)

            card_sprite_group.draw(screen)

            object_manager_sprite_group.draw(screen)
            any_texture_sprite_group.draw(screen)

            if pause:
                pause_menu_sprite_group.draw(screen)

            # tiles_board.render(screen)
            cursor_sprite_group.draw(screen)
            texture_cursor_sprite_group.draw(screen)

            # Тик у таймера от фпс.
            clock.tick(FPS)

            # Обновление кадра.
            pygame.display.flip()

            current_turn = 'Player'

        else:
            main_menu()


def pause_menu(event):
    cursor_sprite_group.update(event)
    texture_cursor_sprite_group.update(event)

    return_to_main_menu = pause_escape_button.update()

    return pause_play_button.update(), return_to_main_menu


enemy1 = Enemy(5, 10, game_objects_board, tiles_board)
enemy2 = Enemy(16, 16, game_objects_board, tiles_board)
enemy3 = Enemy(4, 16, game_objects_board, tiles_board)
end_turn_button = Button(1500, 950, 1, [any_texture_sprite_group])

main_menu()