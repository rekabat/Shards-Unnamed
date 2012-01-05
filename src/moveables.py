import pygame as pg
import mapParser

PX_STEP = 1

class Moveable:
	def __init__(self, map, position, size, art):
		#the map it's on
		self.map = map
		#the map it's on's surface
		self.mapSurface = map.get()
		#the map it's on's surface without events
		self.mapSurface_eventless = map.get_eventless()
		
		#make a rect for where it is
		size = (size[0]*map.getTileSize()[0], size[1]*map.getTileSize()[1]) #given in tile size, convert to pixel size 
		position = map.tile2pix(position) #given in tile coordinates, convert to pixel
		self.rect= pg.Rect((position[0]-size[0]*.5, position[1]-size[1]*.5), size)
		
		# print self.rect
		
		#the image of the moveable
		self.art = pg.image.load(art).convert_alpha()
		
		#the surface behind the moveable
		self.under = self.mapSurface.subsurface(self.rect).copy()
		#a call to place it on the map, which also sets self.under
		self.place(self.rect)
		
	def place(self, newRect, eventless_map=False):
		if self.mapSurface.get_rect().contains(newRect):
			if eventless_map:
				self.under = self.mapSurface_eventless.subsurface(self.rect).copy()
				self.mapSurface.blit(self.under, self.rect) ######COMMENT OUT FOR FUN TIMES!
				self.under = self.mapSurface_eventless.subsurface(newRect).copy()
			else:
				self.mapSurface.blit(self.under, self.rect) ######COMMENT OUT FOR FUN TIMES!
				self.under = self.mapSurface.subsurface(newRect).copy()
			self.mapSurface.blit(self.art, newRect)
			self.rect = newRect
			
			return True
		else:
			print "Warning: Player wants to leave the map."
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
		
		newRect = self.rect.copy()
		newRect.centerx += xmove
		newRect.centery += ymove
		
		#########################################
		#########################################
		# implement sliding along borders
		#########################################
		#########################################
	
		if self.cornersBlocked(newRect):
			if len(direction)>1:
				for each in direction:
					self.move(each)
		else:
			return self.place(newRect)
	
	#########################################
	#########################################
	# Maybe change back to 1 and implement sliding towards passages
	#########################################
	#########################################
	
	def cornersBlocked(self, rect):
		smallerRect = rect.copy()
		smallerRect.width  *= .9
		smallerRect.height *= .9
		return \
			self.map.blocked(smallerRect.topleft)    or \
			self.map.blocked(smallerRect.topright)   or \
			self.map.blocked(smallerRect.bottomleft) or \
			self.map.blocked(smallerRect.bottomright)

class Player(Moveable):
	def __init__(self, map, position, screen):
		Moveable.__init__(self, map, position, (1,1), 'art/player.png')

		self.screen = screen
		self.lastGoodPixel = self.rect.center
		self.moveFrame(self.lastGoodPixel)
		self.udlr = [False, False, False, False]
		
	
	def moveFrame(self, pixel):
		wh = self.screen.getWH()
		placing=pg.Rect(pixel[0]-wh[0]*.5, pixel[1]-wh[1]*.5, wh[0], wh[1])
		if self.mapSurface.get_rect().contains(placing):
			self.screen.get().blit(self.mapSurface.subsurface(placing), (0,0))
			pg.display.flip()
			return True
		return False
		
	
	def move(self, direction):
		
		ret = Moveable.move(self, direction)

		if self.moveFrame(self.rect.center):
			self.lastGoodPixel = self.rect.center
		elif self.moveFrame((self.rect.centerx, self.lastGoodPixel[1])):
			self.lastGoodPixel = (self.rect.centerx, self.lastGoodPixel[1])
		elif self.moveFrame((self.lastGoodPixel[0], self.rect.centery)):
			self.lastGoodPixel = (self.lastGoodPixel[0], self.rect.centery)
		else:
			self.moveFrame(self.lastGoodPixel)
		
		return ret
	
	def place(self, rect, use_eventless=False):
		if Moveable.place(self, rect, use_eventless):
			if self.map.hasEvent(rect.center):
				worldEvents = self.map.passEvents(rect.center)
				# Moveable.place(self, rect, True)
				return worldEvents
		