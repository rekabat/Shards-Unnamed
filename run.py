# Import pygame, locals, and initialize
import pygame as pg
from pygame.locals import *

pg.init()

import src.general as g
import src.gameinterface

clock = pg.time.Clock()

def runGame():

    GI = src.gameinterface.GameInterface('play')
    
    while True:
        clock.tick(g.FRAME_RATE)

        events = pg.event.get()

        GI.dispatch(events)
        GI.renderView()

if __name__ == '__main__': runGame()