import pygame as pg
import mapParser

PX_STEP = 1

class Moveable:
	def __init__(self, map, position, size, art):
		#the map it's on
		self.map = map
		#give tile location
		self.position = map.tile2pix(position)
		#given in tile size
		self.size = (size[0]*map.getTileSize()[0], size[1]*map.getTileSize()[1])
		
		#the surface behind the moveable
		self.under = None
		
		#the image of the moveable
		self.art = pg.image.load(art).convert_alpha()
		
		#a call to place it on the map
		self.place(self.position)
		
	def place(self, position):
		newRect = pg.Rect((position[0]-self.size[0]*.5, position[1]-self.size[1]*.5),self.size)
		
		if self.map.get_rect().contains(newRect):
			if self.under != None:
				currentRect = pg.Rect((self.position[0]-self.size[0]*.5, self.position[1]-self.size[1]*.5),self.size)
				self.map.get().blit(self.under, currentRect)
			self.under = self.map.get().subsurface(newRect).copy()
			self.map.get().blit(self.art, newRect)
			self.position = position
			
			return True
		else:
			return False
	
	def move(self, direction):
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
		
		newPos = (self.position[0]+xmove, self.position[1]+ymove)
		if not self.map.blocked(newPos):
			self.place(newPos)

class Player(Moveable):
	def __init__(self, map, position, screen):
		Moveable.__init__(self, map, position, (1,1), 'art/player.png')
		self.screen = screen
		self.surface = self.map.get()
		self.lastGoodPixel = self.position
		
		self.moveFrame(self.position)
		
	
	def moveFrame(self, pixel):
		wh = self.screen.getWH()
		placing=pg.Rect(pixel[0]-wh[0]*.5, pixel[1]-wh[1]*.5, wh[0], wh[1])
		# print pixel[0]+wh[0]*.5, pixel[1]+wh[1]*.5
		print self.surface.get_rect(), placing, self.surface.get_rect().contains(placing)
		if self.surface.get_rect().contains(placing):
			self.screen.get().blit(self.surface.subsurface(placing), (0,0))
			pg.display.flip()
			return True
		return False
		
	
	def move(self, direction):
		Moveable.move(self, direction)

		if self.moveFrame(self.position):
			self.lastGoodPixel = self.position
		elif self.moveFrame((self.position[0], self.lastGoodPixel[1])):
			self.lastGoodPixel = (self.position[0], self.lastGoodPixel[1])
		elif self.moveFrame((self.lastGoodPixel[0], self.position[1])):
			self.lastGoodPixel = (self.lastGoodPixel[0], self.position[1])
		else:
			self.moveFrame(self.lastGoodPixel)