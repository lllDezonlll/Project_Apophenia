import sys
from Constant_files.CONSTANTS import SIZE, FPS
from funcs.prom_func.Load_func import load_map
from classes.board_classes import *
from classes.laser_class import *


def terminate():
    pygame.quit()
    sys.exit()


pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(SIZE)

if __name__ == '__main__':
    pygame.init()
    map = load_map('map.txt')
    tiles_board = Tiles_Board(19, 19)
    tiles_board.set_view(BOARD_LEFT, BOARD_TOP, CELL_SIZE)
    tiles_board.fill_board(map)
    tiles_board.print_objects()

    game_objects_board = Game_Objects_Board(19, 19)
    game_objects_board.set_view(BOARD_LEFT, BOARD_TOP, CELL_SIZE)
    game_objects_board.fill_board(map)
    game_objects_board.print_objects()

    laser = Laser(510, 10, 'down')

    while True:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

        laser.update()

        tile_sprites_group.draw(screen)
        mirror_sprites_group.draw(screen)
        laser_sprite_group.draw(screen)

        clock.tick(FPS)

        pygame.display.flip()