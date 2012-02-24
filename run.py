# Import pygame, locals, and initialize
import pygame as pg
from pygame.locals import *

pg.init()

import src.general as g
import src.gameinterface

clock = pg.time.Clock()

def runGame():

    GI = src.gameinterface.GameInterface('play')
    
    froze = False

    while True:
        dt = clock.tick(g.FRAME_RATE)
    	if froze:
    		dt = 1./g.FRAME_RATE

        events = pg.event.get()

        trash0, froze = GI.dispatch(events, dt/1000.)
        GI.renderView()

if __name__ == '__main__': runGame()