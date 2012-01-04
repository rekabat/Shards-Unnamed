import pygame as pg
import mapParser

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
		if direction == "U":
			self.place((self.position[0], self.position[1]-1))
		if direction == "D":
			self.place((self.position[0], self.position[1]+1))
		if direction == "L":
			self.place((self.position[0]-1, self.position[1]))
		if direction == "R":
			self.place((self.position[0]+1, self.position[1]))

class Player(Moveable):
	def __init__(self, map, position, screen):
		Moveable.__init__(self, map, position, (1,1), 'art/player.png')
		self.screen = screen
		self.surface = self.map.get()
		
		self.updateFrame(self.position)
		
	
	def updateFrame(self, pixel):
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
		if direction == "U":
			if self.place((self.position[0], self.position[1]-1)):
				self.updateFrame(self.position)
		if direction == "D":
			if self.place((self.position[0], self.position[1]+1)):
				self.updateFrame(self.position)
		if direction == "L":
			if self.place((self.position[0]-1, self.position[1])):
				self.updateFrame(self.position)
		if direction == "R":
			if self.place((self.position[0]+1, self.position[1])):
				self.updateFrame(self.position)