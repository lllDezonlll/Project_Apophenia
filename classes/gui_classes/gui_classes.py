import pygame
from Constant_files.SPRITE_GROUPS import game_sprite_group, cursor_sprite_group, tiles_sprite_group, object_sprite_group, object_manager_sprite_group, texture_cursor_sprite_group
from funcs.prom_funcs.Load_func import load_image
from Constant_files.CONSTANT_OBJECTS import object_description, tile_description


# Класс текстур, накладываемых поверх игровых объектов.
class Following_Texture(pygame.sprite.Sprite):
    def __init__(self, object, image, *groups, rotatable=False, offset_x=0, offset_y=0):
        super().__init__(*groups)
        self.image = image
        self.default_image = image
        self.rect = self.image.get_rect()
        self.object = object
        self.offset_x, self.offset_y = offset_x, offset_y
        self.default_offset_x, self.default_offset_y = offset_x, offset_y
        self.rotatable = rotatable
        self.rect.x, self.rect.y = 10000, 10000
        if self.rotatable:
            self.orientation = None

    def update(self, event):
        # Проверка на статичность или ?вращабельность?.
        if self.rotatable:
            if self.orientation != self.object.orientation:
                self.orientation = self.object.orientation
                self.rotate()

        # Следование за игровым объектом
        self.rect.x, self.rect.y = self.object.rect.x + self.offset_x, self.object.rect.y + self.offset_y

    # Вращает такстуру в зависимости от поворота следуемого объекта. Работает только при rotatable=True.
    def rotate(self):
        self.offset_x, self.offset_y = self.default_offset_x, self.default_offset_y
        if self.orientation == 90:
            self.offset_x, self.offset_y = self.object.rect.w - self.offset_y - self.rect.h, self.offset_x
        if self.orientation == 180:
            self.offset_x, self.offset_y = self.object.rect.h - self.offset_x - self.rect.w, self.object.rect.w - self.offset_y - self.rect.h
        if self.orientation == -90:
            self.offset_x, self.offset_y = self.offset_y, self.object.rect.h - self.offset_x - self.rect.w
        self.image = pygame.transform.rotate(self.default_image, -self.object.orientation)


# Класс игрового курсора.
class Cursor(pygame.sprite.Sprite):
    image = load_image('data/textures', 'test_cursor.png')

    def __init__(self):
        super().__init__(game_sprite_group, cursor_sprite_group)
        self.image = pygame.Surface((1, 1), pygame.SRCALPHA, 32)
        self.image.fill(pygame.Color('white'))
        self.rect = self.image.get_rect()
        self.texture = Following_Texture(self, Cursor.image, [game_sprite_group, texture_cursor_sprite_group], offset_y=-3, offset_x=-3)

    def update(self, event):
        # Следование за системным курсором и обновления затрагиваемого описания.
        self.update_description()
        if pygame.mouse.get_focused():
            self.rect.x, self.rect.y = pygame.mouse.get_pos()

    # Ставит обычную картинку классам описания тайлов и объектов, если игрок не навёлся на предмет описания.
    def update_description(self):
        if not pygame.sprite.spritecollideany(self, tiles_sprite_group):
            tile_description.set_default_description_image()
        if (not pygame.sprite.spritecollideany(self, object_sprite_group) and not
        pygame.sprite.spritecollideany(self, object_manager_sprite_group)):
            object_description.set_default_description_image()


cursor = Cursor()   # Создание курсора.


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, image, groups):
        super().__init__(*groups)
        self.mouse_down = False
        self.image = pygame.Surface((300, 100), pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.image.fill('green')

    def check_click(self):
        if pygame.mouse.get_pressed()[0]:
            self.mouse_down = True

        if not pygame.mouse.get_pressed()[0] and not pygame.sprite.collide_mask(self, cursor):
            self.mouse_down = False

        if not self.mouse_down:
            return False

        if not pygame.mouse.get_pressed()[0] and pygame.sprite.collide_mask(self, cursor) and self.mouse_down:
            self.mouse_down = False
            return True

        return False

    def update(self):

        return self.check_click()
