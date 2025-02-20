import pygame
from Constant_files.SPRITE_GROUPS import (game_sprite_group, object_sprite_group, enemy_sprite_group, laser_sprite_group,
                                          texture_enemy_sprite_group, mirror_sprite_group, base_sprite_group, texture_health_group)
from Constant_files.CONSTANTS import BOARD_LEFT, BOARD_TOP, CELL_SIZE, CELL_COUNT
from classes.helper_classes.hitbox_classes import Hitbox
from Constant_files.CONSTANT_OBJECTS import object_description
from classes.gui_classes.gui_classes import Following_Texture, Health_Bar
from classes.object_classes.mirror_classes import Mirror
from classes.object_classes.tile_classes import Void_Tile
from classes.object_classes.wall_classes import Wall
from classes.object_classes.base_classes import Base
from classes.object_classes.laser_class import Laser
from funcs.prom_funcs.Load_func import load_image
from random import choice
import networkx as nx


class Enemy(pygame.sprite.Sprite):
    image = load_image('data/textures', 'skeleton_1.png', colorkey=-1)
    image_2 = load_image('data/textures', 'skeleton_2.png', colorkey=-1)
    image_3 = load_image('data/textures', 'skeleton_3.png', colorkey=-1)
    image_4 = load_image('data/textures', 'skeleton_4.png', colorkey=-1)
    image_5 = load_image('data/textures', 'skeleton_5.png', colorkey=-1)
    image_6 = load_image('data/textures', 'skeleton_6.png', colorkey=-1)
    image_7 = load_image('data/textures', 'skeleton_7.png', colorkey=-1)
    image_8 = load_image('data/textures', 'skeleton_8.png', colorkey=-1)


    def __init__(self, x, y, objects_board, tiles_board, orientation, health=50, damage=20):
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
        self.orientation = orientation

        self.health = health  # Здоровье врага.
        self.max_health = health

        self.width = CELL_SIZE  # Ширина врага.
        self.height = CELL_SIZE  # Высота врага.
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        self.rect = pygame.Rect(BOARD_LEFT + x * CELL_SIZE, BOARD_TOP + y * CELL_SIZE, self.width, self.height)  # Прямоугольник для взаимодействия.

        self.hitbox = Hitbox(self)
        self.init_individual()
        self.draw()
        self.next_move_calculated()

    def init_individual(self):
        self.texture = Following_Texture(self, [Enemy.image, Enemy.image_2, Enemy.image_3, Enemy.image_4,
                                                Enemy.image_5, Enemy.image_6, Enemy.image_7, Enemy.image_8],
                                         [game_sprite_group, texture_enemy_sprite_group])
        self.health_bar = Health_Bar(self, [None], [game_sprite_group, texture_health_group], offset_y=-22)

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
        self.health_bar.kill()
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
                distance = len(path) - 1
                if distance < min_distance:
                    min_distance = distance
                    nearest_target = base
            except nx.NetworkXNoPath:
                continue

        return nearest_target

    def is_coordinate_free(self, x, y):
        """Проверка, свободна ли координата (x, y)"""
        if x < 0 or x >= CELL_COUNT or y < 0 or y >= CELL_COUNT:
            return False
        if isinstance(self.tiles_board.board[y][x], (Wall, Void_Tile)):
            return False
        if self.objects_board.board[y][x] != '?':
            return False
        for enemy in enemy_sprite_group:
            if enemy != self and enemy.x == x and enemy.y == y:
                return False
        return True

    def do_action(self):
        if self.target is None:
            pass
        elif len(self.result) == 2:
            self.deal_damage()
        else:
            self.move_towards_something()

    def move_towards_something(self):
        if self.is_coordinate_free(*self.next_move):
            next_x, next_y = self.next_move
            self.objects_board.board[self.y][self.x] = '?'
            if next_x > self.x:
                self.orientation = 0
            elif next_x < self.x:
                self.orientation = 180
            elif next_y > self.y:
                self.orientation = 90
            elif next_y < self.y:
                self.orientation = -90
            self.x = next_x
            self.y = next_y
            self.objects_board.add_object(self)
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
                if self.result:
                    self.next_move = self.result[1]
        except Exception:
            pass

    def create_graph(self):
        graph = nx.grid_2d_graph(CELL_COUNT, CELL_COUNT)
        nodes_to_remove = []

        for enemy in enemy_sprite_group:
            if enemy != self:  # Исключаем текущего врага
                x, y = enemy.x, enemy.y
                nodes_to_remove.append((x, y))

        for (x, y) in graph.nodes:
            if isinstance(self.objects_board.board[y][x], (Wall, Base)):
                nodes_to_remove.append((x, y))
        for node in nodes_to_remove:
            try:
                graph.remove_node(node)
            except nx.NetworkXError:
                pass
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
    image = load_image('data/textures', 'skeleton_1.png', colorkey=-1)

    def __init__(self, x, y, objects_board, tiles_board, orientation, health=40, damage=20):
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
        self.orientation = orientation

        self.health = health  # Здоровье врага.
        self.max_health = health

        self.width = CELL_SIZE  # Ширина врага.
        self.height = CELL_SIZE  # Высота врага.
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        self.rect = pygame.Rect(BOARD_LEFT + x * CELL_SIZE, BOARD_TOP + y * CELL_SIZE, self.width, self.height)  # Прямоугольник для взаимодействия.

        self.hitbox = Hitbox(self)
        self.texture = Following_Texture(self, [Enemy_Shooter.image], [game_sprite_group, texture_enemy_sprite_group])
        self.health_bar = Health_Bar(self, [None], [game_sprite_group, texture_health_group], offset_y=-22)
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
        self.health_bar.kill()
        self.objects_board.board[self.y][self.x] = '?'
        self.kill()

    def find_target_on_line(self):
        # Поиск цели (базы или зеркала) на одной прямой с врагом
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Вниз, вправо, вверх, влево
        for dx, dy in directions:
            x, y = self.x + dx, self.y + dy
            while 0 <= x < CELL_COUNT and 0 <= y < CELL_COUNT:
                obj = self.objects_board.board[y][x]
                if isinstance(obj, Wall):
                    break
                if isinstance(obj, (Base, Mirror)):
                    return obj
                if isinstance(self.tiles_board.board[y][x], (Wall, Void_Tile)):
                    break  # Прерываем, если на пути стена или пустота
                x += dx
                y += dy
        return None

    def find_nearest_target(self):
        # Поиск ближайшей цели (зеркала или базы) с помощью алгоритма Дейкстры
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
                distance = len(path) - 1
                if distance < min_distance:
                    min_distance = distance
                    nearest_target = base
            except nx.NetworkXNoPath:
                continue

        return nearest_target

    def shoot_laser(self):
        # Стрельба лазером в направлении цели
        if self.target:
            dx = self.target.x - self.x
            dy = self.target.y - self.y
            if dx == 0 and dy != 0:
                self.orientation = 90 if dy > 0 else -90
            elif dy == 0 and dx != 0:
                self.orientation = 0 if dx > 0 else 180
            else:
                return  # Не стреляем, если цель не на одной прямой

            # Создаем лазер
            laser_x = BOARD_LEFT + self.x * CELL_SIZE + CELL_SIZE // 2
            laser_y = BOARD_TOP + self.y * CELL_SIZE + CELL_SIZE // 2
            Laser(laser_x, laser_y, self.orientation, damage=self.damage)

    def do_action(self):
        # Поиск цели на прямой линии
        self.target = self.find_target_on_line()

        if self.target:
            # Если цель на прямой линии, стреляем
            self.shoot_laser()
        else:
            # Если цель не на прямой линии, ищем ближайшую цель
            self.target = self.find_nearest_target()
            if self.target:
                # Если ближайшая цель найдена, двигаемся к ней
                if len(self.result) == 2:
                    self.deal_damage()
                else:
                    self.move_towards_something()

    def move_towards_something(self):
        next_x, next_y = self.next_move
        # Убедимся, что новая позиция допустима
        if self.can_move(next_x, next_y):
            if next_x > self.x:
                self.orientation = 0
            elif next_x < self.x:
                self.orientation = 180
            elif next_y > self.y:
                self.orientation = 90
            elif next_y < self.y:
                self.orientation = -90
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
        # Найти цель на прямой линии
        self.target = self.find_target_on_line()

        # Если цель на прямой линии не найдена, ищем ближайшую цель
        if self.target is None:
            self.target = self.find_nearest_target()

        # Если цель найдена, рассчитываем путь
        if self.target:
            try:
                graph = self.create_graph()
                start = (self.x, self.y)
                goal = (self.target.x, self.target.y)
                self.result = self.astar_path(graph, start, goal)
                if len(self.result) > 1:
                    self.next_move = self.result[1]
            except Exception:
                pass
        else:
            # Если цель не найдена, останавливаемся
            self.next_move = None

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


