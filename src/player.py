import pygame as pg
import math

import general as g
import moveables

class Player(moveables.Moveable):
	def __init__(self, position, zs, size= (1,1), img='art/playersprite.png'):
		moveables.Moveable.__init__(self, position, zs, size, img)

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
		
	def getBelt(self): return self.belt
	def getName(self): return self.name
	
	def getSortedInv(self):
		ret = {}
		for each in self.inv:
			ret.update({each.getType(): each})
		return ret
	
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
						surfw.set_at((x,y), g.BLACK)

		#make red rectangle surface
		width = (float(amt)/self.getTotalHP()) * (g.TILE_RES[0]*2-2) #the two is the black pixel border
		surfr = pg.Surface((width, g.TILE_RES[1]-2))
		surfr.fill(g.RED)

		#put it on the white surface
		surfw.blit(surfr, (1,1))

		#put new hp on the belt
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
		




