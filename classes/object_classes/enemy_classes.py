import pygame
from Constant_files.SPRITE_GROUPS import (all_sprite_group, object_sprite_group, enemy_sprite_group, laser_sprite_group,
                                          texture_enemy_sprite_group, mirror_sprite_group)
from Constant_files.CONSTANTS import BOARD_LEFT, BOARD_TOP, CELL_SIZE, CELL_COUNT
from classes.helper_classes.hitbox_classes import Hitbox
from Constant_files.CONSTANT_OBJECTS import object_description
from classes.gui_classes.gui_classes import Following_Texture
from classes.object_classes.tile_classes import Wall_Tile, Void_Tile
from funcs.prom_funcs.Load_func import load_image
import networkx as nx


class Enemy(pygame.sprite.Sprite):
    image = load_image('data/textures', 'test_enemy.png', colorkey=-1)

    def __init__(self, x, y, objects_board, tiles_board, health=100, damage=1):
        super().__init__(all_sprite_group, object_sprite_group, enemy_sprite_group)
        self.x = x  # Координата X врага на клеточном поле.
        self.y = y  # Координата Y врага на клеточном поле.
        self.tiles_board = tiles_board  # Доска Тайлов
        self.objects_board = objects_board  # Доска, к которой привязан враг.
        self.damage = damage
        self.objects_board.add_object(self)
        self.laser = None
        self.target_mirror = None  # Инициализация целевого зеркала
        self.path = []  # Путь для движения
        self.moving = False  # Флаг для отслеживания движения

        self.health = health  # Здоровье врага.
        self.width = CELL_SIZE  # Ширина врага.
        self.height = CELL_SIZE  # Высота врага.
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        self.rect = pygame.Rect(BOARD_LEFT + x * CELL_SIZE, BOARD_TOP + y * CELL_SIZE, self.width, self.height)  # Прямоугольник для взаимодействия.

        self.hitbox = Hitbox(self)
        self.texture = Following_Texture(self, Enemy.image, [all_sprite_group, texture_enemy_sprite_group])
        self.draw()

    # Получение урона.
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill_self()
            self.image.fill((255, 0, 0))  # Изменяем цвет на красный для визуального отображения смерти врага

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

    # Отображает своё описание в специальном информационном поле, при получении сигнала от своего хитбокса.
    def display_self_description(self):
        object_description.set_trackable_object(self)

    def kill_self(self):
        self.texture.kill()
        self.objects_board.board[self.y][self.x] = '?'
        self.kill()

    def find_nearest_mirror(self):
        nearest_mirror = None
        min_distance = float('inf')
        for mirror in mirror_sprite_group:
            distance = ((mirror.x - self.x) ** 2 + (mirror.y - self.y) ** 2) ** 0.5
            if distance < min_distance:
                min_distance = distance
                nearest_mirror = mirror
        return nearest_mirror

    def move_towards_mirror(self):
        if self.path:
            next_x, next_y = self.path.pop(0)
            self.x = next_x
            self.y = next_y
            self.rect.x = BOARD_LEFT + self.x * CELL_SIZE
            self.rect.y = BOARD_TOP + self.y * CELL_SIZE

    def can_move(self, x, y):
        if x < 0 or x >= CELL_COUNT or y < 0 or y >= CELL_COUNT:
            return False
        if isinstance(self.tiles_board.board[y][x], (Wall_Tile, Void_Tile)):
            return False
        return True

    def create_graph(self):
        graph = nx.grid_2d_graph(CELL_COUNT, CELL_COUNT)
        nodes_to_remove = []
        for (x, y) in graph.nodes:
            if isinstance(self.tiles_board.board[y][x], (Wall_Tile, Void_Tile)):
                nodes_to_remove.append((x, y))
        for node in nodes_to_remove:
            graph.remove_node(node)
        return graph

    def astar_path(self, graph, start, goal):
        try:
            return nx.astar_path(graph, start, goal)
        except nx.NetworkXNoPath:
            return []

    def move(self):
        try:
            if self.target_mirror:
                graph = self.create_graph()
                start = (self.x, self.y)
                goal = (self.target_mirror.x, self.target_mirror.y)
                self.path = self.astar_path(graph, start, goal)
                print(self.path)
                if self.path:
                    self.moving = True
        except Exception:
            pass

    def update(self, *event):
        # Получает урон от лазера
        if laser := pygame.sprite.spritecollideany(self, laser_sprite_group):
            if laser != self.laser:
                self.laser = laser
                self.take_damage(laser.damage)
                laser.kill_self()

        # Найти ближайшее зеркало
        if not self.target_mirror or len(self.target_mirror.groups()) == 0:
            self.target_mirror = self.find_nearest_mirror()

        if self.moving and len(self.path) > 1:
            self.move_towards_mirror()
            if not self.path:
                self.moving = False

        if len(self.path) == 1:
            self.target_mirror.take_damage(self.damage)

        try:
            if len(self.target_mirror.groups()) == 0:
                self.target_mirror = None
                self.path = []
        except Exception:
            pass