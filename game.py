import random
import pygame
import data_object
from const import *

import image
import sunflower
import zombiebase
import peashooter

class Game(object):
    def __init__(self, surface):
        self.surface = surface
        self.goldFont = pygame.font.Font(None, 60)
        self.gold = 100
        self.zombieFont = pygame.font.Font(None, 60)
        self.zombie = 0
        self.back = image.Image(None, PATH_BACK, None, (0,0), GAME_SIZE)
        self.plants = []
        self.zombies = []
        self.summons = []

        self.hasPlant = []
        for i in range(GRID_SIZE[0]):
            col = []
            for j in range(GRID_SIZE[1]):
                col.append(0)
            self.hasPlant.append(col)

        for i in range(GRID_COUNT[1]):
            self.addZombie(13, i)

    def update(self):
        self.back.update()
        for plant in self.plants:
            plant.update()
            if plant.hasSummon():
                sum = plant.doSummon()
                if sum:
                    self.summons.append(sum)

        for zombie in self.zombies:
            zombie.update()
        
        for summon in self.summons:
            summon.update()

        self.checkSummonVSZombie()
        self.checkZombieVSPlant()

    def checkSummonVSZombie(self):
        for summon in self.summons:
            for zombie in self.zombies:
                if summon.isCollide(zombie):
                    self.fight(summon, zombie)
                    if zombie.hp <= 0:
                        self.zombies.remove(zombie)
                        self.zombie += 1
                    if summon.hp <= 0:
                        self.summons.remove(summon)
                    return 
    
    def checkZombieVSPlant(self):
        for zombie in self.zombies:
            for plant in self.plants:
                if zombie.isCollide(plant):
                    self.fight(zombie, plant)
                    if zombie.hp <= 0:
                        self.zombies.remove(zombie)
                        self.zombie += 1
                    if plant.hp <= 0:
                        self.plants.remove(plant)
                    return 
    
    def fight(self, a, b):
        while True:
            a.hp -= b.attack
            b.hp -= a.attack
            if b.hp <= 0:
                return True
            if a.hp <= 0:
                return False
        return False

    def draw(self):
        self.back.draw(self.surface)
        for plant in self.plants:
            plant.draw(self.surface)
        for zombie in self.zombies:
            zombie.draw(self.surface)
        for summon in self.summons:
            summon.draw(self.surface)

        textImage = self.goldFont.render("Gold: " + str(self.gold), True, (0,0,0))
        self.surface.blit(textImage, (13, 23))
        textImage = self.goldFont.render("Gold: " + str(self.gold), True, (255,255,255))
        self.surface.blit(textImage, (10, 20))

        textImage = self.zombieFont.render("Score: " + str(self.zombie), True, (0,0,0))
        self.surface.blit(textImage, (13, 83))
        textImage = self.zombieFont.render("Score: " + str(self.zombie), True, (255,255,255))
        self.surface.blit(textImage, (10, 80))

    def getIndexByMousePos(self, mousePos):
        x = (mousePos[0] - LEFT_TOP[0]) // GRID_SIZE[0]
        y = (mousePos[1] - LEFT_TOP[1]) // GRID_SIZE[1]
        return x, y
    
    def addSunFlower(self, x, y):
        if self.hasPlant[x][y] == 1:
            return
        self.hasPlant[x][y] = 1
        pos = (x * GRID_SIZE[0] + LEFT_TOP[0], y * GRID_SIZE[1] + LEFT_TOP[1])
        sf = sunflower.SunFlower(self.back, 0, pos)
        self.plants.append( sf )
    
    def addPeaShooter(self, x, y):
        if self.hasPlant[x][y] == 1:
            return
        self.hasPlant[x][y] = 1
        pos = (x * GRID_SIZE[0] + LEFT_TOP[0], y * GRID_SIZE[1] + LEFT_TOP[1])
        ps = peashooter.PeaShooter(self.back, 1, pos)
        self.plants.append( ps )
    
    def addZombie(self, x, y):
        pos = (x * GRID_SIZE[0] + LEFT_TOP[0], y * GRID_SIZE[1] + LEFT_TOP[1])
        ps = zombiebase.ZombieBase(self.back, 4, pos)
        self.zombies.append( ps )

    def checkLoot(self, mousePos):
        for summon in self.summons:
            if not summon.canLoot():
                continue
            rect = summon.getRect()
            if rect.collidepoint(mousePos):
                self.summons.remove(summon)
                self.gold += summon.getPrice()
                return True
        return False
    
    def checkAddPlant(self, mousePos, plantId):
        x, y = self.getIndexByMousePos(mousePos)
        if 0 <= x < GRID_SIZE[0] and 0 <= y < GRID_SIZE[1]:
            if self.hasPlant[x][y] == 0:
                if self.gold >= data_object.data[plantId]['PRICE']:
                    self.gold -= data_object.data[plantId]['PRICE']
                    if plantId == SUN_FLOWER_IDX:
                        self.addSunFlower(x, y)
                    elif plantId == PEA_SHOOTER_IDX:
                        self.addPeaShooter(x, y)

    def mouseClickHandler(self, btnType):
        mousePos = pygame.mouse.get_pos()
        if btnType == 1:
            if not self.checkLoot(mousePos):
                self.checkAddPlant(mousePos, SUN_FLOWER_IDX)
        else:
            self.checkAddPlant(mousePos, PEA_SHOOTER_IDX)
            
