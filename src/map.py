import pygame as pg
from pygame.locals import *

import mapParser
import general as g

class Map:
    def __init__(self, file, screenres):
        self.screenres = screenres
        self.file = file + ".map"
        self.evtFile = file + ".evt"

        mapData = mapParser.parse(file)

        self.mapSizeTiles = mapData['mapSize']
        self.mapSizePx = mapData['mapSizePx']

        if self.screenres[0] > self.mapSizePx[0]:
            x = int((self.screenres[0]-self.mapSizePx[0])/2.)
            w = self.screenres[0]
        else:
            x = 0
            w = self.mapSizePx[0]
        if self.screenres[1] > self.mapSizePx[1]:
            y = int((self.screenres[1]-self.mapSizePx[1])/2.)
            h = self.screenres[1]
        else:
            y=0
            h = self.mapSizePx[1]
        self.drawingSize = (w,h)
        self.mapDrawingDif = (x,y)
        self.mapRectOnImg = pg.Rect((x,y), self.mapSizePx)


        self.setup = mapData['setup']
        
        self.zsetup = {} #key is z, return is a list of tiles on that z level
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
        
        self.zsetup2 = {} #key is z, return is setup dict for that z. 
                        #key for setup dict is pos, returns is the tile there (at the given z)
        for pos in self.setup:
            for each in self.setup[pos]:
                for drawOnZ in each.getZs():
                    if drawOnZ not in self.zsetup2.keys():
                        self.zsetup2[drawOnZ] = {}
                    self.zsetup2[drawOnZ][pos] = each
        maxz = max(self.zsetup2.keys())
        for z in range(maxz+1):
            if z not in self.zsetup2.keys():
                self.zsetup2[z] = {}


        for pos in self.setup:
            self.setup[pos] = self.setup[pos][0]

        #a dict whose key is z and the return is the image of this z and all those belowed it layered
        self.layersOfAndBelow = self.makeLayersOfAndBelow()
        #a dict whose key is z and the return is the image of this z and all those above it layered 
        self.layersOfAndAbove = self.makeLayersOfAndAbove()

    def getMapSizePx(self): return self.mapSizePx
    def getMapSizeTiles(self): return self.mapSizeTiles
    def getDrawingSize(self): return self.drawingSize
    def getMapDrawingDif(self): return self.mapDrawingDif
    
    def makeLayersOfAndBelow(self):
        ret = {}

        img = pg.Surface(self.drawingSize)
        zimg = img.subsurface(self.mapRectOnImg)

        # zimg = pg.Surface(self.mapSizePx, SRCALPHA, 32)
        zs = self.zsetup.keys()
        zs.sort()
        
        for z in zs:
            for tile in self.zsetup[z]:
                zimg.blit(tile.getArt(), tile.getRect())
            ret[z]=img.copy()
        
        return ret

    def makeLayersOfAndAbove(self):
        ret = {}

        zs = self.zsetup.keys()
        zs.sort()
        zs = zs[::-1]

        maxz = max(zs)

        # ret[maxz] = pg.Surface(self.mapSizePx, SRCALPHA, 32)
        # for tile in self.zsetup[maxz]:
            # ret[maxz].blit(tile.getArt(), tile.getRect())
        # for z in zs[1:]:
            # ret[z] = pg.Surface(self.mapSizePx, SRCALPHA, 32)
            # for tile in self.zsetup[z]:
                # ret[z].blit(tile.getArt(), tile.getRect())
            # ret[z].blit(ret[z+1], (0,0))
        
        ret[maxz] = pg.Surface(self.drawingSize, SRCALPHA, 32)
        img = ret[maxz].subsurface(self.mapRectOnImg)
        for tile in self.zsetup[maxz]:
            img.blit(tile.getArt(), tile.getRect())

        for z in zs[1:]:
            ret[z] = pg.Surface(self.drawingSize, SRCALPHA, 32)
            img = ret[z].subsurface(self.mapRectOnImg)
            for tile in self.zsetup[z]:
                img.blit(tile.getArt(), tile.getRect())
            img.blit(ret[z+1].subsurface(self.mapRectOnImg), (0,0))
            
            

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
    
    def pix2tile(self, pix):
        return g.pix2tile((pix[0]-self.mapDrawingDif[0], pix[1]-self.mapDrawingDif[1]))
    def tile2rect(self, (x,y)):
        return pg.Rect((x * g.TILE_RES[0] + self.mapDrawingDif[0], y * g.TILE_RES[1] + self.mapDrawingDif[1]), g.TILE_RES)

    def getTile(self, coords, z, pixel=True): #false means tile
        if pixel:
            coords = g.pix2tile(coords)
        # print coords
        if coords in self.zsetup2[z].keys():
            return self.zsetup2[z][coords]
        else:
            return False
    
    def blocked(self, rect, zlist):#coords, pixel=True): #false means tile
        corners = (g.pix2tile(rect.topleft), \
            g.pix2tile(rect.topright), \
            g.pix2tile(rect.bottomleft), \
            g.pix2tile(rect.bottomright) )
        ret = True
        for z in zlist:
            blockedAtThisZ = False
            for corner in corners:
                try: #if a tile exists at this z and IS blocked, return true
                    bl = self.zsetup2[z][corner].blocked()
                    blockedAtThisZ = blockedAtThisZ or bl
                except: #if a tile doesn't exist at this z, return true (it is blocked here)
                    blockedAtThisZ = True
                    break
            ret = ret and blockedAtThisZ
        return ret

    
    def tileExists(self,rect,zlist):
        corners = (g.pix2tile(rect.topleft), \
            g.pix2tile(rect.topright), \
            g.pix2tile(rect.bottomleft), \
            g.pix2tile(rect.bottomright) )
        for z in zlist:
            for corner in corners:
                if corner not in self.zsetup2[z].keys():
                    return False
        return True

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
        self.Z = z #list
        self.rect = g.tile2rect(pos)
    
    def source(self): return self.Source
    def type(self): return self.PosOnTileFile
    def getArt(self): return self.art
    def blocked(self): return self.Blocked
    def getZs(self): return self.Z
    def getRect(self): return self.rect
    
    def setArt(self, art):
        self.art = art