import pygame
from classes.object_classes.base_class import base
from Constant_files.SPRITE_GROUPS import game_sprite_group, card_sprite_group, energy_sprite_group
from random import randrange
from classes.gui_classes.gui_classes import cursor
from Constant_files.CONSTANTS import LEFT_INTERFACE_LEFT, LEFT_INTERFACE_TOP


class Energy(pygame.sprite.Sprite):
    def __init__(self, default_count):
        super().__init__(game_sprite_group, energy_sprite_group)
        self.image = pygame.Surface((100, 100), pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 12, 300
        self.default_count = default_count
        self.current_count = default_count
        self.font = font = pygame.font.Font(None, 50)

    def spend_energy(self, amount):
        self.current_count -= amount

    def add_energy(self, amount):
        self.current_count += amount

    def return_to_default_count(self):
        self.current_count = self.default_count

    def update(self, event):
        self.image = pygame.Surface((100, 100), pygame.SRCALPHA, 32)
        self.image.blit(self.font.render(str(self.current_count), 1, pygame.Color('blue')), (10, 10, self.rect.w, self.rect.h))

energy = Energy(3)


class Deck_Active:
    def __init__(self):
        self.cards = []
        pass

    def add_cards(self, cards):
        self.cards.extend(cards)

    def draw_card(self, amount=1):
        for i in range(amount):
            if len(deck_hand.cards) == 10:
                break
            if len(self.cards) == 0:
                deck_discard.shuffle_to_deck_active()
            if len(self.cards) == 0:
                break
            card = self.cards.pop(randrange(0, len(self.cards)))
            deck_hand.add_card(card)


class Deck_Hand(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(game_sprite_group)
        self.cards = []
        pass

    def add_card(self, card):
        self.cards.append(card)
        card.change_deck(self)

    def discard_card(self, card):
        deck_discard.add_card(self.cards.pop(self.cards.index(card)))

    def show_cards(self):
        for i, card in enumerate(self.cards):
            # print(i, card)
            card.rect.y = LEFT_INTERFACE_TOP + (card.rect.h + 10) * i

    def update(self, event):
        self.show_cards()


class Deck_Discard:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)
        card.change_deck(self)

    def shuffle_to_deck_active(self):
        deck_active.add_cards(self.cards)
        self.cards = []


deck_active = Deck_Active()
deck_hand = Deck_Hand()
deck_discard = Deck_Discard()


class Card(pygame.sprite.Sprite):
    def __init__(self, deck=deck_active):
        super().__init__(game_sprite_group, card_sprite_group)
        self.deck = deck
        self.cost = 0
        self.mouse_down = False
        self.image = pygame.Surface((396, 48), pygame.SRCALPHA, 32)
        self.image.fill(pygame.Color('red'))
        self.rect = self.image.get_rect()
        self.rect.x = LEFT_INTERFACE_LEFT
        pass

    def play(self):
        pass

    def change_deck(self, deck):
        self.deck = deck

    def check_click_to_play(self, event):
        if pygame.mouse.get_pressed()[0]:
            self.mouse_down = True

        if not pygame.mouse.get_pressed()[0] and not pygame.sprite.collide_mask(self, cursor) and self.deck == deck_hand:
            self.mouse_down = False

        if not self.mouse_down:
            return

        if not pygame.mouse.get_pressed()[0] and pygame.sprite.collide_mask(self, cursor) and self.deck == deck_hand and self.mouse_down and energy.current_count >= self.cost:
            self.play()
            energy.spend_energy(self.cost)
            self.change_deck(deck_discard)
            self.mouse_down = False

    def update(self, *event):
        self.check_click_to_play(event)

        if self.deck == deck_hand:
            self.image.fill(pygame.Color('red'))
        else:
            self.image.fill(pygame.SRCALPHA)


class Attack(Card):
    def __init__(self):
        super().__init__(deck=deck_active)
        self.cost = 1

    def play(self):
        base.active_cannon.fire_laser(damage=10)
        deck_hand.discard_card(self)


class Heal(Card):
    def __init__(self):
        super().__init__(deck=deck_active)
        self.cost = 2

    def play(self):
        base.heal(5)
        deck_hand.discard_card(self)

    def update(self, *event):
        self.check_click_to_play(event)

        if self.deck == deck_hand:
            self.image.fill(pygame.Color('green'))
        else:
            self.image.fill(pygame.SRCALPHA)




deck_active.add_cards([Attack(), Attack(), Attack(), Attack(), Attack(), Heal(), Heal(), Heal(), Attack(), Attack(), Heal(), Attack(), Heal()])
