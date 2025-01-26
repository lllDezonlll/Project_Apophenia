import pygame
from Constant_files.SPRITE_GROUPS import (game_sprite_group, object_sprite_group, enemy_sprite_group, laser_sprite_group,
                                          texture_enemy_sprite_group, mirror_sprite_group)
from Constant_files.CONSTANTS import BOARD_LEFT, BOARD_TOP, CELL_SIZE, CELL_COUNT
from classes.helper_classes.hitbox_classes import Hitbox
from Constant_files.CONSTANT_OBJECTS import object_description
from classes.gui_classes.gui_classes import Following_Texture
from classes.object_classes.tile_classes import Void_Tile
from classes.object_classes.wall_classes import Wall
from funcs.prom_funcs.Load_func import load_image
import networkx as nx


class Enemy(pygame.sprite.Sprite):
    image = load_image('data/textures', 'test_enemy.png', colorkey=-1)

    def __init__(self, x, y, objects_board, tiles_board, health=100, damage=1):
        super().__init__(game_sprite_group, object_sprite_group, enemy_sprite_group)
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
        self.texture = Following_Texture(self, Enemy.image, [game_sprite_group, texture_enemy_sprite_group])
        self.draw()
        self.next_move_calculated()

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
        graph = self.create_graph()
        start = (self.x, self.y)
        min_distance = float('inf')
        nearest_mirror = None

        for mirror in mirror_sprite_group:
            goal = (mirror.x, mirror.y)
            try:
                path = nx.dijkstra_path(graph, start, goal)
                distance = len(path) - 1
                if distance < min_distance:
                    min_distance = distance
                    nearest_mirror = mirror
            except nx.NetworkXNoPath:
                continue

        return nearest_mirror

    def move_towards_mirror(self):
        if self.path:
            next_x, next_y = self.next_move
            self.objects_board.board[self.y][self.x] = '?'
            self.objects_board.board[next_y][next_x] = self
            self.x = next_x
            self.y = next_y
            self.rect.x = BOARD_LEFT + self.x * CELL_SIZE
            self.rect.y = BOARD_TOP + self.y * CELL_SIZE

    def can_move(self, x, y):
        if x < 0 or x >= CELL_COUNT or y < 0 or y >= CELL_COUNT:
            return False
        if isinstance(self.tiles_board.board[y][x], (Wall, Void_Tile)):
            return False
        return True

    def next_move_calculated(self):
        # Найти ближайшее зеркало
        try:
            if len(self.target_mirror.groups()) == 0:
                self.target_mirror = None
        except Exception:
            pass
        else:
            self.target_mirror = self.find_nearest_mirror()
        try:
            if self.target_mirror:
                graph = self.create_graph()
                start = (self.x, self.y)
                goal = (self.target_mirror.x, self.target_mirror.y)
                self.next_move = self.astar_path(graph, start, goal)[0]
                # if self.path:
                    # self.moving = True
                # self.next_move = self.path.pop(0)
        except Exception:
            pass



    def create_graph(self):
        graph = nx.grid_2d_graph(CELL_COUNT, CELL_COUNT)
        nodes_to_remove = []
        for (x, y) in graph.nodes:
            if isinstance(self.tiles_board.board[y][x], (Wall, Void_Tile)):
                nodes_to_remove.append((x, y))
        for node in nodes_to_remove:
            graph.remove_node(node)
        return graph

    def astar_path(self, graph, start, goal):
        try:
            print(nx.astar_path(graph, start, goal))
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
                # if self.path:
                    # self.moving = True
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
        # self.target_mirror = self.find_nearest_mirror()

        # if self.moving and len(self.path) > 1:
            # self.move_towards_mirror()
            # if not self.path:
                # self.moving = False

        # if len(self.path) == 1:
          #  self.target_mirror.take_damage(self.damage)