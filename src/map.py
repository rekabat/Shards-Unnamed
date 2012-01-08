import pygame as pg
from pygame.locals import *

# import worldEvents
import mapParser
import general as g

class Map:
    def __init__(self, file):
        self.file = file + ".map"
        self.evtFile = file + ".evt"

        mapData = mapParser.parse(file)

        self.mapSizeTiles = mapData['mapSize']
        self.mapSizePx = mapData['mapSizePx']
        self.setup = mapData['setup']
    
    def getMapSizePx(self):
        return self.mapSizePx
    
    def getTile(self, coords, pixel=True): #false means tile
        if pixel:
            return self.setup[g.pix2tile(coords)]
        else:
            return self.setup[coords]
    
    def blocked(self, rect):#coords, pixel=True): #false means tile
        return self.setup[g.pix2tile(rect.topleft)    ].blocked() or \
               self.setup[g.pix2tile(rect.topright)   ].blocked() or \
               self.setup[g.pix2tile(rect.bottomleft) ].blocked() or \
               self.setup[g.pix2tile(rect.bottomright)].blocked()
    
    def getTilesInRect(self, rect):
        tl = g.pix2tile(rect.topleft)
        br = g.pix2tile(rect.bottomright)

        ret = []

        i = tl[0]
        while i<=br[0] and i<self.mapSizeTiles[0]:
            j = tl[1]
            while j<=br[1] and j<self.mapSizeTiles[1]:
                ret.append(self.setup[(i,j)])
                j+=1
            i+=1
                
        return ret

class Tile:
    def __init__(self, source, posOnTileFile, blocked, z, pos):
        self.Source = source
        self.PosOnTileFile = posOnTileFile
        self.art = None
        self.Blocked = blocked
        self.Z = z
        self.rect = g.tile2rect(pos)
    
    def source(self):
        return self.Source

    def type(self):
        return self.PosOnTileFile
    
    def setArt(self, art):
        self.art = art

    def getArt(self):
        return self.art

    def blocked(self):
        return self.Blocked
    
    def z(self):
        return self.Z
    
    def getRect(self):
        return self.rect