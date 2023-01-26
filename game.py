import os
import sys
import pygame
from pygame.locals import Rect, Color, QUIT
from hero import Hero
from enemy import Enemy
import const as CONST

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load("sound/bgm.mp3")
        self.bombSound = pygame.mixer.Sound("sound/bomb.mp3")
        pygame.display.set_caption("Plane(press WSAD to move)")
        self.screen = pygame.display.set_mode((480, 680))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("kaiti", 24)
        self.backgroundImage = pygame.image.load("images/background.png").convert_alpha()
        self.newEnemyCounter = 0
        self.newEnemySpeedRatioCounter = 0
        self.newEnemySpeed = CONST.NEW_ENEMY_SPEED
        self.newEnemyCounterMax = CONST.FPS / self.newEnemySpeed

        self.hero = Hero(self)
        self.enemyList = []
        self.gameOver = False
        self.score = 0
        self.maxScore = 0

        self.readMaxScore()

    def start(self):
        pygame.mixer.music.play(-1)
        while True:
            self.handleEvent()
            self.tick()
            self.clock.tick(CONST.FPS)
    
    def handleEvent(self):
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                sys.exit()
        if not self.gameOver:
            self.hero.handleEvent(events)
    
    def refreshEnemy(self):
        # delete hited enemy
        for bullet in self.hero.bullets:
            if bullet.isDead: continue
            bulletRect = bullet.rect
            for enemy in self.enemyList:
                if (not enemy.isDead) and bulletRect.colliderect(enemy.rect):
                    bullet.setDead(True)
                    enemy.setDead(True)
                    self.bombSound.play()
                    self.score += 1
                    if self.score > self.maxScore:
                        self.maxScore = self.score
                    break

        # remove useless enemies
        self.enemyList = [enemy for enemy in self.enemyList if enemy.isValid() and (not enemy.isDead)]

        # refresh speed
        if self.newEnemySpeedRatioCounter > CONST.FPS:
            self.newEnemySpeedRatioCounter = 0
            self.newEnemySpeed += CONST.NEW_ENEMY_SPEED_RATIO
            self.newEnemyCounterMax = CONST.FPS / self.newEnemySpeed
        else:
            self.newEnemySpeedRatioCounter += 1

        # gen new enemies
        if self.newEnemyCounter >= self.newEnemyCounterMax:
            self.newEnemyCounter = 0
            enemy = Enemy.genEnemy(self)
            self.enemyList.append(enemy)
        else:
            self.newEnemyCounter += 1
    
    def checkLife(self):
        # check collide with enemies
        heroRect = self.hero.rect
        for enemy in self.enemyList:
            if enemy.rect.colliderect(heroRect):
                return False
        
        return True
    
    def readMaxScore(self):
        score = 0
        if os.path.exists(CONST.FILE_PATH):
            with open(CONST.FILE_PATH, 'r') as f:
                try:
                    score = int(f.read())
                except:
                    pass
        self.maxScore = score
    
    def saveMaxScore(self):
        with open(CONST.FILE_PATH, 'w') as f:
            f.write(str(self.maxScore))


    def tick(self):
        # background
        self.screen.blit(self.backgroundImage, (0, 0))
        
        # show fps
        if CONST.SHOW_FPS:
            fpsSurface = self.font.render(f"fps:{int(self.clock.get_fps())}", True, pygame.Color(125, 125, 125))
            fpsRect = fpsSurface.get_rect()
            fpsRect.topleft = (10, 10)
            self.screen.blit(fpsSurface, fpsRect)
        
        # gen enemies
        if not self.gameOver:
            self.refreshEnemy()

        # enemy tick
        if not self.gameOver:
            for enemy in self.enemyList:
                enemy.tick()
        
        # hero
        if not self.gameOver:
            self.hero.tick()

        # score
        scoreSurface = self.font.render(f"Score:{self.score}", True, pygame.Color(125, 125, 125))
        scoreRect = scoreSurface.get_rect()
        scoreRect.topright = (self.screen.get_width() - 10, 10)
        self.screen.blit(scoreSurface, scoreRect)

        # top score
        maxScoreSurface = self.font.render(f"Top Score:{self.maxScore}", True, pygame.Color(125, 125, 125))
        maxScoreRect = maxScoreSurface.get_rect()
        maxScoreRect.topright = (self.screen.get_width() - 10, 40)
        self.screen.blit(maxScoreSurface, maxScoreRect)

        # game over
        if self.gameOver:
            gameOverSurface = self.font.render("Game Over", True, pygame.Color(255, 255, 255))
            gameOverRect = gameOverSurface.get_rect()
            gameOverRect.center = self.screen.get_rect().center
            self.screen.blit(gameOverSurface, gameOverRect)

        pygame.display.flip()

        if not self.gameOver and not self.checkLife():
            self.gameOver = True
            self.saveMaxScore()
            pygame.mixer.music.stop()