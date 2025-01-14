import sys
import pygame


from Constant_files.CONSTANTS import *
from Constant_files.SPRITE_GROUPS import *
from Constant_files.CONSTANT_OBJECTS import screen, clock


from funcs.prom_func.Load_func import load_map
from classes.board_classes import Tiles_Board, Game_Objects_Board
from classes.laser_class import Laser


def terminate():    # Закончить работу программы.
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    pygame.init()
    pygame.mouse.set_visible(False)  # Удаление видимости системного курсора.

    map = load_map('map.txt')  # Загрузка карты.

    # Создание доски тайлов.
    tiles_board = Tiles_Board(CELL_COUNT, CELL_COUNT)
    tiles_board.set_view(BOARD_LEFT, BOARD_TOP, CELL_SIZE)
    tiles_board.fill_board(map)
    tiles_board.print_objects()

    # Создание доски объектов.
    game_objects_board = Game_Objects_Board(CELL_COUNT, CELL_COUNT)
    game_objects_board.set_view(BOARD_LEFT, BOARD_TOP, CELL_SIZE)
    game_objects_board.fill_board(map)
    game_objects_board.print_objects()

    while True:  # Основной игровой цикл.
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Закончить программу если игрок нажал на крестик.
                terminate()

            if event.type == pygame.KEYDOWN:  # Выпустить лазер, нажимая wasd, в соответствующие стороны из позиции курсора.
                x, y = pygame.mouse.get_pos()
                if event.key == pygame.K_s:
                    Laser(x, y, 90)
                if event.key == pygame.K_w:
                    Laser(x, y, -90)
                if event.key == pygame.K_a:
                    Laser(x, y, 180)
                if event.key == pygame.K_d:
                    Laser(x, y, 0)

        all_sprite_group.update()  # Обновление всех спрайтов.

        # Отрисовка спрайтов в правильном порядке.
        tiles_sprite_group.draw(screen)
        mirror_sprite_group.draw(screen)
        texture_mirror_sprite_group.draw(screen)
        laser_sprite_group.draw(screen)
        texture_laser_sprite_group.draw(screen)
        description_sprite_group.draw(screen)
        cursor_sprite_group.draw(screen)

        # Тик у таймера от фпс.
        clock.tick(FPS)

        # Обновление кадра.
        pygame.display.flip()
