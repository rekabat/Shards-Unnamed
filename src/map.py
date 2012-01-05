import pygame as pg
from pygame.locals import *

import worldEvents
import mapParser


class Map:
    def __init__(self, file):
        self.file = file + ".map"
        self.evtFile = file + ".evt"

        self.tileFile, self.tileSize, self.mapSize, self.setup = mapParser.parse(self.file)

        self.img = pg.Surface((self.mapSize[0]*self.tileSize[0], self.mapSize[1]*self.tileSize[1]))

        tm = mapParser.TileMap(self.tileFile, self.tileSize)
        we = worldEvents.parse(self.evtFile)

        for pos in self.setup.keys():
            mapParser.tileToMap(self.img, pos, tm.get(self.setup[pos].type()), self.tileSize)
        
        self.img_eventless = self.img.copy()
        
        for pos in self.setup.keys():
            if pos in we:
                mapSubsurface = self.img.subsurface(mapParser.tileRect(pos, self.tileSize))
                self.setup[pos].addEvents(we[pos], mapSubsurface)
                

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
            
    def triggerEvent(self, coords, pixel=True): # false means tile
        if pixel:
            return self.setup[self.pix2tile(coords)].triggerEvent()
        else:
            return self.setup[coords].triggerEvent()