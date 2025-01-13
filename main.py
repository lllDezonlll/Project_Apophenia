import sys
from Constant_files.CONSTANTS import SIZE, FPS
from funcs.prom_func.Load_func import load_map
from classes.board_classes import *
from classes.laser_class import *
from classes.description_classes import *


def terminate():
    pygame.quit()
    sys.exit()


pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(SIZE)

if __name__ == '__main__':
    pygame.init()
    map = load_map('map.txt')
    tiles_board = Tiles_Board(CELL_COUNT, CELL_COUNT)
    tiles_board.set_view(BOARD_LEFT, BOARD_TOP, CELL_SIZE)
    tiles_board.fill_board(map)
    tiles_board.print_objects()

    game_objects_board = Game_Objects_Board(CELL_COUNT, CELL_COUNT)
    game_objects_board.set_view(BOARD_LEFT, BOARD_TOP, CELL_SIZE)
    game_objects_board.fill_board(map)
    game_objects_board.print_objects()

    while True:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            if event.type == pygame.KEYDOWN:
                x, y = pygame.mouse.get_pos()
                if event.key == pygame.K_s:
                    Laser(x, y, 'down')
                if event.key == pygame.K_w:
                    Laser(x, y, 'up')
                if event.key == pygame.K_a:
                    Laser(x, y, 'left')
                if event.key == pygame.K_d:
                    Laser(x, y, 'right')

        all_sprite_group.update()

        tiles_sprite_group.draw(screen)
        mirror_sprite_group.draw(screen)
        laser_sprite_group.draw(screen)
        description_sprite_group.draw(screen)

        clock.tick(FPS)

        pygame.display.flip()
