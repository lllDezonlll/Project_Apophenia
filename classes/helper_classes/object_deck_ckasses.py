import pygame
from Constant_files.SPRITE_GROUPS import all_sprite_group, object_manager_sprite_group


class Object_manager(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprite_group, object_manager_sprite_group)
        self.objects = []

    def add_objects(self, objects):
        self.objects.extend(objects)

    def del_objects(self, objects):
        for object in objects:
            del self.objects[self.objects.index(object)]

    def show_objects(self):
        for i, object in self.objects:
            pass