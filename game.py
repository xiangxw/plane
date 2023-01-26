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
        pygame.display.set_caption("飞机大战(移动:WSAD)")
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
        # 删除被打中的敌机
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

        # 删除无用的敌机
        self.enemyList = [enemy for enemy in self.enemyList if enemy.isValid() and (not enemy.isDead)]

        # 刷新速度
        if self.newEnemySpeedRatioCounter > CONST.FPS:
            self.newEnemySpeedRatioCounter = 0
            self.newEnemySpeed += CONST.NEW_ENEMY_SPEED_RATIO
            self.newEnemyCounterMax = CONST.FPS / self.newEnemySpeed
        else:
            self.newEnemySpeedRatioCounter += 1

        # 刷新新的敌机
        if self.newEnemyCounter >= self.newEnemyCounterMax:
            self.newEnemyCounter = 0
            enemy = Enemy.genEnemy(self)
            self.enemyList.append(enemy)
        else:
            self.newEnemyCounter += 1
    
    def checkLife(self):
        # 检查与敌机的碰撞
        heroRect = self.hero.rect
        for enemy in self.enemyList:
            if enemy.rect.colliderect(heroRect):
                return False
        
        # TODO 检查与子弹的碰撞
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
        # 背景
        self.screen.blit(self.backgroundImage, (0, 0))
        
        # 显示fps
        if CONST.SHOW_FPS:
            fpsSurface = self.font.render(f"fps:{int(self.clock.get_fps())}", True, pygame.Color(125, 125, 125))
            fpsRect = fpsSurface.get_rect()
            fpsRect.topleft = (10, 10)
            self.screen.blit(fpsSurface, fpsRect)
        
        # 敌机刷新
        if not self.gameOver:
            self.refreshEnemy()

        # 敌机
        if not self.gameOver:
            for enemy in self.enemyList:
                enemy.tick()
        
        # hero
        if not self.gameOver:
            self.hero.tick()

        # 分数
        scoreSurface = self.font.render(f"分数:{self.score}", True, pygame.Color(125, 125, 125))
        scoreRect = scoreSurface.get_rect()
        scoreRect.topright = (self.screen.get_width() - 10, 10)
        self.screen.blit(scoreSurface, scoreRect)

        # 最高分
        maxScoreSurface = self.font.render(f"最高分:{self.maxScore}", True, pygame.Color(125, 125, 125))
        maxScoreRect = maxScoreSurface.get_rect()
        maxScoreRect.topright = (self.screen.get_width() - 10, 40)
        self.screen.blit(maxScoreSurface, maxScoreRect)

        # 游戏结束
        if self.gameOver:
            gameOverSurface = self.font.render("游戏结束", True, pygame.Color(255, 255, 255))
            gameOverRect = gameOverSurface.get_rect()
            gameOverRect.center = self.screen.get_rect().center
            self.screen.blit(gameOverSurface, gameOverRect)

        pygame.display.flip()

        if not self.gameOver and not self.checkLife():
            self.gameOver = True
            self.saveMaxScore()
            pygame.mixer.music.stop()