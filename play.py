import random
import time

import pygame as pg
from pygame.locals import *
pg.init()

import src.display      as display
import src.text         as text
import src.mapParser    as mapParser
import src.moveables    as moveables

def main():
    screen = display.Display()
    screen.createDisplay()

    theMap = mapParser.Map('maps/mapgen_map')

    currentPx =theMap.tile2pix((12,10))
    player = moveables.Player(theMap, (12, 10), screen)

    up, down, left, right = False, False, False, False

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            
            elif event.type == pg.KEYDOWN:
                key = event.dict['key']
                if key == pg.K_w:
                    up = True
                if key == pg.K_s:
                    down = True
                if key == pg.K_a:
                    left = True
                if key == pg.K_d:
                    right = True
            
            elif event.type == pg.KEYUP:
                key = event.dict['key']
                if key == pg.K_w:
                    up = False
                if key == pg.K_s:
                    down = False
                if key == pg.K_a:
                    left = False
                if key == pg.K_d:
                    right = False
        
        mv = ""
        mv += "U" if up else ""
        mv += "D" if down else ""
        mv += "L" if left else ""
        mv += "R" if right else ""

        player.move(mv)

        pg.time.Clock().tick()

if __name__ == '__main__': main()