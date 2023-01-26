import pygame
from bullet import Bullet
import const as CONST

FIRE_SOUND = None

class Aggressive:
    def __init__(self, game, config):
        self.game = game
        self.direction = config.get("direction", CONST.UP)
        self.image = pygame.image.load(config["image"]).convert_alpha()
        self.bulletIndex = config.get("bulletIndex", 1)
        self.autoFire = config.get("autoFire", True)
        self.rect = self.image.get_rect()
        self.fireCounter = 0 # fire counter
        self.fireCounterMax = CONST.FPS / CONST.FIRE_SPEED # when fireCounter reach this, fire
        self.bullets = []
    
    def tick(self):
        if self.autoFire:
            # fire or not
            if self.fireCounter >= self.fireCounterMax:
                self.fireCounter = 0
                self.fire()
            self.fireCounter += 1

            # remove useless bullets
            self.bullets = [bullet for bullet in self.bullets if bullet.isValid() and (not bullet.isDead)]

            # bullet tick
            for bullet in self.bullets:
                bullet.tick()

        # draw
        self.game.screen.blit(self.image, self.rect)
    
    def fire(self):
        x = self.rect.centerx 
        y = 0
        if self.direction == CONST.UP:
            y = self.rect.top
        elif self.direction == CONST.DOWN:
            y = self.rect.bottom
        bullet = Bullet(self, x, y, self.direction, self.bulletIndex)
        self.bullets.append(bullet)

        global FIRE_SOUND
        if FIRE_SOUND is None:
            FIRE_SOUND = pygame.mixer.Sound("sound/fire.mp3")
            FIRE_SOUND.set_volume(0.1)
        FIRE_SOUND.play()