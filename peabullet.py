import objectbase
import time

class PeaBullet(objectbase.ObjectBase):
    def __init__(self, parent, id, pos):
        super(PeaBullet, self).__init__(parent, id, pos)

    def checkPosition(self):
        if time.time() - self.prePositionTime <= self.getPostionCD():
            return
        self.prePositionTime = time.time()
        self.pos[0] += 3


        


