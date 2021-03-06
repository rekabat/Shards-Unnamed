import pygame as pg

from .general import Utils as g

class Text:
    def __init__(self, str, size, color=g.WHITE, antialiasing=True):
        self.str = str
        self.color = color
        self.size = size
        self.antialiasing = antialiasing

        self.img = pg.font.Font(None, self.size).render(self.str, self.antialiasing, self.color)

    def get(self):
        return self.img

    def getSize(self):
        return self.size

    def getStr(self):
        return self.str

    def getColor(self):
        return self.color

    def getAA(self):
        return self.antialiasing

    def getLength(self):
        return self.get().get_rect().width

    def place(self, surface, position, center=True):
        strSurface = self.get()
        if center:
            rect = strSurface.get_rect()
            rect.centerx = position[0]
            rect.centery = position[1]
            surface.blit(strSurface, rect)

            return rect
        else:
            surface.blit(strSurface, position)

            return 0

    def concatenate(self, texts):
        newStr = self.getStr()
        for each in texts:
            if each.getSize() != self.getSize():
                print("Error, text blocks different size, can not concatenate.")
                return False
            else:
                newStr += each.getStr()

        return Text(newStr, self.getSize(), self.getColor(), self.getAA())
