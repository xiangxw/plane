import random
from aggressive import Aggressive
import const as CONST

class Enemy(Aggressive):
    @classmethod
    def genEnemy(cls, game):
        config = {
            "direction": CONST.DOWN,
            "image": "images/enemy1.png",
            "bulletIndex": 2,
            "enemySpeed": 2,
            "autoFire": False,
        }
        return cls(game, config)

    def __init__(self, game, config):
        super(Enemy, self).__init__(game, config)
        self.rect.left = random.randint(0, game.screen.get_width() - self.rect.width)
        self.rect.bottom = 0
        self.enemySpeed = config.get("enemySpeed", 2)
        self.isDead = False
    
    def setDead(self, dead):
        self.isDead = dead
    
    def tick(self):
        if self.direction == CONST.DOWN:
            self.rect.top += self.enemySpeed
        elif self.direction == CONST.UP:
            self.rect.top -= self.enemySpeed
        super(Enemy, self).tick()
    
    def isValid(self):
        if self.direction == CONST.DOWN:
            return self.rect.top < self.game.screen.get_height()
        elif self.direction == CONST.UP:
            return self.rect.bottom > 0
        return True