import pygame as pg

#important constant
TILE_RES = (32, 32) #the width and hight of tiles in pixels
# PX_STEP = 200 #pixels/second
FRAME_RATE = 60 #Frames per second

#easy references
WHITE=(255,255,255)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
BLACK=(0,0,0)



#useful functions

#gets the rect given tile coordinates
def tile2rect((x, y)):
	return pg.Rect((x * TILE_RES[0], y * TILE_RES[1]), TILE_RES)

def pix2tile((x,y)):
	return (int(x/TILE_RES[0]), int(y/TILE_RES[1]))

def tile2pix((x, y), center = True): #center pixel
	if center:
		return (int((x+.5)*TILE_RES[0]), int((y+.5)*TILE_RES[1]))
	else:
		return (int(x*TILE_RES[0]), int(y*TILE_RES[1]))

def pix2tile2rect((x,y)):
	return tile2rect(pix2tile((x,y)), TILE_RES)

def distance(point1, point2):
	return ((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)**.5