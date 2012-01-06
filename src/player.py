import pygame as pg

TILE_RES = (32,32)
PX_STEP = 1

class Player:
	def __init__(self, position, size= (1,1), art='art/player.png', art_excited='art/playerredline.png'):
		#make a rect for where it is
		size = (size[0]*TILE_RES[0], size[1]*TILE_RES[1]) #given in tile size, convert to pixel size 
		position = ((position[0]+.5)*TILE_RES[0], (position[1]+.5)*TILE_RES[1]) #given in tile coordinates, convert to pixel
		self.rect= pg.Rect((position[0]-size[0]*.5, position[1]-size[1]*.5), size)\
		
		#the image of the player
		self.art = pg.image.load(art).convert_alpha()
		self.art_excited = pg.image.load(art_excited).convert_alpha()

		self.lastGoodPixel = self.rect.center

		self.udlr = [False, False, False, False]
	
	def getRect(self):
		return self.rect
		
	def getArt(self):
		return self.art
	
	def ifMoved(self, direction):
		xmove = 0
		ymove = 0
		
		if "U" in direction:
			ymove-=PX_STEP
		if "D" in direction:
			ymove+=PX_STEP
		if "L" in direction:
			xmove-=PX_STEP
		if "R" in direction:
			xmove+=PX_STEP
		
		newRect = self.rect.copy()
		newRect.centerx += xmove
		newRect.centery += ymove
		
		return newRect
	
	def move(self, rectTo):
		self.rect = rectTo

	def goodFrameRect(self):
		wh = self.screen.getWH()
		return pg.Rect(self.lastGoodPixel[0]-wh[0]*.5, self.lastGoodPixel[1]-wh[1]*.5, wh[0], wh[1])