# Разрушитель гробниц (таран)
class Enemy_Tomb_Wrecker(Enemy):
    def __init__(self, x, y, objects_board, tiles_board, orientation, health=50, damage=40):
        super().__init__(x, y, objects_board, tiles_board, orientation, health=health, damage=damage)
        self.move_counter = 0  # Счетчик ходов

    def do_action(self, *event):
        self.move_counter += 1  # Увеличиваем счетчик ходов

        # Ходим только каждый второй ход
        if self.move_counter % 2 == 0:
            super().do_action()

    def move_towards_something(self):
        next_x, next_y = self.next_move
        if isinstance(self.objects_board.board[next_y][next_x], Wall):
            wall = self.objects_board.board[next_y][next_x]
            wall.kill_self()
        if self.can_move(next_x, next_y):
            if next_x > self.x:
                self.orientation = 0
            elif next_x < self.x:
                self.orientation = 180
            elif next_y > self.y:
                self.orientation = 90
            elif next_y < self.y:
                self.orientation = -90
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

    def create_graph(self):
        graph = nx.grid_2d_graph(CELL_COUNT, CELL_COUNT)
        nodes_to_remove = []

        for enemy in enemy_sprite_group:
            if enemy != self:  # Исключаем текущего врага
                x, y = enemy.x, enemy.y
                nodes_to_remove.append((x, y))

        for (x, y) in graph.nodes:
            if isinstance(self.objects_board.board[y][x], Base):
                nodes_to_remove.append((x, y))
        for node in nodes_to_remove:
            try:
                graph.remove_node(node)
            except nx.NetworkXError:
                pass
        return graph


