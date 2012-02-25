import pygame as pg

import general as g

class Moveable:
	def __init__(self, position, zs, size, img):
		#make a rect for where it is
		self.pos = g.tile2rect(position).topleft  #given in tile coordinates, convert to topleft pixel
		self.size = (size[0]*g.TILE_RES[0], size[1]*g.TILE_RES[1]) #given in tile size, convert to pixel size 
		self.rect= pg.Rect(self.pos, self.size)
		
		#what floor "level" is the player on
		self.zs = zs

		#the image of the player
		img = pg.image.load(img).convert_alpha()

		#the image of the player facing in all directions
		img = {
			"D": img.subsurface(pg.Rect((0,0),              (self.size[0]*3, self.size[1]))),
			"L": img.subsurface(pg.Rect((0,1*self.size[1]), (self.size[0]*3, self.size[1]))),
			"R": img.subsurface(pg.Rect((0,2*self.size[1]), (self.size[0]*3, self.size[1]))),
			"U": img.subsurface(pg.Rect((0,3*self.size[1]), (self.size[0]*3, self.size[1])))  }

		self.udlrFacing = {}
		for k in img.keys():
			self.udlrFacing[k] = {
				1: img[k].subsurface(pg.Rect((0,0),self.size)).copy(),
				0: img[k].subsurface(pg.Rect((1*self.size[0],0),self.size)).copy(),
				2: img[k].subsurface(pg.Rect((1*self.size[0],0),self.size)).copy(),
				3: img[k].subsurface(pg.Rect((2*self.size[0],0),self.size)).copy()   }
		#the current direction the player is facing
		self.facing = "D"
		# The number of pixels stepped since last change in image
		self.pixStepped = 0
		#the number of pixels before the image is changed
		self.pixStepSize = 20
		# The surrent image (still, left foot, right foot)
		self.currentImg = 0

		#the player defaulted to face forward
		self.art = self.udlrFacing[self.facing][self.currentImg]

		#the directions the player is currently going
		self.udlr = [False, False, False, False]

	def getRect(self): return self.rect
	def getArt(self): return self.art
	def getZs(self): return self.zs
	def getDirectionFacing(self): return self.facing

	def ifMoved(self, direction, dt):
		xmove, ymove = 0, 0
		
		step = (g.PX_STEP*dt)

		if "U" in direction:
			if ("L" in direction) or ("R" in direction):
				ymove -= step**.5
			else:
				ymove -= step
		if "D" in direction:
			if ("L" in direction) or ("R" in direction):
				ymove += step**.5
			else:
				ymove += step
		if "L" in direction:
			if ("U" in direction) or ("D" in direction):
				xmove -= step**.5
			else:
				xmove -= step
		if "R" in direction:
			if ("U" in direction) or ("D" in direction):
				xmove += step**.5
			else:
				xmove += step

		posPix = (self.pos[0]+xmove, self.pos[1]+ymove)
		return pg.Rect(posPix, self.size), posPix

	def move(self, rectTo, zs, posPix=None):
		self.rect = rectTo
		self.zs = zs
		if posPix is None:
			self.pixStepped += g.distance(self.pos, rectTo.topleft)
			self.pos = rectTo.topleft
		else:
			self.pixStepped += g.distance(self.pos, posPix)
			self.pos = posPix

		while self.pixStepped >= self.pixStepSize:
			self.pixStepped -= self.pixStepSize
			self.currentImg = 0 if (self.currentImg == 3) else self.currentImg+1

			self.art = self.udlrFacing[self.facing][self.currentImg]
		
	def forgetMovement(self):
		self.udlr = [False, False, False, False]
	
	def movingDirection(self, dir):
		if   dir == "U": self.udlr[0] = True
		elif dir == "D": self.udlr[1] = True
		elif dir == "L": self.udlr[2] = True
		elif dir == "R": self.udlr[3] = True
	
	def stoppingDirection(self, dir):
		if   dir == "U": self.udlr[0] = False
		elif dir == "D": self.udlr[1] = False
		elif dir == "L": self.udlr[2] = False
		elif dir == "R": self.udlr[3] = False
	
	def overallDirection(self):
		dir = ""

		dir += "U" if self.udlr[0] else ""
		dir += "D" if self.udlr[1] else ""
		dir += "L" if self.udlr[2] else ""
		dir += "R" if self.udlr[3] else ""

		if ("U" in dir) and ("D" in dir): dir = dir.replace("U", "").replace("D", "")
		if ("L" in dir) and ("R" in dir): dir = dir.replace("L", "").replace("R", "")

		return dir
	
	def turn(self):
		trn = self.overallDirection()
		
		#in cases of diagonal, choose U or D
		for d in self.overallDirection():
			self.art = self.udlrFacing[d][self.currentImg]
			self.facing = d
			if (d == "U") or (d == "D"):
				break