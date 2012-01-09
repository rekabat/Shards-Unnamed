import pygame as pg
from pygame.locals import *

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
        
        self.zsetup = {} #key is z, return is setup dict for that z. 
                        #key for setup dict is pos, returns is the tile there (at the given z)
        for pos in self.setup:
            for each in self.setup[pos]:
                drawOnZ = min(each.getZs())
                if drawOnZ not in self.zsetup.keys():
                    self.zsetup[drawOnZ] = []
                self.zsetup[drawOnZ].append(each)
        maxz = max(self.zsetup.keys())
        for z in range(maxz+1):
            if z not in self.zsetup.keys():
                self.zsetup[z] = []
        


        for pos in self.setup:
            self.setup[pos] = self.setup[pos][0]

        #a dict whose key is z and the return is the image of this z and all those belowed it layered
        self.layersOfAndBelow = self.makeLayersOfAndBelow()
        #a dict whose key is z and the return is the image of this z and all those above it layered 
        self.layersOfAndAbove = self.makeLayersOfAndAbove()
    
    def makeLayersOfAndBelow(self):
        ret = {}

        zimg = pg.Surface(self.mapSizePx, SRCALPHA, 32)
        zs = self.zsetup.keys()
        zs.sort()
        
        for z in zs:
            for tile in self.zsetup[z]:
                zimg.blit(tile.getArt(), tile.getRect())
            ret[z]=zimg.copy()
        
        return ret

    def makeLayersOfAndAbove(self):
        ret = {}

        zs = self.zsetup.keys()
        zs.sort()
        zs = zs[::-1]

        maxz = max(zs)
        ret[maxz] = pg.Surface(self.mapSizePx, SRCALPHA, 32)
        for tile in self.zsetup[maxz]:
            ret[maxz].blit(tile.getArt(), tile.getRect())
        
        for z in zs[1:]:
            ret[z] = pg.Surface(self.mapSizePx, SRCALPHA, 32)
            for tile in self.zsetup[z]:
                ret[z].blit(tile.getArt(), tile.getRect())
            ret[z].blit(ret[z+1], (0,0))
        
        return ret

    def getImageOfAndBelowZ(self, z, partial = False):
        if z not in self.layersOfAndBelow.keys():
            return False
        
        if not partial:
            return self.layersOfAndBelow[z]
        else:
            return self.layersOfAndBelow[z].subsurface(partial)
    
    def getImageOfAndAboveZ(self, z, partial = False):
        if z not in self.layersOfAndAbove.keys():
            return False
        
        if not partial:
            return self.layersOfAndAbove[z]
        else:
            return self.layersOfAndAbove[z].subsurface(partial)

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
    
    def getZs(self):
        return self.Z
    
    def getRect(self):
        return self.rect