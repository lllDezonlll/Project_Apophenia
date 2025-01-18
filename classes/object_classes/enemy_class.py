import pygame
from Constant_files.SPRITE_GROUPS import all_sprite_group, object_sprite_group, enemy_sprite_group, texture_enemy_sprite_group
from Constant_files.CONSTANTS import BOARD_LEFT, BOARD_TOP, CELL_SIZE
from classes.helper_classes.hitbox_classes import Hitbox
from Constant_files.CONSTANT_OBJECTS import object_description
from classes.gui_classes.gui_classes import Following_Texture
from funcs.prom_func.Load_func import load_image

class Enemy(pygame.sprite.Sprite):
    image = load_image('data/textures', 'test_enemy.png', colorkey=-1)

    def __init__(self, x, y, board, health=100):
        super().__init__(all_sprite_group, object_sprite_group, enemy_sprite_group)
        self.x = x  # Координата X врага на клеточном поле.
        self.y = y  # Координата Y врага на клеточном поле.
        self.board = board  # Доска, к которой привязан враг.

        self.health = health  # Здоровье врага.
        self.width = CELL_SIZE  # Ширина врага.
        self.height = CELL_SIZE  # Высота врага.
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        self.rect = pygame.Rect(BOARD_LEFT + x * CELL_SIZE, BOARD_TOP + y * CELL_SIZE, self.width, self.height)  # Прямоугольник для взаимодействия.

        self.hitbox = Hitbox(self)
        self.texture = Following_Texture(self, Enemy.image, [all_sprite_group, texture_enemy_sprite_group], rotatable=True)
        self.draw()

    # Получение урона.
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.state = 'destroyed'
            self.image.fill((255, 0, 0))  # Изменяем цвет на красный для визуального отображения сметри врага

    # Восстановление здоровья.
    def heal(self, amount):
        """ Восстановление здоровья врага """
        if self.health > 0:
            self.health += amount
            if self.health > 100:
                self.health = 100

    def draw(self):
        # Рисуем врага (например, красный квадрат)
        self.image.fill(pygame.Color('red'))

    # Взаимодействие с лазером.
    def interact_with_laser(self, laser):
        # Враг получает урон от лазера.
        self.take_damage(laser.damage)
        laser.kill_self()  # Уничтожить лазер.

    # Отображает своё описание в специальном информационном поле, при получении сигнала от своего хитбокса.
    def display_self_description(self):
        object_description.set_trackable_object(self)

    def kill_self(self):
        self.texture.kill()
        self.board.board[self.y][self.x] = '?'
        self.kill()

    def update(self):
        pass