import pygame
from Constant_files.SPRITE_GROUPS import (game_sprite_group, object_sprite_group, enemy_sprite_group, laser_sprite_group,
                                          texture_enemy_sprite_group, mirror_sprite_group, base_sprite_group)
from Constant_files.CONSTANTS import BOARD_LEFT, BOARD_TOP, CELL_SIZE, CELL_COUNT
from classes.helper_classes.hitbox_classes import Hitbox
from Constant_files.CONSTANT_OBJECTS import object_description
from classes.gui_classes.gui_classes import Following_Texture
from classes.object_classes.mirror_classes import Mirror
from classes.object_classes.tile_classes import Void_Tile
from classes.object_classes.wall_classes import Wall
from classes.object_classes.base_class import Base
from classes.object_classes.laser_class import Laser
from funcs.prom_funcs.Load_func import load_image
import networkx as nx


class Enemy(pygame.sprite.Sprite):
    image = load_image('data/textures', 'test_enemy.png', colorkey=-1)

    def __init__(self, x, y, objects_board, tiles_board, health=20, damage=20):
        super().__init__(game_sprite_group, object_sprite_group, enemy_sprite_group)
        self.x = x  # Координата X врага на клеточном поле.
        self.y = y  # Координата Y врага на клеточном поле.
        self.tiles_board = tiles_board  # Доска Тайлов
        self.objects_board = objects_board  # Доска, к которой привязан враг.
        self.damage = damage
        self.objects_board.add_object(self)
        self.laser = None
        self.target = None  # Инициализация целевого объекта
        self.next_move = None
        self.result = None

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

    def find_nearest_target(self):
        graph = self.create_graph()
        start = (self.x, self.y)
        min_distance = float('inf')
        nearest_target = None

        # Поиск ближайшего зеркала
        for mirror in mirror_sprite_group:
            goal = (mirror.x, mirror.y)
            try:
                path = nx.dijkstra_path(graph, start, goal)
                distance = len(path) - 1
                if distance < min_distance:
                    min_distance = distance
                    nearest_target = mirror
            except nx.NetworkXNoPath:
                continue

        # Поиск ближайшей базы
        for base in base_sprite_group:
            goal = (base.x, base.y)
            try:
                path = nx.dijkstra_path(graph, start, goal)
                distance = len(path) - 4
                if distance < min_distance:
                    min_distance = distance
                    nearest_target = base
            except nx.NetworkXNoPath:
                continue

        return nearest_target

    def do_action(self):
        if self.target is None:
            pass
        elif len(self.result) == 4 and type(self.target) == Base:
            self.deal_damage()
        elif len(self.result) == 2:
            self.deal_damage()
        else:
            self.move_towards_something()

    def move_towards_something(self):
        next_x, next_y = self.next_move
        self.objects_board.board[self.y][self.x] = '?'
        self.objects_board.board[next_y][next_x] = self
        self.x = next_x
        self.y = next_y
        self.rect.x = BOARD_LEFT + self.x * CELL_SIZE
        self.rect.y = BOARD_TOP + self.y * CELL_SIZE

    def deal_damage(self):
        if len(self.target.groups()) == 0:
            self.target = None
            return
        self.target.take_damage(self.damage)

    def can_move(self, x, y):
        if x < 0 or x >= CELL_COUNT or y < 0 or y >= CELL_COUNT:
            return False
        if isinstance(self.tiles_board.board[y][x], (Wall, Void_Tile)):
            return False
        return True

    def next_move_calculated(self):
        # Найти ближайший объект (зеркало или базу)
        self.target = self.find_nearest_target()

        try:
            if len(self.target.groups()) == 0:
                self.target = None
        except Exception:
            return

        try:
            if self.target:
                graph = self.create_graph()
                start = (self.x, self.y)
                goal = (self.target.x, self.target.y)
                self.result = self.astar_path(graph, start, goal)
                self.next_move = self.result[1]
        except Exception:
            pass

    def create_graph(self):
        graph = nx.grid_2d_graph(CELL_COUNT, CELL_COUNT)
        nodes_to_remove = []
        for (x, y) in graph.nodes:
            if isinstance(self.objects_board.board[y][x], (Wall, Base)):
                nodes_to_remove.append((x, y))
        for node in nodes_to_remove:
            graph.remove_node(node)
        return graph

    def astar_path(self, graph, start, goal):
        try:
            return nx.astar_path(graph, start, goal)
        except nx.NetworkXNoPath:
            return []

    def update(self, *event):
        # Получает урон от лазера
        if laser := pygame.sprite.spritecollideany(self, laser_sprite_group):
            if laser != self.laser:
                self.laser = laser
                self.take_damage(laser.damage)
                laser.kill_self()



