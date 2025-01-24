import pygame
from Constant_files.SPRITE_GROUPS import all_sprite_group, object_sprite_group, mirror_sprite_group, texture_mirror_sprite_group
from Constant_files.CONSTANTS import BOARD_LEFT, BOARD_TOP, CELL_SIZE
from classes.helper_classes.hitbox_classes import Hitbox
from Constant_files.CONSTANT_OBJECTS import object_description
from classes.gui_classes.gui_classes import Following_Texture
from funcs.prom_funcs.Load_func import load_image


# Класс обычного одностороннего зеркала с обычным 90-градусным отражением.
class Mirror(pygame.sprite.Sprite):
    image = load_image('data/textures', 'mirror_test.png')

    def __init__(self, x, y, orientation, board, health=100, state='normal', unique_abilities=None, is_place_action=False):
        super().__init__(all_sprite_group, object_sprite_group, mirror_sprite_group)
        self.x = x  # Координата X зеркала на клеточном поле.
        self.y = y  # Координата Y зеркала на клеточном поле.
        self.board = board  # Доска, к которой привязано зеркало.

        self.orientation = orientation  # Поворот зеркала.
        self.health = health  # Здоровье зеркала.
        self.state = state  # Состояние зеркала (например, нормальное, поврежденное).
        self.unique_abilities = unique_abilities if unique_abilities else []  # Уникальные способности.
        self.width = CELL_SIZE  # Ширина зеркала.
        self.height = CELL_SIZE  # Высота зеркала.
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        self.rect = pygame.Rect(BOARD_LEFT + x * CELL_SIZE, BOARD_TOP + y * CELL_SIZE, self.width, self.height)  # Прямоугольник для взаимодействия.

        if is_place_action:
            self.rect.x = 10000

        self.hitbox = Hitbox(self)
        self.texture = Following_Texture(self, Mirror.image, [all_sprite_group, texture_mirror_sprite_group], rotatable=True, offset_x=0, offset_y=0)
        if not is_place_action:
            self.board.add_object(self, del_previous=True)

        self.board.print_objects()
        self.draw()

    # Получение урона.
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill_self()

    # Восстановление здоровья.
    def heal(self, amount):
        """ Восстановление здоровья зеркала """
        if self.state != 'destroyed':
            self.health += amount
            if self.health > 100:
                self.health = 100

    def draw(self):
        # Рисуем диагонали в зависимости от ориентации зеркала
        if self.orientation in [180, 0]:
            pygame.draw.line(self.image, pygame.Color('blue'), (0, 0), (CELL_SIZE, CELL_SIZE), 2)
        elif self.orientation in [90, -90]:
            pygame.draw.line(self.image, pygame.Color('blue'), (0, CELL_SIZE), (CELL_SIZE, 0), 2)

    # Отражение задетого лазера.
    def reflect_laser(self, laser):
        # Зеркало не отражает, если оно сломано.
        if self.state == 'destroyed':
            return

        # Далее идут правила отражения этого зеркала.
        if self.orientation == 0:  # Узнать поворот зеркала.
            if laser.orientation == 90:  # Узнать поворот лазера.
                laser.orientation = 0  # Поменять направление полёта лазера.
            elif laser.orientation == 180:  # Узнать поворот лазера, прилетевшего с другой стороны.
                laser.orientation = -90  # Поменять направление полёта лазера.
            else:  # В случае прилёта лазера не по правилам отражения:
                self.take_damage(laser.damage)  # Получить урон.
                laser.kill_self()  # Уничтожить лазер.

        elif self.orientation == 90:
            if laser.orientation == -90:
                laser.orientation = 0
            elif laser.orientation == 180:
                laser.orientation = 90
            else:
                self.take_damage(laser.damage)
                laser.kill_self()

        elif self.orientation == 180:
            if laser.orientation == 0:
                laser.orientation = 90
            elif laser.orientation == -90:
                laser.orientation = 180
            else:
                self.take_damage(laser.damage)
                laser.kill_self()

        elif self.orientation == -90:
            if laser.orientation == 0:
                laser.orientation = -90
            elif laser.orientation == 90:
                laser.orientation = 180
            else:
                self.take_damage(laser.damage)
                laser.kill_self()

    # Отображает своё описание в специальном информационном поле, при получении сигнала от своего хитбокса.
    def display_self_description(self):
        object_description.set_trackable_object(self)

    def kill_self(self):
        self.texture.kill()
        self.board.del_object(self)
        self.rect.x, self.rect.y = 10000, 10000
        self.kill()

    def update(self, event):
        pass
