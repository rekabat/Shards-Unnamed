import pygame as pg
import general as g

class Player:
	def __init__(self, position, z, size= (1,1), art='art/player.png'):
	# def __init__(self, position, size= (1,1), art='art/blog200812.png'):
		#make a rect for where it is
		size = (size[0]*g.TILE_RES[0], size[1]*g.TILE_RES[1]) #given in tile size, convert to pixel size 
		position = ((position[0]+.5)*g.TILE_RES[0], (position[1]+.5)*g.TILE_RES[1]) #given in tile coordinates, convert to pixel
		self.rect= pg.Rect((position[0]-size[0]*.5, position[1]-size[1]*.5), size)\
		
		#what floor "level" is the player on
		self.z = z

		#the image of the player
		art = pg.image.load(art).convert_alpha() #loaded as facing up

		#the image of the player facing in all directions
		self.udlrFacing = (                \
			art,                           \
			pg.transform.rotate(art, 180), \
			pg.transform.rotate(art, 90),  \
			pg.transform.rotate(art, 270)  )
		#the player defaulted to face forward
		self.art = self.udlrFacing[0]

		#the directions the player is currently going
		self.udlr = [False, False, False, False]


		self.name = "Bartholomew"
	
	def getRect(self):
		return self.rect
		
	def getArt(self):
		return self.art
	
	def ifMoved(self, direction):
		xmove = 0
		ymove = 0
		
		if "U" in direction:
			ymove-=g.PX_STEP
		if "D" in direction:
			ymove+=g.PX_STEP
		if "L" in direction:
			xmove-=g.PX_STEP
		if "R" in direction:
			xmove+=g.PX_STEP
		
		newRect = self.rect.copy()
		newRect.centerx += xmove
		newRect.centery += ymove
		
		return newRect
	
	def move(self, rectTo):
		self.rect = rectTo

	def goodFrameRect(self):
		wh = self.screen.getWH()
		return pg.Rect(self.lastGoodPixel[0]-wh[0]*.5, self.lastGoodPixel[1]-wh[1]*.5, wh[0], wh[1])
	
	def forgetMovement(self):
		self.udlr = [False, False, False, False]
	
	def movingDirection(self, dir):
		if dir == "U":
			self.udlr[0] = True
		elif dir == "D":
			self.udlr[1] = True
		elif dir == "L":
			self.udlr[2] = True
		elif dir == "R":
			self.udlr[3] = True
	
	def stoppingDirection(self, dir):
		if dir == "U":
			self.udlr[0] = False
		elif dir == "D":
			self.udlr[1] = False
		elif dir == "L":
			self.udlr[2] = False
		elif dir == "R":
			self.udlr[3] = False
	
	def overallDirection(self):
		dir = ""
		dir += "U" if self.udlr[0] else ""
		dir += "D" if self.udlr[1] else ""
		dir += "L" if self.udlr[2] else ""
		dir += "R" if self.udlr[3] else ""
		return dir
	
	def turn(self):
		trn = self.overallDirection()

		#ignore having both up and down or both left and right
		if ("U" in trn) and ("D" in trn):
			trn.replace("U", "")
			trn.replace("D", "")
		if ("L" in trn) and ("R" in trn):
			trn.replace("L", "")
			trn.replace("R", "")
		
		#in cases of diagonal, choose U or D
		if ("U" in trn) or ("D" in trn):
			if "U" in trn:
				self.art = self.udlrFacing[0]
			if "D" in trn:
				self.art = self.udlrFacing[1]
		elif "L" in trn:
			self.art = self.udlrFacing[2]
		elif "R" in trn:
			self.art = self.udlrFacing[3]

		
	
	def getName(self):
		return self.name