class Enemy_Shooter(pygame.sprite.Sprite):
    image = load_image('data/textures', 'test_enemy.png', colorkey=-1)

    def __init__(self, x, y, objects_board, tiles_board, health=20, damage=20):
        super().__init__(game_sprite_group, object_sprite_group, enemy_sprite_group)
        self.x = x  # Координата X врага на клеточном поле.
        self.y = y  # Координата Y врага на клеточном поле.
        self.tiles_board = tiles_board  # Доска Тайлов
        self.objects_board = objects_board  # Доска, к которой привязан враг.
        self.damage = damage
        self.objects_board.add_object(self)
        self.laser = None
        self.target = None  # Инициализация целевого объекта
        self.next_move = None
        self.result = None

        self.health = health  # Здоровье врага.
        self.width = CELL_SIZE  # Ширина врага.
        self.height = CELL_SIZE  # Высота врага.
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        self.rect = pygame.Rect(BOARD_LEFT + x * CELL_SIZE, BOARD_TOP + y * CELL_SIZE, self.width, self.height)  # Прямоугольник для взаимодействия.

        self.hitbox = Hitbox(self)
        self.texture = Following_Texture(self, Enemy_Shooter.image, [game_sprite_group, texture_enemy_sprite_group])
        pygame.draw.rect(self.image, pygame.Color('red'), (24, 24, 2, 2))
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

    # Отображает своё описание в специальном информационном поле, при получении сигнала от своего хитбокса.
    def display_self_description(self):
        object_description.set_trackable_object(self)

    def kill_self(self):
        self.texture.kill()
        self.objects_board.board[self.y][self.x] = '?'
        self.kill()

    def find_target_on_line(self):
        # Поиск цели (базы или зеркала) на одной прямой с врагом
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Вниз, вправо, вверх, влево
        for dx, dy in directions:
            x, y = self.x + dx, self.y + dy
            while 0 <= x < CELL_COUNT and 0 <= y < CELL_COUNT:
                obj = self.objects_board.board[y][x]
                if isinstance(obj, (Base, Mirror)):
                    return obj
                if isinstance(self.tiles_board.board[y][x], (Wall, Void_Tile)):
                    break  # Прерываем, если на пути стена или пустота
                x += dx
                y += dy
        return None

    def shoot_laser(self):
        # Стрельба лазером в направлении цели
        if self.target:
            dx = self.target.x - self.x
            dy = self.target.y - self.y
            if dx == 0 and dy != 0:
                orientation = 90 if dy > 0 else -90
            elif dy == 0 and dx != 0:
                orientation = 0 if dx > 0 else 180
            else:
                return  # Не стреляем, если цель не на одной прямой

            # Создаем лазер
            laser_x = BOARD_LEFT + self.x * CELL_SIZE + CELL_SIZE // 2
            laser_y = BOARD_TOP + self.y * CELL_SIZE + CELL_SIZE // 2
            Laser(laser_x, laser_y, orientation, damage=self.damage)

    def do_action(self):
        # Поиск цели на прямой
        self.target = self.find_target_on_line()

        if self.target:
            self.shoot_laser()  # Стреляем, если цель на прямой
        else:
            # Если цель не на прямой, двигаемся к ближайшей цели
            if self.target is None:
                self.target = self.find_target_on_line()

            if self.target:
                if len(self.result) == 2:
                    self.deal_damage()
                else:
                    self.move_towards_something()

    def move_towards_something(self):
        next_x, next_y = self.next_move
        # Убедимся, что новая позиция допустима
        if self.can_move(next_x, next_y):
            # Удаляем себя с текущей позиции
            self.objects_board.board[self.y][self.x] = '?'
            # Перемещаемся на новую позицию
            self.x = next_x
            self.y = next_y
            # Обновляем позицию на доске
            self.objects_board.board[self.y][self.x] = self
            # Обновляем прямоугольник для отрисовки
            self.rect.x = BOARD_LEFT + self.x * CELL_SIZE
            self.rect.y = BOARD_TOP + self.y * CELL_SIZE

    def deal_damage(self):
        if len(self.target.groups()) == 0:
            self.target = None
            return
        self.target.take_damage(self.damage)

    def can_move(self, x, y):
        if x < 0 or x >= CELL_COUNT or y < 0 or y >= CELL_COUNT:
            return False
        if isinstance(self.tiles_board.board[y][x], (Wall, Void_Tile)):
            return False
        return True

    def next_move_calculated(self):
        # Найти ближайший объект (зеркало или базу)
        self.target = self.find_target_on_line()

        try:
            if len(self.target.groups()) == 0:
                self.target = None
        except Exception:
            return

        try:
            if self.target:
                graph = self.create_graph()
                start = (self.x, self.y)
                goal = (self.target.x, self.target.y)
                self.result = self.astar_path(graph, start, goal)
                if len(self.result) > 1:
                    self.next_move = self.result[1]
        except Exception:
            pass

    def create_graph(self):
        graph = nx.grid_2d_graph(CELL_COUNT, CELL_COUNT)
        nodes_to_remove = []
        for (x, y) in graph.nodes:
            if isinstance(self.objects_board.board[y][x], (Wall, Base)):
                nodes_to_remove.append((x, y))
        for node in nodes_to_remove:
            graph.remove_node(node)
        return graph

    def astar_path(self, graph, start, goal):
        try:
            return nx.astar_path(graph, start, goal)
        except nx.NetworkXNoPath:
            return []

    def update(self, *event):
        # Получает урон от лазера
        for laser in laser_sprite_group:
            if pygame.sprite.collide_mask(self, laser):
                if laser != self.laser:
                    self.laser = laser
                    self.take_damage(laser.damage)
                    laser.kill_self()