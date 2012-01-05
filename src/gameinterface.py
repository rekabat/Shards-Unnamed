import pygame as pg
from pygame.locals import *

import display
import map
import moveables

TILE_RES = (32,32)
class GameInterface:
    def __init__(self, state="main-menu"):
        self.display = display.Display()
        self.map = None
        self.player = None

        self.state = state
        if state == "main-menu":
            print "Not quite there yet"
        elif state == "play":
            self.createWorld()
        
    def createWorld(self):
        self.map = map.Map('maps/mapgen_map')
        self.player = moveables.Player(self.map, (12, 10), self.display)
    
    def dispatch(self, events):
        if self.state == "main-menu":
            pass

        elif self.state == "play":
            for event in events:
                if event.type == pg.KEYDOWN:
                    key = event.dict['key']
                    if key == pg.K_w:
                        self.player.udlr[0] = True
                    if key == pg.K_s:
                        self.player.udlr[1] = True
                    if key == pg.K_a:
                        self.player.udlr[2] = True
                    if key == pg.K_d:
                        self.player.udlr[3] = True
                
                elif event.type == pg.KEYUP:
                    key = event.dict['key']
                    if key == pg.K_w:
                        self.player.udlr[0] = False
                    if key == pg.K_s:
                        self.player.udlr[1] = False
                    if key == pg.K_a:
                        self.player.udlr[2] = False
                    if key == pg.K_d:
                        self.player.udlr[3] = False
            
            mv = ""
            mv += "U" if self.player.udlr[0] else ""
            mv += "D" if self.player.udlr[1] else ""
            mv += "L" if self.player.udlr[2] else ""
            mv += "R" if self.player.udlr[3] else ""

            returnedWE = self.player.move(mv)

        elif self.state == "pause":
            pass
