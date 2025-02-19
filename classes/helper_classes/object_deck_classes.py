import pygame
from Constant_files.SPRITE_GROUPS import game_sprite_group, object_manager_sprite_group, laser_sprite_group, energy_sprite_group
from Constant_files.CONSTANTS import OBJECT_MANAGER_LEFT, OBJECT_MANAGER_TOP
from classes.object_classes.mirror_classes import Mirror
from classes.helper_classes.deck_and_cards_classes import Energy
from classes.object_classes.wall_classes import Wall
from classes.helper_classes.board_classes import game_objects_board
from classes.helper_classes.hitbox_classes import Hitbox
from funcs.prom_funcs.Calc_coords_func import find_coords_on_board
from funcs.prom_funcs.Load_func import fullname


class Elixir(Energy):
    def __init__(self, default_count):
        super().__init__(default_count)
        self.rect.x = 1512



elixir = Elixir(float('inf'))


class Object_manager(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(game_sprite_group, object_manager_sprite_group)
        self.image = pygame.Surface((1, 1), pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.max_object_count = 28
        self.picked_action = None
        self.objects = []

    def add_objects(self, objects):
        for object in objects:
            if self.max_object_count != len(self.objects):
                self.objects.append(object)

    def del_objects(self, objects):
        for object in objects:
            del self.objects[self.objects.index(object)]

    def show_objects(self):
        for i, object in enumerate(self.objects):
            object.rect.x = OBJECT_MANAGER_LEFT + i % 7 * (object.rect.w + 6)
            object.rect.y = OBJECT_MANAGER_TOP + i // 7 * (object.rect.h + 6)

    def pick_action(self, action):
        self.picked_action = action
        for curr_action in self.objects:
            if self.picked_action != curr_action:
                curr_action.deselect()

    def rotate_objects(self, rotate_way):
        for object in list(filter(lambda x: type(x) == Place_action, self.objects)):
            if rotate_way == 'right':
                object.rotate_object(90)
            else:
                object.rotate_object(-90)

    def update(self, *event):
        self.show_objects()

        if self.picked_action is None:
            return

        self.picked_action.do_action()


object_manager = Object_manager()


class Place_action(pygame.sprite.Sprite):
    def __init__(self, object, has_orientation=True):
        super().__init__(game_sprite_group, object_manager_sprite_group)
        self.font = pygame.font.Font(fullname('data/fonts', 'CustomFontTtf12H10.ttf'), 24)
        self.cost = 1
        self.object_manager = object_manager
        self.mouse_down = False
        self.object = object
        self.has_orientation = has_orientation
        self.selected = False
        self.image = type(object).image
        self.default_image = self.image
        self.rect = self.image.get_rect()
        self.hitbox = Hitbox(self, clickable=True)

    def pick_action(self):
        if self.selected:
            self.selected = False
            self.object_manager.pick_action(None)
            return
        self.selected = True
        self.object_manager.pick_action(self)

    def deselect(self):
        self.selected = False

    def do_action(self):

        x, y = self.check_click()

        if laser_sprite_group.sprites() != []:
            print('Есть лазеры')
            return

        if not x is None and not y is None and game_objects_board.board[y][x] == '?':
            if self.cost <= elixir.current_count:
                elixir.spend_energy(self.cost)
            else:
                return
            if self.has_orientation:
                type(self.object)(x, y, self.object.orientation, game_objects_board)
            else:
                type(self.object)(x, y, game_objects_board)

    def check_click(self):
        if pygame.mouse.get_pressed()[0]:
            self.mouse_down = True

        if not pygame.mouse.get_pressed()[0] and self.mouse_down:
            x, y = find_coords_on_board(*pygame.mouse.get_pos())
            self.mouse_down = False

            if x not in range(19) or y not in range(19) or (x in range(8, 11) and y in range(8, 11)):
                return None, None

            return x, y


        return None, None

    def rotate_object(self, angle):
        if not self.has_orientation:
            return
        self.object.orientation = self.object.orientation + angle
        if self.object.orientation == 270:
            self.object.orientation = -90
        elif self.object.orientation == -180:
            self.object.orientation = 180
        self.image = pygame.transform.rotate(self.image, -angle)
        self.default_image = pygame.transform.rotate(self.default_image, -angle)

    def update(self, event):
        self.image = self.default_image.copy()
        if self.selected:
            pygame.draw.rect(self.image, pygame.Color('white'), (0, 0, 48, 48), width=2)
        self.image.blit(self.font.render(str(self.cost), 1, pygame.Color('white')), (2, 26))


class Manipulate_action(pygame.sprite.Sprite):
    def __init__(self, manipulate_x, manipulate_y):
        super().__init__(game_sprite_group, object_manager_sprite_group)
        self.font = pygame.font.Font(fullname('data/fonts', 'CustomFontTtf12H10.ttf'), 24)
        self.cost = 1
        self.image = pygame.Surface((48, 48), pygame.SRCALPHA, 32)
        self.manipulate_x, self.manipulate_y = manipulate_x, manipulate_y
        self.mouse_down = False
        self.selected = False
        self.default_image = pygame.Surface((48, 48), pygame.SRCALPHA, 32)
        self.object_manager = object_manager
        self.image.fill(pygame.Color('red'))
        self.default_image.fill(pygame.Color('red'))
        self.rect = self.image.get_rect()
        self.hitbox = Hitbox(self, clickable=True, is_manipulate_action=True)

    def pick_action(self):
        if self.selected:
            self.selected = False
            self.object_manager.pick_action(None)
            return
        self.selected = True
        self.object_manager.pick_action(self)

    def deselect(self):
        self.selected = False

    def do_action(self):
        if laser_sprite_group.sprites() != []:
            print('Есть лазеры')
            return

        x, y = self.check_click()
        if not x is None and not y is None:
            if self.cost <= elixir.current_count:
                elixir.spend_energy(self.cost)
            else:
                return
            object = game_objects_board.board[y][x]
            if object != '?':
                self.manipulate_with_object(object, x, y)
            else:
                elixir.add_energy(self.cost)

    def manipulate_with_object(self, object, x, y):
        if (not 0 <= x + self.manipulate_x <= 18 or not 0 <= y + self.manipulate_y <= 18 or
                x + self.manipulate_x in range(8, 11) and y + self.manipulate_y in range(8, 11)):
            print('Выход за поле или попадание объекта на базу игрока.')
            elixir.add_energy(self.cost)
            return

        if game_objects_board.board[y + self.manipulate_y][x + self.manipulate_x] != '?':
            print('Передвижение объекта на другой объект невозможно.')
            elixir.add_energy(self.cost)
            return

        game_objects_board.board[y][x] = '?'
        object.x += self.manipulate_x
        object.y += self.manipulate_y
        object.rect.x += 48 * self.manipulate_x
        object.rect.y += 48 * self.manipulate_y
        game_objects_board.add_object(object)

        game_objects_board.print_objects()

    def check_click(self):
        if pygame.mouse.get_pressed()[0]:
            self.mouse_down = True

        if not pygame.mouse.get_pressed()[0] and self.mouse_down:
            x, y = find_coords_on_board(*pygame.mouse.get_pos())
            self.mouse_down = False

            if x not in range(19) or y not in range(19):
                return None, None

            return x, y

        return None, None

    def update(self, event):
        if self.selected:
            pygame.draw.rect(self.image, pygame.Color('white'), (0, 0, 48, 48), width=2)
        else:
            self.image = self.default_image.copy()
        self.image.blit(self.font.render(str(self.cost), 1, pygame.Color('white')), (2, 26))


object_manager.add_objects([Place_action(Mirror(10000, 10000, 0, game_objects_board, is_place_action=True)),
                            Place_action(Wall(10000, 10000, game_objects_board), has_orientation=False),
                            Manipulate_action(1, 0),
                            Manipulate_action(-1, 0),
                            Manipulate_action(0, 1),
                            Manipulate_action(0, -1),
                            Place_action(Mirror(10000, 10000, 0, game_objects_board, is_place_action=True)),
                            Place_action(Wall(10000, 10000, game_objects_board), has_orientation=False),
                            Manipulate_action(1, 0),
                            Manipulate_action(-1, 0),
                            Manipulate_action(0, 1),
                            Manipulate_action(0, -1),
                            ])