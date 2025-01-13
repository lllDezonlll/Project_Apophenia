from Constant_files.SPRITE_GROUPS import *


class Description(pygame.sprite.Sprite):
    def __init__(self, image, x, y, width, height):
        super().__init__(all_sprite_group, description_sprite_group)
        self.width, self.height = width, height
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.set_default_description_image()

    def set_default_description_image(self):
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, pygame.Color('red'), (0, 0, self.width, self.height), width=3)


class Tile_description(Description):
    def __init__(self, image, x, y, width, height):
        super().__init__(image, x, y, width, height)
        self.tile = None

    def set_trackable_tile(self, tile):
        self.tile = tile

    def display_tile_info(self):
        self.set_default_description_image()
        font = pygame.font.Font(None, 50)
        self.image.blit(font.render(type(self.tile).__name__, 1, pygame.Color('red')), (10, 10, self.width, self.height))

    def update(self):
        if self.tile is None:
            return
        self.display_tile_info()


class Object_descriptiom(Description):
    def __init__(self, image, x, y, width, height):
        super().__init__(image, x, y, width, height)
        self.object = None

    def set_trackable_object(self, object):
        self.object = object

    def display_object_info(self):
        self.set_default_description_image()
        font = pygame.font.Font(None, 50)
        self.image.blit(font.render(type(self.object).__name__, 1, pygame.Color('red')), (10, 10, self.width, self.height))
        self.image.blit(font.render(str(self.object.health) + 'HP', 1, pygame.Color('red')), (10, 50, self.width, self.height))

    def update(self):
        if self.object is None:
            return
        self.display_object_info()
