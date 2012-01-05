# Import pygame, locals, and initialize
import pygame as pg
from pygame.locals import *
pg.init()

import src.gameinterface

clock = pg.time.Clock()

def runGame():

    GI = src.gameinterface.GameInterface('play')
    
    while True:
        clock.tick(50)

        events = pg.event.get()
        if pg.QUIT in [each.type for each in events]:
            return
        else:
            GI.dispatch(events)

if __name__ == '__main__': runGame()