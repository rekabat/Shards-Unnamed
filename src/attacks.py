import pygame as pg

import general as g

class Attack:
	def __init__(self, **kwargs):
		# self.rect = pg.Rect((0,0), g.TILE_RES)
		# self.img = None
		# self.img_icon = None
		self.alignment = kwargs["alignment"]
		self.user = kwargs["user"]

		self.cooldown = 1000	#ms before the spell can be re-cast
		self.timeSinceLastCast = None

	def getRect(self): return self.rect
	def getImg(self): return self.img
	def getIcon(self): return self.img_icon
	def getAlignment(self): return self.alignment

	def cast(self):
		if self.timeSinceLastCast is None:
			if self.user.useShards(self.cost):
				self.timeSinceLastCast = 0
				return True
			else:
				return False
		else:
			return False

	def tick(self, dt):
		if self.timeSinceLastCast is None:
			return False

		self.timeSinceLastCast += dt
		if self.timeSinceLastCast >= self.cooldown:
			self.timeSinceLastCast = None
			return 0

		return 1 - self.timeSinceLastCast / float(self.cooldown)

	def hit(self, target): pass



class sword(Attack):
	def __init__(self, **kwargs):
		Attack.__init__(self, **kwargs)
		# self.duration 

class icefield(Attack):
	def __init__(self, **kwargs):
		Attack.__init__(self, **kwargs)

		self.cost		= (10,0,0,0)
		self.duration 	= 3000			#how long it lasts (ms)
		self.shift_rate = .004				#how often it shifts (ms^-1)
		self.size 		= 2 			#size of the square ((size*2+1)^2 tiles)
		self.img_icon	= pg.image.load('art/attacks/icefield_icon.png').convert_alpha()

		img				= pg.image.load('art/attacks/icefield.png').convert_alpha()
		self.img 		= pg.Surface((g.TILE_RES[0]*(self.size*2+1), g.TILE_RES[1]*(self.size*2+1)), pg.SRCALPHA, 32)
		for i in range(self.size*2+1):
			for j in range(self.size*2+1):
				self.img.blit(img, (i*g.TILE_RES[0],j*g.TILE_RES[1]))
	
	def cast(self, *args): #playerRect, direction
		if Attack.cast(self):
				return icefield_cast(	
					args[0].topleft,	#start at player's center
					self.duration,
					self.shift_rate,
					self.size,
					self.img,
					self.alignment
					)


class icefield_cast(icefield):
	def __init__(self, start, duration, shift_rate, size, img, alignment):
		self.dur = duration
		self.shift_rate = shift_rate
		self.size = size
		self.img = img
		self.alignment = alignment

		self.timeSinceCast = 0
		self.rect = pg.Rect((start[0]-self.size*g.TILE_RES[0], start[1]-self.size*g.TILE_RES[1]), (g.TILE_RES[0]*(size*2+1), g.TILE_RES[1]*(size*2+1)))
		
		self.alreadyTouched = []

	def tick(self, dt):
		self.timeSinceCast += dt
		if self.timeSinceCast > self.dur:
			return False #handle this by terminating the cast
		if int((self.timeSinceCast-dt)*self.shift_rate) < int((self.timeSinceCast)*self.shift_rate):
			self.img = pg.transform.rotate(self.img, 90)
		return True

	def hit(self, target):
		if target.getAlignment() != self.alignment:
			if target not in self.alreadyTouched:
				self.alreadyTouched.append(target)
				target.takeHP(1)

class fireball(Attack):
	def __init__(self, **kwargs):
		Attack.__init__(self, **kwargs)
		
		self.cost		= (4,0,0,0)

		self.speed 		= .4 			#how fast it moves forward (pixels/ms)
		self.distance 	= 5*g.TILE_RES[0] 	#how many tiles it goes forward
		img		= pg.image.load('art/attacks/fireball.png').convert_alpha()
		self.img = {                \
			"U": img,                           \
			"D": pg.transform.rotate(img, 180), \
			"L": pg.transform.rotate(img, 90),  \
			"R": pg.transform.rotate(img, 270)  }
		self.img_icon	= pg.image.load('art/attacks/fireball_icon.png').convert_alpha()
	
	def cast(self, *args): #playerRect, direction):
		if Attack.cast(self):
				return fireball_cast(	
					args[0].topleft,	#start at player's center
					args[1],			#the direction it travels
					self.speed,
					self.distance,
					self.img,
					self.alignment
					)
class fireball_cast(fireball):
	def __init__(self, start, dir, speed, distance, img, alignment):
		self.loc = start
		self.dir = dir
		self.speed = speed
		self.distance = distance
		self.img = img
		self.alignment = alignment
		self.rect = None
		self.tick(0)

		self.alreadyTouched = []

	def getImg(self): return self.img[self.dir]

	def tick(self, dt):
		self.distance -= self.speed*dt
		if self.distance<=0:
			return False #handle this by terminating the cast
		
		if self.dir=="U":
			self.loc = (self.loc[0], self.loc[1]-self.speed*dt)
		elif self.dir=="D":
			self.loc = (self.loc[0], self.loc[1]+self.speed*dt)
		elif self.dir=="L":
			self.loc = (self.loc[0]-self.speed*dt, self.loc[1])
		elif self.dir=="R":
			self.loc = (self.loc[0]+self.speed*dt, self.loc[1])
		
		self.rect = pg.Rect(self.loc, g.TILE_RES)

		return True

	def hit(self, target):
		if target.getAlignment() != self.alignment:
			if target not in self.alreadyTouched:
				self.alreadyTouched.append(target)
				target.takeHP(1)




