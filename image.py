import pygame

class Image(pygame.sprite.Sprite):
    def __init__(self, parent, pathFmt, pathIndex, pos, size=None, pathIndexCount=0):
        super(Image, self).__init__()
        self.parent = parent
        self.pathFmt = pathFmt
        self.pathIndex = pathIndex
        self.pos = list(pos)
        self.size = size
        self.image = None
        self.pathIndexCount = pathIndexCount
        self.updateImage()
    
    def getAbsolutePos(self):
        pos = self.pos
        if self.parent:
            pos = (pos[0] + self.parent.pos[0], pos[1] + self.parent.pos[1] )
        return pos
    
    def updateImage(self):
        path = self.pathFmt
        if self.pathIndexCount != 0:
            path = path % self.pathIndex
        self.image = pygame.image.load(path)
        if self.size:
            self.image = pygame.transform.scale(self.image, self.size)
    
    def getRect(self):
        rect = self.image.get_rect()
        rect.x, rect.y = self.getAbsolutePos()
        return rect
    
    def updateIndex(self, pathIndex):
        self.pathIndex = pathIndex
        self.updateImage()

    def updateSize(self, size):
        self.size = size
        self.updateImage()

    def draw(self, surface):
        rect = self.image.get_rect()
        rect.x, rect.y = self.getAbsolutePos()
        surface.blit(self.image, rect)
    
    def update(self):
        pass
