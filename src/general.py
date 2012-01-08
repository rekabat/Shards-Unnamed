import pygame as pg

#important constant
TILE_RES = (32, 32) #the width and hight of tiles in pixels
PX_STEP = 3 #The size steps all moving things take in pixels

#easy references
WHITE=(255,255,255)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
BLACK=(0,0,0)



#useful functions

#gets the rect given tile coordinates
def tile2rect((x, y), squareSize):
	return pg.Rect((x * squareSize[0], y * squareSize[1]), squareSize)

