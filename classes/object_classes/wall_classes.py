import pygame
from Constant_files.CONSTANTS import BOARD_LEFT, BOARD_TOP, CELL_SIZE
from Constant_files.SPRITE_GROUPS import game_sprite_group, object_sprite_group, laser_sprite_group, wall_sprite_group, texture_health_group
from classes.helper_classes.hitbox_classes import Hitbox
from Constant_files.CONSTANT_OBJECTS import object_description
from classes.gui_classes.gui_classes import Health_Bar
from funcs.prom_funcs.Load_func import load_image


class Wall(pygame.sprite.Sprite):
    image = load_image('data/textures', 'test_wall.png')

    def __init__(self, x, y, board, health=100):
        super().__init__(game_sprite_group, object_sprite_group, wall_sprite_group)
        self.x, self.y, self.board = x, y, board
        self.value = 0

        self.health = health
        self.max_health = health

        self.image = Wall.image
        self.rect = pygame.Rect(BOARD_LEFT + x * CELL_SIZE, BOARD_TOP + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        self.hitbox = Hitbox(self)

        self.health_bar = Health_Bar(self, [None], [game_sprite_group, texture_health_group], offset_y=-22)

        self.laser = None

        self.board.add_object(self, del_previous=True)

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill_self()

    def display_self_description(self):
        object_description.set_trackable_object(self)

    def kill_self(self):
        self.board.del_object(self)
        self.rect.x, self.rect.y = 10000, 10000
        self.kill()

    def update(self, event):
        # Получает урон от лазера и уничтожает его при касании.
        if laser := pygame.sprite.spritecollideany(self, laser_sprite_group):
            if laser != self.laser:
                self.laser = laser
                self.take_damage(laser.damage)
                laser.kill_self()