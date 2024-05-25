import image
import time

import random
import data_object
from const import *


class ObjectBase(image.Image):
    def __init__(self, parent, id, pos):
        self.id = id
        self.hp = self.getData()['HP']
        self.attack = self.getData()['ATT']
        self.preIndexTime = 0
        self.preSummonTime = 0
        self.prePositionTime = 0
        super(ObjectBase, self).__init__(parent, self.getData()['PATH'], 0, pos, self.getData()['SIZE'], self.getData()['IMAGE_INDEX_MAX'])
    
    def getData(self):
        return data_object.data[self.id]
    
    def getSummonCD(self):
        return self.getData()['SUMMON_CD']

    def getImageIndexCD(self):
        return self.getData()['IMAGE_INDEX_CD']
    
    def getPostionCD(self):
        return self.getData()['POSITION_CD']

    def canLoot(self):
        return self.getData()['CAN_LOOT']

    def getPrice(self):
        return self.getData()['PRICE']

    def isCollide(self, obj):
        return self.getRect().colliderect( obj.getRect() )
        
    def checkSummon(self):
        if time.time() - self.preSummonTime <= self.getSummonCD():
            return
        self.preSummonTime = time.time()
        self.preSummon()
    
    def checkImageIndex(self):
        if time.time() - self.preIndexTime <= self.getImageIndexCD():
            return
        self.preIndexTime = time.time()
        idx = self.pathIndex + 1
        if idx >= self.pathIndexCount:
            idx = 0
        self.updateIndex(idx)

    def update(self):
        self.checkSummon()
        self.checkImageIndex()
        self.checkPosition()

    def checkPosition(self):
        if time.time() - self.prePositionTime <= self.getPostionCD():
            return
        self.prePositionTime = time.time()

    def hasSummon(self):
        return False

    def preSummon(self):
        pass

    def doSummon(self):
        pass


