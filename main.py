import sys

from Constant_files.CONSTANTS import *
from Constant_files.SPRITE_GROUPS import *
from Constant_files.CONSTANT_OBJECTS import screen, clock

from classes.helper_classes.board_classes import tiles_board, game_objects_board
from classes.object_classes.laser_class import Laser
from classes.object_classes.enemy_classes import Enemy
from classes.object_classes.mirror_classes import Mirror
from classes.object_classes.tile_classes import Wall_Tile, Default_Tile, Void_Tile
from funcs.prom_func.Calc_coords_func import find_coords_on_board


def terminate():    # Закончить работу программы.
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    pygame.init()
    pygame.mouse.set_visible(False)  # Удаление видимости системного курсора.
    enemy = Enemy(5, 10, game_objects_board, tiles_board)

    while True:  # Основной игровой цикл.
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Закончить программу если игрок нажал на крестик.
                terminate()

            if event.type == pygame.KEYDOWN:  # Выпустить лазер, нажимая wasd, в соответствующие стороны из позиции курсора.
                x, y = find_coords_on_board(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                laser_x, laser_y = pygame.mouse.get_pos()
                if event.key == pygame.K_s:
                    Laser(laser_x, laser_y, 90)
                if event.key == pygame.K_w:
                    Laser(laser_x, laser_y, -90)
                if event.key == pygame.K_a:
                    Laser(laser_x, laser_y, 180)
                if event.key == pygame.K_d:
                    Laser(laser_x, laser_y, 0)
                if event.key == pygame.K_f:
                    enemy.move()
                if event.key == pygame.K_1:
                    game_objects_board.add_object(Mirror(x, y, 0, game_objects_board), del_previous=True)
                if event.key == pygame.K_2:
                    game_objects_board.add_object(Mirror(x, y, 90, game_objects_board), del_previous=True)
                if event.key == pygame.K_3:
                    game_objects_board.add_object(Mirror(x, y, 180, game_objects_board), del_previous=True)
                if event.key == pygame.K_4:
                    game_objects_board.add_object(Mirror(x, y, -90, game_objects_board), del_previous=True)
                if event.key == pygame.K_q:
                    tiles_board.add_tile(Default_Tile(x, y, tiles_board), del_previous=True)
                    game_objects_board.del_object(game_objects_board.board[y][x])
                if event.key == pygame.K_e:
                    tiles_board.add_tile(Wall_Tile(x, y, tiles_board), del_previous=True)
                    print(game_objects_board.board[y][x])
                    game_objects_board.del_object(game_objects_board.board[y][x])

        all_sprite_group.update()  # Обновление всех спрайтов.

        # Отрисовка спрайтов в правильном порядке.
        tiles_sprite_group.draw(screen)
        mirror_sprite_group.draw(screen)
        texture_mirror_sprite_group.draw(screen)
        texture_enemy_sprite_group.draw(screen)
        laser_sprite_group.draw(screen)
        texture_laser_sprite_group.draw(screen)
        description_sprite_group.draw(screen)
        # tiles_board.render(screen)
        cursor_sprite_group.draw(screen)

        # Тик у таймера от фпс.
        clock.tick(FPS)

        # Обновление кадра.
        pygame.display.flip()
