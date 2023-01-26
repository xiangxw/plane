import pygame
import const as CONST

class Bullet:
    imageMap = {}
    def __init__(self, parent, x, y, direction, imageIndex = 1):
        self.parent = parent
        self.direction = direction
        self.image = Bullet.getImageByIndex(imageIndex)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        if direction == CONST.UP:
            self.rect.top = y
        elif direction == CONST.DOWN:
            self.rect.bottom = y
        self.isDead = False
    
    def setDead(self, dead):
        self.isDead = dead
    
    def isValid(self):
        if self.direction == CONST.UP:
            return self.rect.bottom > 0
        elif self.direction == CONST.DOWN:
            return self.rect.top < self.parent.game.screen.get_height()
        return True

    def tick(self):
        if self.direction == CONST.UP:
            self.rect.centery -= CONST.BULLET_SPEED
        elif self.direction == CONST.DOWN:
            self.rect.centery += CONST.BULLET_SPEED 
        self.parent.game.screen.blit(self.image, self.rect)
    
    @classmethod
    def getImageByIndex(cls, index):
        image = cls.imageMap.get(index)
        if not image:
            image = pygame.image.load(f"images/bullet{index}.png").convert_alpha()
            cls.imageMap[index] = image
        return image