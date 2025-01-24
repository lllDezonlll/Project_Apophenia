import pygame
from Constant_files.SPRITE_GROUPS import all_sprite_group, hitbox_sprite_group, cursor_sprite_group, object_manager_sprite_group
from Constant_files.CONSTANTS import BOARD_LEFT, BOARD_TOP, CELL_SIZE, CELL_COUNT, OBJECT_MANAGER_LEFT, OBJECT_MANAGER_TOP

# Класс игровых хитбоксов.
class Hitbox(pygame.sprite.Sprite):
    def __init__(self, object, clickable=False, is_manipulate_action=False):
        super().__init__(all_sprite_group, hitbox_sprite_group)
        self.object = object
        self.clickable = clickable
        self.is_manipulate_action = is_manipulate_action
        if self.clickable:
            self.mouse_down = False
        self.rect = self.object.rect

    def check_click(self):
        if pygame.mouse.get_pressed()[0]:
            self.mouse_down = True
            if ((pygame.mouse.get_pos()[0] not in range(BOARD_LEFT, BOARD_LEFT + CELL_COUNT * CELL_SIZE) or
                pygame.mouse.get_pos()[1] not in range(BOARD_TOP, BOARD_TOP + CELL_COUNT * CELL_SIZE)) and
                not (pygame.mouse.get_pos()[0] in range(OBJECT_MANAGER_LEFT, OBJECT_MANAGER_LEFT + 396) and
                     pygame.mouse.get_pos()[1] in range(OBJECT_MANAGER_TOP, OBJECT_MANAGER_TOP + 222))):
                self.object.deselect()

        if not pygame.mouse.get_pressed()[0] and not pygame.sprite.spritecollideany(self, cursor_sprite_group):
            self.mouse_down = False

        if not self.mouse_down:
            return

        if not pygame.mouse.get_pressed()[0] and pygame.sprite.spritecollideany(self, cursor_sprite_group) and self.mouse_down:
            self.object.pick_action()
            self.mouse_down = False

    def show_description(self):
        # Передаёт сигнал о отображении своего описания объектам, которых касается курсор.
        if (pygame.mouse.get_pos()[0] in range(self.rect.x, self.rect.x + self.rect.width) and
                pygame.mouse.get_pos()[1] in range(self.rect.y, self.rect.y + self.rect.height)):
            if type(self.object).__name__ == 'Base':
                return
            try:
                self.object.display_self_description()
            except Exception:
                self.object.object.display_self_description()

    def update(self, *event):
        # Следовние за объектом и подстраивание своих размеров под него.
        self.rect = self.object.rect
        if not self.is_manipulate_action:
            self.show_description()

        if self.clickable:
            self.check_click()


