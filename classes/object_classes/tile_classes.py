import pygame
from Constant_files.CONSTANTS import BOARD_LEFT, BOARD_TOP, CELL_SIZE
from Constant_files.SPRITE_GROUPS import all_sprite_group, tiles_sprite_group, laser_sprite_group
from classes.helper_classes.hitbox_classes import Hitbox
from Constant_files.CONSTANT_OBJECTS import tile_description


# Обычный тайл, не имеющий никаких эффектов.
class Default_Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, board):
        self.x, self.y, self.board = x, y, board
        self.value = 0
        super().__init__(all_sprite_group, tiles_sprite_group)
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, pygame.Color((210, 247, 217)), (0, 0, CELL_SIZE, CELL_SIZE))
        self.rect = pygame.Rect(BOARD_LEFT + x * CELL_SIZE, BOARD_TOP + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        self.hitbox = Hitbox(self)

    # Отображает своё описание в специальном информационном поле, при получении сигнала от своего хитбокса.
    def display_self_description(self):
        tile_description.set_trackable_tile(self)

    def kill_self(self):
        self.kill()


# Пустой тайл. Просто клетка, на которой ничего нельзя расположить.
class Void_Tile(Default_Tile):
    def __init__(self, x, y, board):
        super().__init__(x, y, board)
        pygame.draw.rect(self.image, pygame.Color((0, 0, 0)), (0, 0, CELL_SIZE, CELL_SIZE))


# Класс стены.
class Wall_Tile(Default_Tile):
    def __init__(self, x, y, board):
        super().__init__(x, y, board)
        self.health = 100
        self.laser = None
        pygame.draw.rect(self.image, pygame.Color((97, 117, 101)), (0, 0, CELL_SIZE, CELL_SIZE))

    def update(self):
        # Получает урон от лазера и уничтожает его при касании.
        if laser := pygame.sprite.spritecollideany(self, laser_sprite_group):
            if laser != self.laser:
                self.laser = laser
                self.take_damage(laser.damage)
                laser.kill_self()

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.board.add_tile(Default_Tile(self.x, self.y, self.board))
            self.kill_self()

