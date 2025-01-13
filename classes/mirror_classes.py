import pygame
from Constant_files.SPRITE_GROUPS import all_sprite_group, mirror_sprite_group
from Constant_files.CONSTANTS import BOARD_LEFT, BOARD_TOP, CELL_SIZE
from classes.hitbox_classes import Hitbox
from Constant_files.CONSTANT_OBJECTS import object_description


class Mirror(pygame.sprite.Sprite):
    def __init__(self, x, y, orientation,  health=100, reflection_angle=45, state='normal', unique_abilities=None):
        super().__init__(all_sprite_group, mirror_sprite_group)
        self.x = BOARD_LEFT + x * CELL_SIZE # Координата X зеркала
        self.y = BOARD_TOP + y * CELL_SIZE # Координата Y зеркала

        self.orientation = orientation
        self.health = health  # Здоровье зеркала
        self.reflection_angle = reflection_angle  # Угол отражения
        self.state = state  # Состояние зеркала (например, нормальное, поврежденное)
        self.unique_abilities = unique_abilities if unique_abilities else []  # Уникальные способности
        self.width = CELL_SIZE  # Ширина зеркала
        self.height = CELL_SIZE  # Высота зеркала
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)  # Прямоугольник для взаимодействия
        self.rotation_angle = 0  # Угол поворота зеркала (в градусах)
        self.hitbox = Hitbox(self)
        self.draw()

    def rotate(self, angle):
        """ Поворот зеркала """
        self.rotation_angle = (self.rotation_angle + angle) % 360
        self.image = pygame.transform.rotate(self.create_mirror_image(), self.rotation_angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def create_mirror_image(self):
        """ Создание базового изображения зеркала """
        mirror_image = pygame.Surface((self.width, self.height))
        mirror_image.fill((255, 255, 255))  # Белый цвет для зеркала
        pygame.draw.polygon(mirror_image, (0, 0, 0), [(0, 0), (self.width, 0), (self.width, self.height),
                                                      (0, self.height)])  # Рисуем простое прямоугольное зеркало
        return mirror_image

    def reflect_laser(self, laser_angle):
        """ Отражение лазера от зеркала """
        new_angle = laser_angle + self.reflection_angle
        return new_angle % 360  # Возвращаем новый угол отражения, ограниченный диапазоном [0, 360]

    def take_damage(self, damage):
        """ Уменьшение здоровья зеркала """
        self.health -= damage
        if self.health <= 0:
            self.state = 'destroyed'
            self.image.fill((255, 0, 0))  # Изменяем цвет на красный для визуализации разрушенного состояния

    def heal(self, amount):
        """ Восстановление здоровья зеркала """
        if self.state != 'destroyed':
            self.health += amount
            if self.health > 100:
                self.health = 100

    def activate_ability(self):
        """ Активация уникальной способности (по типу зеркала) """
        pass

    def update(self):
        """ Обновление состояния зеркала """
        pass

    def draw(self):
        # Рисуем диагонали в зависимости от ориентации зеркала
        if self.orientation in [1, 2]:
            pygame.draw.line(self.image, pygame.Color('blue'), (0, 0), (CELL_SIZE, CELL_SIZE), 2)
        elif self.orientation in [3, 4]:
            pygame.draw.line(self.image, pygame.Color('blue'), (0, CELL_SIZE), (CELL_SIZE, 0), 2)

    # Пример уникальной способности
    def unique_ability_example(self):
        pass

    def reflect_laser(self, laser):
        if self.state == 'destroyed':
            return
        if self.orientation == 1:
            if laser.direction == 'right':
                laser.direction = 'down'
            elif laser.direction == 'up':
                laser.direction = 'left'
            else:
                self.take_damage(laser.damage)
                laser.kill_self()

        elif self.orientation == 2:
            if laser.direction == 'down':
                laser.direction = 'right'
            elif laser.direction == 'left':
                laser.direction = 'up'
            else:
                self.take_damage(laser.damage)
                laser.kill_self()

        elif self.orientation == 3:
            if laser.direction == 'right':
                laser.direction = 'up'
            elif laser.direction == 'down':
                laser.direction = 'left'
            else:
                self.take_damage(laser.damage)
                laser.kill_self()

        elif self.orientation == 4:
            if laser.direction == 'up':
                laser.direction = 'right'
            elif laser.direction == 'left':
                laser.direction = 'down'
            else:
                self.take_damage(laser.damage)
                laser.kill_self()

    def display_self_description(self):
        object_description.set_trackable_object(self)
