import pygame
from pygame.locals import KEYDOWN, K_w, K_s, K_a, K_d, K_j
from aggressive import Aggressive
from bullet import Bullet
import const as CONST

BOTTOM_MARGIN = 10

class Hero(Aggressive):
    def __init__(self, game):
        super(Hero, self).__init__(game, {
            "direction": CONST.UP,
            "image": "images/hero1.png",
            "bulletIndex": 1,
        })
        self.rect.centerx = game.screen.get_width() / 2
        self.rect.bottom = game.screen.get_height() - BOTTOM_MARGIN
    
    def handleEvent(self, events):
        keys = pygame.key.get_pressed()
        if keys[K_w]:
            self.move(CONST.UP)
        if keys[K_s]:
            self.move(CONST.DOWN)
        if keys[K_a]:
            self.move(CONST.LEFT)
        if keys[K_d]:
            self.move(CONST.RIGHT)

    def tick(self):
        super(Hero, self).tick()
    
    def move(self, direction):
        if direction == CONST.UP:
            self.rect.top = max(0, self.rect.top - CONST.HERO_SPEED)
        elif direction == CONST.DOWN:
            self.rect.bottom = min(self.game.screen.get_height() - BOTTOM_MARGIN, self.rect.bottom + CONST.HERO_SPEED)
        elif direction == CONST.LEFT:
            self.rect.left = max(0, self.rect.left - CONST.HERO_SPEED)
        elif direction == CONST.RIGHT:
            self.rect.right = min(self.game.screen.get_width(), self.rect.right + CONST.HERO_SPEED)