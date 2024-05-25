import objectbase
import time

class SunLight(objectbase.ObjectBase):
    def __init__(self, parent, id, pos):
        super(SunLight, self).__init__(parent, id, pos)

    def checkPosition(self):
        if time.time() - self.prePositionTime <= self.getPostionCD():
            return
        self.prePositionTime = time.time()
        
        if self.getAbsolutePos()[1] < 500:
            self.pos[1] += 2

