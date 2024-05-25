import objectbase
import time

class ZombieBase(objectbase.ObjectBase):
    def __init__(self, parent, id, pos):
        super(ZombieBase, self).__init__(parent, id, pos)

    def checkPosition(self):
        if time.time() - self.prePositionTime <= self.getPostionCD():
            return
        self.prePositionTime = time.time()
        self.pos[0] -= 2


