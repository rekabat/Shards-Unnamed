import pygame as pg

import general as g

class Moveable:
	def __init__(self, position, z, size, img, pixStep=.20):
		self.size = (size[0]*g.TILE_RES[0], size[1]*g.TILE_RES[1]) #given in tile size, convert to pixel size 

		#make a rect for where it is
		self.pos = None #g.tile2rect(position).topleft  #given in tile coordinates, convert to topleft pixel
		self.rect = None #pg.Rect(self.pos, self.size)
		self.previousRect = None #self.rect.copy()
		# self.fourCorners = None
		
		#what floor "level" is the player on
		self.z = None #zs

		self.setPlace(position, z) #sets pos,rect,previousrect,zs

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
				0: img[k].subsurface(pg.Rect((0,0),self.size)).copy(),
				1: img[k].subsurface(pg.Rect((1*self.size[0],0),self.size)).copy(),
				2: img[k].subsurface(pg.Rect((0,0),self.size)).copy(),
				3: img[k].subsurface(pg.Rect((2*self.size[0],0),self.size)).copy()   }

		self.udlrFacing_outline = {}
		for d in self.udlrFacing:
			tempDict = {}
			for s in self.udlrFacing[d]:
				tempDict[s] = g.makeOutlinedArt(self.udlrFacing[d][s], g.BLUE)
			self.udlrFacing_outline[d]=tempDict

		#the current direction the player is facing
		self.facing = "D"
		# The number of pixels stepped since last change in image
		self.pixStepped = 0
		self.previousPixStepped = 0
		#the number of pixels before the image is changed
		self.pixStepSize = 20
		#the number of pixels traversed in a millisecond
		self.pixStep = pixStep + 0
		# The surrent image (still, left foot, right foot)
		self.currentImg = 0

		#the player defaulted to face forward
		self.art = (self.udlrFacing[self.facing][self.currentImg], self.udlrFacing_outline[self.facing][self.currentImg])
		self.previousArt = self.art

		#the directions the player is currently going
		self.udlr = [False, False, False, False]

	def getRect(self): return self.rect
	# def getFourCorners(self): return self.fourCorners
	def getArt(self, outline = False):
		if outline: return self.art[1]
		else: return self.art[0]
	def getZ(self): return self.z
	def getDirectionFacing(self): return self.facing
	def getPosition(self): return self.pos

	def setPlace(self, position, z):
		#make a rect for where it is
		self.pos = g.tile2rect(position).topleft  #given in tile coordinates, convert to topleft pixel
		self.rect= pg.Rect(self.pos, self.size)
		# self.fourCorners = (self.rect.topleft, self.rect.topright, self.rect.bottomleft, self.rect.bottomright)
		self.previousRect = self.rect.copy()
		
		#what floor "level" is the player on
		self.z = z

	def setZ(self, z): self.z = z

	def move(self, mv, dt, forceTurn = False):
		self.previousRect = self.getRect().copy()

		xmove, ymove = 0, 0
		
		step = (self.pixStep*dt)

		direction = mv

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

		self.pos = (self.pos[0]+xmove, self.pos[1]+ymove)

		self.previousPixStepped = self.pixStepped+0
		self.pixStepped += g.distance(self.pos, self.rect.topleft)

		self.rect =  pg.Rect(self.pos, self.size)


		if forceTurn:
			x, y = self.getRect().center
			x = x - forceTurn[0]
			y = y - forceTurn[1]
			if abs(x)>abs(y):
				if x>0:
					trn = "L"
				else:
					trn = "R"
			else:
				if y>0:
					trn = "U"
				else:
					trn = "D"
		else:
			trn = self.overallDirection()
		
		#in cases of diagonal, choose U or D
		for d in trn:
			self.art = (self.udlrFacing[d][self.currentImg], self.udlrFacing_outline[d][self.currentImg])
			self.facing = d
			if (d == "U") or (d == "D"):
				break

		while self.pixStepped >= self.pixStepSize:
			self.pixStepped -= self.pixStepSize
			self.currentImg = 0 if (self.currentImg == 3) else self.currentImg+1
			self.previousArt = (self.art[0], self.art[1])
			self.art = (self.udlrFacing[self.facing][self.currentImg], self.udlrFacing_outline[self.facing][self.currentImg])
	
	def undoMove(self):
		self.rect = self.previousRect.copy()
		# self.z = self.oldZ
		# self.fourCorners = (self.rect.topleft, self.rect.topright, self.rect.bottomleft, self.rect.bottomright)
		self.pos = self.rect.topleft
		if self.previousPixStepped > self.pixStepped:
			self.art = (self.previousArt[0], self.previousArt[1])
			self.currentImg = 3 if (self.currentImg == 0) else self.currentImg-1
		self.pixStepped = self.previousPixStepped
		
		
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