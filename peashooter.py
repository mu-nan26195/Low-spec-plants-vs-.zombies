import random
import time
import peabullet
import objectbase
from const import *

class PeaShooter(objectbase.ObjectBase):
    def __init__(self, parent, id, pos):
        super(PeaShooter, self).__init__(parent, id, pos)
        self.hasShoot = False
        self.hasBullet = False

    def hasSummon(self):
        return self.hasBullet

    def preSummon(self):
        self.pathIndex = 0
        self.hasShoot = True
    
    def doSummon(self):
        if self.hasSummon():
            self.hasBullet = False
            return peabullet.PeaBullet(self, 3, (self.size[0]-20, 30))

    def checkImageIndex(self):
        if time.time() - self.preIndexTime <= self.getImageIndexCD():
            return
        self.preIndexTime = time.time()
        idx = self.pathIndex + 1
        if idx == 8:
            if self.hasShoot:
                self.hasBullet = True
        if idx >= self.pathIndexCount:
            idx = 9
        self.updateIndex(idx)

