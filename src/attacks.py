import pygame as pg

import general as g

class Attack:
	def __init__(self):
		self.duration = 0
		self.power = 0
		self.rect = pg.Rect((0,0), g.TILE_RES)
		self.img = None
		self.barimg = None
	
class sword(Attack):
	def __init__(self):#, **kwargs):
		Attack.__init__(self)#, **kwargs)
		# self.duration 

class fireball(Attack):
	def __init__(self):#, **kwargs):
		Attack.__init__(self)#, **kwargs)
		# self.duration 
		self.speed 		= 400 	#how fast it moves forward (pixels/second)
		self.distance 	= 5 	#how many tiles it goes forward
		self.img		= pg.image.load('art/player.png').convert_alpha()
	
	def cast(self, playerRect, direction):
		return fireball_cast(	
			playerRect.center, 	#start at player's center
			direction,			#the direction it travels
			self.speed,
			self.distance,
			self.img
			)
		
class fireball_cast(fireball):
	def __init__(self, start, dir, speed, distance, img):
		self.loc = start
		self.dir = dir
		self.speed = speed
		self.distance = distance
		self.img = img
		self.rect = self.tick(0)
	def tick(self, dt):
		self.distance -= self.speed*dt
		if self.distance<=0:
			return False #handle this by terminating the cast
		
		if self.dir=="U":
			self.loc = (self.loc[0]-self.speed*dt, self.loc[1])
		elif self.dir=="D":
			self.loc = (self.loc[0]+self.speed*dt, self.loc[1])
		elif self.dir=="L":
			self.loc = (self.loc[0], self.loc[1]-self.speed*dt)
		elif self.dir=="R":
			self.loc = (self.loc[0], self.loc[1]+self.speed*dt)
		
		self.rect = pg.Rect(self.loc, g.TILE_RES)

		return True