# Призрак
class Enemy_Ghost(Enemy):
    image = load_image('data/textures', 'ghost_1.png', colorkey=-1)
    image_2 = load_image('data/textures', 'ghost_2.png', colorkey=-1)
    image_3 = load_image('data/textures', 'ghost_3.png', colorkey=-1)
    image_4 = load_image('data/textures', 'ghost_4.png', colorkey=-1)
    image_5 = load_image('data/textures', 'ghost_5.png', colorkey=-1)
    image_6 = load_image('data/textures', 'ghost_6.png', colorkey=-1)
    image_7 = load_image('data/textures', 'ghost_7.png', colorkey=-1)
    image_8 = load_image('data/textures', 'ghost_8.png', colorkey=-1)

    def __init__(self, x, y, objects_board, tiles_board, orientation, health=10, damage=50):
        super().__init__(x, y, objects_board, tiles_board, orientation, health=health, damage=damage)

    def init_individual(self):
        self.texture = Following_Texture(self, [Enemy_Ghost.image, Enemy_Ghost.image_2, Enemy_Ghost.image_3, Enemy_Ghost.image_4,
                                                Enemy_Ghost.image_5, Enemy_Ghost.image_6, Enemy_Ghost.image_7, Enemy_Ghost.image_8],
                                         [game_sprite_group, texture_enemy_sprite_group])
        self.health_bar = Health_Bar(self, [None], [game_sprite_group, texture_health_group], offset_y=-22)

    def deal_damage(self):
        if len(self.target.groups()) == 0:
            self.explosion()
            return

        self.explosion()
        self.kill_self()

    def explosion(self):
        current_x, current_y = self.x, self.y
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                # Координаты соседней клетки
                neighbor_x = current_x + dx
                neighbor_y = current_y + dy

                if 0 <= neighbor_x < CELL_COUNT and 0 <= neighbor_y < CELL_COUNT:
                    neighbor_object = self.objects_board.board[neighbor_y][neighbor_x]

                    if neighbor_object != '?' and neighbor_object is not None:
                        if hasattr(neighbor_object, 'take_damage'):
                            neighbor_object.take_damage(self.damage)

    def do_action(self):
        super().do_action()
        if self.objects_board.board[self.y][self.x] != '?':
            super().do_action()
            if self.find_nearest_target() is None:
                self.explosion()


# Могильщик
class Enemy_Graveter(Enemy_Shooter):
    def __init__(self, x, y, objects_board, tiles_board, orientation, health=15, damage=10):
        super().__init__(x, y, objects_board, tiles_board, orientation, health=health, damage=damage)

    def shoot_laser(self):
        # Стрельба лазером в направлении цели
        laser_x = BOARD_LEFT + self.x * CELL_SIZE + CELL_SIZE // 2
        laser_y = BOARD_TOP + self.y * CELL_SIZE + CELL_SIZE // 2
        Laser(laser_x, laser_y, 0, damage=self.damage)
        Laser(laser_x, laser_y, 90, damage=self.damage)
        Laser(laser_x, laser_y, -90, damage=self.damage)
        Laser(laser_x, laser_y, 180, damage=self.damage)

    def do_action(self):
        self.shoot_laser()
        # масив доступных клеток
        available_cells = []
        for dx in range(CELL_COUNT):
            for dy in range(CELL_COUNT):
                if self.objects_board.board[dy][dx] == '?':
                    available_cells.append((dx, dy))
        if available_cells:
            self.x, self.y = choice(available_cells)
            # Удаляем себя с текущей позиции
            self.objects_board.board[self.y][self.x] = '?'
            # Обновляем позицию на доске
            self.objects_board.board[self.y][self.x] = self
            # Обновляем прямоугольник для отрисовки
            self.rect.x = BOARD_LEFT + self.x * CELL_SIZE
            self.rect.y = BOARD_TOP + self.y * CELL_SIZE


