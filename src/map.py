import pygame as pg
from pygame.locals import *

import worldEvents
import mapParser

TILE_RES = (32, 32)

class Map:
    def __init__(self, file):
        self.file = file + ".map"
        self.evtFile = file + ".evt"

        mapData = mapParser.genMap(file)

        self.tileFile = mapData['tileFile']
        self.tileSize = mapData['tileSize']
        self.mapSize = mapData['mapSize']
        self.setup = mapData['setup']
        self.img = mapData['img']
        self.img_eventless = mapData['img_eventless']

    def get(self):
        return self.img
    
    def get_eventless(self):
        return self.img_eventless
    
    def get_rect(self):
        return self.img.get_rect()
    
    def tile2pix(self,(x, y)):
        if x > self.mapSize[0] or y > self.mapSize[1] or x < 0 or y < 0:
            print "out of bounds"
            raise KeyboardInterrupt
        # print (x+.5), self.tileSize[0], (y+.5), self.tileSize[1], int((x+.5)*self.tileSize[0]), int((y+.5)*self.tileSize[1])
        return (int((x+.5)*self.tileSize[0]), int((y+.5)*self.tileSize[1]))
    
    def pix2tile(self,(x,y)):
        return (int(x/self.tileSize[0]), int(y/self.tileSize[1]))
    
    def getTileSize(self):
        return self.tileSize
    
    def getTile(self, coords, pixel=True): #false means tile
        if pixel:
            return self.setup[self.pix2tile(coords)]
        else:
            return self.setup[coords]
    
    def blocked(self, coords, pixel=True): #false means tile
        if pixel:
            return self.setup[self.pix2tile(coords)].blocked()
        else:
            return self.setup[coords].blocked()
    
    def hasEvent(self, coords, pixel=True): # false means tile
        if pixel:
            return self.setup[self.pix2tile(coords)].hasEvent()
        else:
            return self.setup[coords].hasEvent()
    
    def passEvents(self, coords, pixel=True): # false means tile
        if pixel:
            return self.setup[self.pix2tile(coords)].passEvents()
        else:
            return self.setup[coords].passEvents()
    

    def hasEventNear(self, rect):
        corners = [rect.topleft, rect.bottomleft, rect.topright, rect.bottomright]
        closeTiles = [self.pix2tile(each) for each in corners]
        closeTiles.remove(self.pix2tile(rect.center))

        return self.hasEvent(closeTiles[0], False) or \
            self.hasEvent(closeTiles[1], False) or \
            self.hasEvent(closeTiles[2], False)
            