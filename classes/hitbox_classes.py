from Constant_files.SPRITE_GROUPS import *


class Hitbox(pygame.sprite.Sprite):
    def __init__(self, object):
        super().__init__(all_sprite_group, hitbox_sprite_group)
        self.object = object
        self.rect = self.object.rect

    def update(self):
        self.rect = self.object.rect
        if (pygame.mouse.get_pos()[0] in range(self.rect.x, self.rect.x + self.rect.width) and
                pygame.mouse.get_pos()[1] in range(self.rect.y, self.rect.y + self.rect.height)):
            self.object.display_self_description()