"""# Большой скелет толкатель
class Big_boneser(Enemy):
    def __init__(self, x, y, objects_board, tiles_board, orientation, health=100, damage=30):
        super().__init__(x, y, objects_board, tiles_board, orientation, health=health, damage=damage)

    def create_graph(self):
        graph = nx.grid_2d_graph(CELL_COUNT, CELL_COUNT)
        nodes_to_remove = []

        # Удаляем узлы, соответствующие другим врагам
        for enemy in enemy_sprite_group:
            if enemy != self:  # Исключаем текущего врага
                x, y = enemy.x, enemy.y
                nodes_to_remove.append((x, y))

        # Удаляем узлы, соответствующие базе
        for base in base_sprite_group:
            nodes_to_remove.append((base.x, base.y))

        # Удаляем узлы, которые находятся за пределами карты или являются Void_Tile
        for (x, y) in graph.nodes:
            if x < 0 or x >= CELL_COUNT or y < 0 or y >= CELL_COUNT:
                nodes_to_remove.append((x, y))
            if isinstance(self.tiles_board.board[y][x], Void_Tile):
                nodes_to_remove.append((x, y))

        # Удаляем узлы из графа
        for node in nodes_to_remove:
            try:
                graph.remove_node(node)
            except nx.NetworkXError:
                pass

        # Добавляем ребра, если между клетками стоит одна стена
        for (x, y) in graph.nodes:
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Только соседние клетки (без диагоналей)
                neighbor_x = x + dx
                neighbor_y = y + dy

                # Проверяем, что соседняя клетка находится в пределах карты
                if 0 <= neighbor_x < CELL_COUNT and 0 <= neighbor_y < CELL_COUNT:
                    # Если между клетками стоит одна стена, добавляем ребро
                    if isinstance(self.tiles_board.board[neighbor_y][neighbor_x], Wall):
                        # Проверяем, что за стеной нет другой стены
                        behind_wall_x = neighbor_x + dx
                        behind_wall_y = neighbor_y + dy

                        if 0 <= behind_wall_x < CELL_COUNT and 0 <= behind_wall_y < CELL_COUNT:
                            if not isinstance(self.tiles_board.board[behind_wall_y][behind_wall_x], Wall):
                                graph.add_edge((x, y), (neighbor_x, neighbor_y))

        return graph

    def move_towards_something(self):
        if self.next_move is None:
            return

        next_x, next_y = self.next_move

        # Проверяем, является ли следующая клетка стеной
        if isinstance(self.tiles_board.board[next_y][next_x], Wall):
            # Координаты за стеной
            dx = next_x - self.x
            dy = next_y - self.y
            behind_wall_x = next_x + dx
            behind_wall_y = next_y + dy

            # Проверяем, что за стеной нет другой стены и клетка свободна
            if 0 <= behind_wall_x < CELL_COUNT and 0 <= behind_wall_y < CELL_COUNT:
                if self.objects_board.board[behind_wall_y][behind_wall_x] == '?':
                    if self.is_coordinate_free(behind_wall_x, behind_wall_y):
                        # Толкаем стену
                        self.tiles_board.board[behind_wall_y][behind_wall_x] = self.tiles_board.board[next_y][next_x]
                        self.tiles_board.board[next_y][next_x] = None

                        # Перемещаем Big_boneser на следующую клетку
                        self.objects_board.board[self.y][self.x] = '?'
                        self.x, self.y = next_x, next_y
                        self.objects_board.add_object(self)
                        self.rect.x = BOARD_LEFT + self.x * CELL_SIZE
                        self.rect.y = BOARD_TOP + self.y * CELL_SIZE

        # Если следующая клетка не стена или стену нельзя толкнуть, двигаемся как обычно
        if self.is_coordinate_free(next_x, next_y):
            print(True)
            self.objects_board.board[self.y][self.x] = '?'
            self.x, self.y = next_x, next_y
            self.objects_board.add_object(self)
            self.rect.x = BOARD_LEFT + self.x * CELL_SIZE
            self.rect.y = BOARD_TOP + self.y * CELL_SIZE
        else:
            print(False)
            
    def do_action(self):
        super().do_action()
"""

