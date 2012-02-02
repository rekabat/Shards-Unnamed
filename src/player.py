import pygame as pg
import general as g

class Player:
	def __init__(self, position, zs, size= (1,1), art='art/player.png'):
		#####################################
		# Avatar info #######################
		#####################################

		#make a rect for where it is
		size = (size[0]*g.TILE_RES[0], size[1]*g.TILE_RES[1]) #given in tile size, convert to pixel size 
		position = ((position[0]+.5)*g.TILE_RES[0], (position[1]+.5)*g.TILE_RES[1]) #given in tile coordinates, convert to pixel
		self.rect= pg.Rect((position[0]-size[0]*.5, position[1]-size[1]*.5), size)\
		
		#what floor "level" is the player on
		self.zs = zs

		#the image of the player
		art = pg.image.load(art).convert_alpha() #loaded as facing up
		# art = pg.transform.scale(art, (100,100))

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

		#the current direction the player is facing
		self.facing = "U"

		#####################################
		# Avatar info #######################
		#####################################




		#####################################
		# Character info ####################
		#####################################

		self.name = "Bartholomew"
		self.stats = {	'lvl': 	0,	\
						'hp': 	10,	\
						'def': 	1,	\
						'mag': 	1,	\
						'atk': 	1	} #stats
		self.inv = [] #armor, weapons, potions, shards, runes, misc
		self.spells = [] #all available spells for crafting
		self.belt = {} #spells and potions currently chosen for battle + equipped weapon
		self.equipped = {	"head":		None,	\
							"chest":	None,	\
							"legs":		None,	\
							"offhand":	None,	\
							"weapon":	None	} #currently equipped armor and weapons

		#####################################
		# Character info ####################
		#####################################
		
		
	def getRect(self):
		return self.rect
		
	def getArt(self):
		return self.art
	
	def getZs(self):
	 	return self.zs
	
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
	
	def move(self, rectTo, zs):
		self.rect = rectTo
		self.zs = zs
	
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
				self.facing = "U"
			if "D" in trn:
				self.art = self.udlrFacing[1]
				self.facing = "D"
		elif "L" in trn:
			self.art = self.udlrFacing[2]
			self.facing = "L"
		elif "R" in trn:
			self.art = self.udlrFacing[3]
			self.facing = "R"

	def getTileOn(self):
		return g.pix2tile(self.getRect().center)
	
	def getTileInFrontOf(self):
		on = self.getTileOn()
		if self.facing == "U":
			inFrontOf = (on[0], on[1]-1)
		elif self.facing == "D":
			inFrontOf = (on[0], on[1]+1)
		elif self.facing == "L":
			inFrontOf = (on[0]-1, on[1])
		elif self.facing == "R":
			inFrontOf = (on[0]+1, on[1])
		
		return inFrontOf
	
	def getName(self):
		return self.name
	
	def giveItem(self, item):
		self.inv.append(item)
	
	def takeItem(self, item):
		self.inv.remove(item)
	
	def getSortedInv(self):
		ret = {}
		for each in self.inv:
			ret.update({each.getType(): each})
		return ret