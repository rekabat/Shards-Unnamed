import pygame as pg
import math

import general as g

class Player:
	def __init__(self, position, zs, size= (1,1), img='art/player.png'):
		#####################################
		# Avatar info #######################
		#####################################

		#make a rect for where it is
		self.pos = g.tile2rect(position).topleft  #given in tile coordinates, convert to topleft pixel
		self.size = (size[0]*g.TILE_RES[0], size[1]*g.TILE_RES[1]) #given in tile size, convert to pixel size 
		self.rect= pg.Rect(self.pos, self.size)
		
		#what floor "level" is the player on
		self.zs = zs

		#the image of the player
		img = pg.image.load(img).convert_alpha() #loaded as facing up
		# art = pg.transform.scale(art, (100,100))

		#the image of the player facing in all directions
		self.udlrFacing = {                \
			"U": img,                           \
			"D": pg.transform.rotate(img, 180), \
			"L": pg.transform.rotate(img, 90),  \
			"R": pg.transform.rotate(img, 270)  }
		#the current direction the player is facing
		self.facing = "U"

		#the player defaulted to face forward
		self.art = self.udlrFacing[self.facing]

		#the directions the player is currently going
		self.udlr = [False, False, False, False]

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
		self.belt = Belt({ 	0: None, 
						1: None, 
						2: None, 
						3: None,
						4: None, 
						5: None, 
						6: None, 
						7: None }, #spells and potions currently chosen for battle + equipped weapon
						self.stats['hp'])
		self.equipped = {	"head":		None,	\
							"chest":	None,	\
							"legs":		None,	\
							"offhand":	None,	\
							"weapon":	None	} #currently equipped armor and weapons

		#####################################
		# Character info ####################
		#####################################
		
		
	def getRect(self): return self.rect
	def getArt(self): return self.art
	def getZs(self): return self.zs
	def getBelt(self): return self.belt
	def getName(self): return self.name
	def getDirectionFacing(self): return self.facing
	
	def getSortedInv(self):
		ret = {}
		for each in self.inv:
			ret.update({each.getType(): each})
		return ret
	
	def ifMoved(self, direction, dt):
		xmove = 0
		ymove = 0
		
		if "U" in direction:
			ymove-=(g.PX_STEP*dt)
		if "D" in direction:
			ymove+=(g.PX_STEP*dt)
		if "L" in direction:
			xmove-=(g.PX_STEP*dt)
		if "R" in direction:
			xmove+=(g.PX_STEP*dt)

		posPix = (self.pos[0]+xmove, self.pos[1]+ymove)
		return pg.Rect(posPix, self.size), posPix

	def move(self, rectTo, zs, posPix=None):
		self.rect = rectTo
		self.zs = zs
		if posPix is None:
			self.pos = rectTo.topleft
		else:
			self.pos = posPix
		
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
				self.art = self.udlrFacing["U"]
				self.facing = "U"
			if "D" in trn:
				self.art = self.udlrFacing["D"]
				self.facing = "D"
		elif "L" in trn:
			self.art = self.udlrFacing["L"]
			self.facing = "L"
		elif "R" in trn:
			self.art = self.udlrFacing["R"]
			self.facing = "R"
	
	def getTilePixInFrontOf(self): #players center + half a tile in the direction he faces
		ret = self.rect.center
		if   self.facing == "U": ret = (ret[0], ret[1]-g.TILE_RES[1])
		elif self.facing == "D": ret = (ret[0], ret[1]+g.TILE_RES[1])
		elif self.facing == "L": ret = (ret[0]-g.TILE_RES[0], ret[1])
		elif self.facing == "R": ret = (ret[0]+g.TILE_RES[0], ret[1])
		return ret
	
	def giveItem(self, item):
		self.inv.append(item)
	
	def takeItem(self, item):
		self.inv.remove(item)
	
	def takeHP(self, amt):
		self.stats['hp'] -= amt
		if self.stats['hp']<=0:
			return True
		self.belt.adjustCurrentHP(self.stats['hp'])
		return False
	
	def setBeltSlot(self, slot, set):
		self.getBelt().setBeltSlot(slot, set)
	
	def cast(self, slot, *args):
		return self.getBelt().cast(slot, *args)


class Belt:
	def __init__(self, eq, hp):
		self.eq = eq
		self.hp = hp
		self.img = self.genImg(eq, hp)
	
	def genImg(self, eq, hp):
		img = pg.Surface((g.TILE_RES[0]*10, g.TILE_RES[1]))

		#for the equipped items
		for i in range(10):
			if i is 4 or i is 5:
				pass
			else:
				if i<4:
					j=i
				elif i>5:
					j=i-2
				rect = pg.Rect((i*g.TILE_RES[1], 0), g.TILE_RES)

				if self.eq[j] is None:
					surf = pg.Surface(g.TILE_RES)
					surf.fill(g.WHITE)
				else:
					surf = self.eq[j].getImg()

				for x in range(g.TILE_RES[0]):
					for y in range(g.TILE_RES[1]):
						if (x == 0) or (y == 0) or (x == g.TILE_RES[0]-1) or (y == g.TILE_RES[1]-1):
							surf.set_at((x,y),g.BLACK)
				img.subsurface(rect).blit(surf, (0,0))
		
		self.img = img

		#for the health bar
		self.adjustCurrentHP(self.getTotalHP())

		return img
	
	def getImg(self): return self.img
	def getTotalHP(self): return self.hp
	
	def adjustCurrentHP(self, amt): # needs to be amt/total (not -amt)
		img = self.getImg()

		#make it all white
		dim = (g.TILE_RES[0]*2, g.TILE_RES[1])
		rect = pg.Rect((4*g.TILE_RES[1], 0), dim)
		surfw = pg.Surface(dim)
		surfw.fill(g.WHITE)

		#give it a red outline
		for x in range(g.TILE_RES[0]*2):
			for y in range(g.TILE_RES[1]):
					if (x == 0) or (y == 0) or (x == g.TILE_RES[0]*2-1) or (y == g.TILE_RES[1]-1):
						surfw.set_at((x,y), g.RED)

		#make part red
		width = (float(amt)/self.getTotalHP()) * g.TILE_RES[0]*2
		surfr = pg.Surface((width, g.TILE_RES[1]))
		surfr.fill(g.RED)
		x = (g.TILE_RES[0]*2 - width) / 2.
		surfw.blit(surfr, (x,0))

		img.subsurface(rect).blit(surfw, (0,0))
	
	def setBeltSlot(self, slot, set):
		if slot>7:
			raise KeyboardInterrupt("Belt slot out of range.")
		
		self.eq[slot]=set

		if slot >= 4:
			slot += 2

		self.img.blit(set.getIcon(), (slot*g.TILE_RES[1], 0))
	
	def cast(self, slot, *args):
		if self.eq[slot] is not None:
			return self.eq[slot].cast(*args)
		return False
		




