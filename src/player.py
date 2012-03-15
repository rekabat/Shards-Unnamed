import pygame as pg

import general as g
import moveables

class Player(moveables.Moveable):
	def __init__(self, position, zs, font, size= (1,1), img='art/playersprite.png'): #font is used for belt
		moveables.Moveable.__init__(self, position, zs, size, img)

		#####################################
		# Character info ####################
		#####################################

		self.name = "Bartholomew"
		self.stats = {	'lvl': 	0,
						'hp': 	10,
						'def': 	1,
						'mag': 	1,
						'atk': 	1	} #stats
		self.curStats = {'lvl': 0,
						'hp': 	10,
						'def': 	1,
						'mag': 	1,
						'atk': 	1	} #current stats

		self.inv = [] #armor, weapons, potions, shards, runes, misc
		self.shards = {"odic": 200, "cosmic": 20, "aether": 20, "occult": 1}
			#odic represents life, human, plant, animal, or otherwise -> given by the gods
			#cosmic is the middle ground, between mortal life and the immortal heavens
			#aether is the energy of the heavens and immortals
			#occult is a mystery, a strange form of energy with great power
		self.focuses = [] #all available spells for crafting
		self.belt = Belt(self.shards,
						{0: None, 1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None}, #focuses currently chosen for battle + equipped weapon
						self.stats['hp'],
						font)
		self.equipped = {	"head":		None,	\
							"chest":	None,	\
							"legs":		None,	\
							"offhand":	None,	\
							"weapon":	None	} #currently equipped armor and weapons
		self.alignment = 0

		#####################################
		# Character info ####################
		#####################################
		
	def getBelt(self): return self.belt
	def getName(self): return self.name
	def getAlignment(self): return self.alignment
	def getStat(self, stat): return self.stats[stat]
	def getCurStat(self, stat): return self.curStats[stat]
	
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
		self.curStats['hp'] -= amt
		if self.curStats['hp'] <= 0:
			return True
		self.belt.adjustCurrentHP(self.curStats['hp'])
		return False

	def useShards(self, amt):
		self.shards["odic"] 	-= amt[0]
		if self.shards["odic"] < 0:
			self.shards["odic"] 	+= amt[0]
			return False
		self.shards["cosmic"] 	-= amt[1]
		if self.shards["cosmic"] < 0:
			self.shards["cosmic"] 	+= amt[0]
			return False
		self.shards["aether"] 	-= amt[2]
		if self.shards["aether"] < 0:
			self.shards["aether"] 	+= amt[0]
			return False
		self.shards["occult"] 	-= amt[3]
		if self.shards["occult"] < 0:
			self.shards["occult"] 	+= amt[0]
			return False

		self.belt.adjustCurrentShards(self.shards)
		return True
	
	def setBeltSlot(self, slot, set):
		self.getBelt().setBeltSlot(slot, set)
	
	def cast(self, slot, *args):
		return self.getBelt().cast(slot, *args)

	def tick(self, dt):
		self.belt.tick(dt)


class Belt:
	def __init__(self, sh, eq, hp, font):
		# self.sh = sh #shards
		self.eq = eq #equipped focuses
		self.hp = hp #total hp

		self.font = font

		self.shardTypes = {0: "Odic", 1:"Cosmic", 2:"Aether", 3:"Occult"}

		self.shardPanel = None
		self.hpPanel = None
		self.img = self.genImg(sh, eq, hp)
	
	def genImg(self, sh, eq, hp):
		img = pg.Surface((g.TILE_RES[0]*10, g.TILE_RES[1]*2))

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
		self.hpPanel = pg.Surface((g.TILE_RES[0]*2, g.TILE_RES[1]))
		self.hpPanel.fill(g.WHITE)
		g.giveBorder(self.hpPanel, g.BLACK, 1)
		self.adjustCurrentHP(self.getTotalHP())

		#for the shard totals
		self.shardPanel = pg.Surface((10*g.TILE_RES[0]/4., g.TILE_RES[1]))
		self.shardPanel.fill((100,100,95))
		g.giveBorder(self.shardPanel, g.BLACK, 1)
		self.adjustCurrentShards(sh)

		return img
	
	def getImg(self): return self.img
	def getTotalHP(self): return self.hp
	
	def adjustCurrentHP(self, amt): # needs to be amt/total (not -amt)
		surfw = self.hpPanel.copy()

		#make red rectangle surface
		width = (float(amt)/self.getTotalHP()) * (g.TILE_RES[0]*2-2) #the two is the black pixel border
		surfr = pg.Surface((width, g.TILE_RES[1]-2))
		surfr.fill(g.RED)

		#put it on the white surface
		surfw.blit(surfr, (1,1))

		#put new hp on the belt
		self.getImg().blit(surfw, (4*g.TILE_RES[1], 0))
	
	def adjustCurrentShards(self, sh):

		y = g.TILE_RES[1]	
		for i in range(4):
			x = i*10*g.TILE_RES[0]/4.

			surfc = self.shardPanel.copy()

			texttop = self.font.text(self.shardTypes[i]+":", 15)
			textbot = self.font.text(str(sh[self.shardTypes[i].lower()]), 15)

			surfc.blit(texttop.get(), (1,1))
			surfc.blit(textbot.get(), (1,16))
			self.img.blit(surfc, (x,y))


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
	
	def tick(self, dt):
		for each in self.eq:
			fraction = self.eq[each].tick(dt)
			if fraction:
				surf = pg.Surface((g.TILE_RES[0], g.TILE_RES[1]*fraction))
				surf.fill(g.BLACK)
				surf.set_alpha(200)

				icon = self.eq[each].getIcon().copy()
				icon.blit(surf, (0,0))

				slot = each+0
				if slot >= 4:
					slot += 2

				self.img.blit(icon, (g.TILE_RES[0]*slot, 0))




