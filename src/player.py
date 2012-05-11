import pygame as pg

import general as g
import moveables

class Player(moveables.Moveable):
	def __init__(self, position, z, font, screenwidth, size= (1,1), img='art/playersprite.png'): #font is used for belt
		moveables.Moveable.__init__(self, position, z, size, img)

		#####################################
		# Character info ####################
		#####################################

		self.name = "Bartholomew"
		self.stats = {	'lvl': 	1,
						'hp': 	10,
						'odic': 	1,
						'cosmic': 	1,
						'aether': 	1,
						'occult':	1,	} #stats
		self.curStats = {'lvl':		1,
						'hp': 		10,
						'odic': 	1,
						'cosmic': 	1,
						'aether': 	1,
						'occult':	1,	} #current stats
		self.experience = {	'odic':		0,
							'cosmic':	0,
							'aether':	0,
							'occult':	0}

		self.inv = [] #armor, weapons, potions, shards, runes, misc

		self.shards = {"odic": 20, "cosmic": 200, "aether": 20, "occult": 1}
		'''
			odic represents life, human, plant, animal, or otherwise -> given by the gods
			cosmic is the middle ground, between mortal life and the immortal heavens
			aether is the energy of the heavens and immortals
			occult is a mystery, a strange form of energy with great power
		'''
		self.cosmic_timer = 0 # a timer in ms for the regneration of cosmic shards (see tick)

		self.focuses = [] #all available spells for casting
		self.belt = Belt(self.shards,
						{0: None, 1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None, 8:None}, #focuses currently chosen for battle + equipped weapon, 8 belongs to sword
						self.stats['hp'],
						self.curStats['hp'],
						font,
						screenwidth)
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

	def setStat(self, stat, val): self.stats[stat] = val
	def setCurStat(self, stat, val): self.curStats[stat] = val
	
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

	def giveFocus(self, focus):
		self.focuses.append(focus)
	
	def takeHP(self, amt):
		self.curStats['hp'] -= amt
		if self.curStats['hp'] <= 0:
			return True
		self.belt.adjustCurrentHP(self.curStats['hp'])
		return False

	def giveExperience(self, amt):
		self.experience['odic'] 	+= amt[0]
		self.experience['cosmic'] 	+= amt[1]
		self.experience['aether'] 	+= amt[2]
		self.experience['occult'] 	+= amt[3]

		for each in self.experience:
			'''
			possible fomulas:
				modified "fast" pokemon -> .8 * (5 + self.getStat(each))**3 - 100
			'''
			if self.experience[each] > .8 * (5 + self.getStat(each))**3 - 100:
				self.setStat(each, self.getStat(each)+1)
				self.setCurStat(each, self.getCurStat(each)+1)
				print each, "has leveled up."
				if (self.getStat('odic')+self.getStat('cosmic')+self.getStat('aether')+self.getStat('occult'))%5 == 0:
					self.setStat("lvl", self.getStat("lvl")+1)
					self.setCurStat("lvl", self.getCurStat("lvl")+1)
					print "leveled up!!!"

		# print self.experience

	def useShards(self, amt):
		if 	(self.shards["odic"] 	>= amt[0]) and \
			(self.shards["cosmic"] 	>= amt[1]) and \
			(self.shards["aether"] 	>= amt[2]) and \
			(self.shards["occult"] 	>= amt[3]) :

				self.shards["odic"]		-= amt[0]
				self.shards["cosmic"] 	-= amt[1]
				self.shards["aether"] 	-= amt[2]
				self.shards["occult"] 	-= amt[3]
				self.belt.adjustCurrentShards(self.shards)

				self.giveExperience(amt)

				return True
		else:
			return False

	def giveShards(self, amt):
		self.shards["odic"]		+= amt[0]
		self.shards["cosmic"] 	+= amt[1]
		self.shards["aether"] 	+= amt[2]
		self.shards["occult"] 	+= amt[3]
		self.belt.adjustCurrentShards(self.shards)
	
	def equip(self, slot, set):
		self.getBelt().equip(slot, set)
	
	def cast(self, slot, *args):
		return self.getBelt().cast(slot, *args)

	def tick(self, dt):
		# max cosmic = cosmic_lvl*20+180
		# recharge rate = max cosmic / 10,000 ms

		maxCosmic = (self.getStat("cosmic")*20+180)

		self.cosmic_timer += dt
		ms_toGetA_shard = int(30000 / maxCosmic)

		cosToGet = self.cosmic_timer // ms_toGetA_shard
		self.cosmic_timer = self.cosmic_timer % ms_toGetA_shard

		toMax = maxCosmic - self.shards["cosmic"]
		if toMax != 0:
			if toMax < cosToGet:
				cosToGet = toMax
			self.giveShards((0, int(cosToGet), 0, 0))

		self.belt.tick(dt)


class Belt:
	def __init__(self, curShards, eq, hp, curHP, font, screenwidth):
		# self.sh = sh #shards
		self.eq = eq #equipped focuses
		self.hp = hp #total hp

		self.curShards = curShards
		self.curHP = curHP

		self.font = font

		self.screenW = screenwidth
		self.scaledTile = (int(self.screenW*.4/8.), int(self.screenW*.4/8.))
		# 8 scaled tiles for skills, 4 for hp bar, 8 for shards 

		self.shardTypes = {0: "Odic", 1:"Cosmic", 2:"Aether", 3:"Occult"}

		self.shardPanel = None
		self.hpPanel = None
		# self.spellPanel = None
		self.img = None
		self.genImg()
	
	def genImg(self):
		self.img = pg.Surface( (self.screenW, self.scaledTile[1]) )

		#for the equipped focuses
		for i in range(8):
			if self.eq[i] is None:
				surf = pg.Surface(self.scaledTile)
				surf.fill((100,100,100))
				g.giveBorder(surf, g.BLACK, 1)
			else:
				surf = self.eq[i].getIcon()
				surf = pg.transform.scale(surf, self.scaledTile)
				# g.giveBorder(surf, g.BLACK, 1)
			self.img.blit(surf, (i*self.scaledTile[0], 0))

		#for the health bar
		self.hpPanel = pg.Surface((self.screenW - self.scaledTile[0]*16, self.scaledTile[1]))
		self.hpPanel.fill(g.WHITE)
		g.giveBorder(self.hpPanel, g.BLACK, 1)
		self.adjustCurrentHP(self.curHP) #anytime you equip a new focus it will look like you have full hp!!!!!!

		#for the shard totals
		self.shardPanel = pg.Surface((self.scaledTile[0]*2, self.scaledTile[1]))
		self.shardPanel.fill((100,100,100))
		g.giveBorder(self.shardPanel, g.BLACK, 1)
		self.adjustCurrentShards(self.curShards)
	
	def getImg(self): return self.img
	# def getImg(self): return pg.transform.scale(self.img, (self.screenW, int((self.screenW/float(self.img.get_width())) * self.img.get_height())))
	def getTotalHP(self): return self.hp
	
	def equip(self, slot, set):
		self.eq[slot] = set
		self.genImg()

	def adjustCurrentHP(self, amt): # needs to be amt/total (not -amt)
		self.curHP = amt

		surfw = self.hpPanel.copy()

		#make red rectangle surface
		width = (amt/float(self.getTotalHP())) * (surfw.get_width()-2) #the two is the black pixel border
		surfr = pg.Surface((width, self.scaledTile[1]-2))
		surfr.fill(g.RED)

		#put it on the white surface
		surfw.blit(surfr, (1,1))

		#put new hp on the belt
		self.getImg().blit(surfw, (8*self.scaledTile[0], 0))
	
	def adjustCurrentShards(self, sh):
		self.curShards = sh

		for i in range(4):
			surfc = self.shardPanel.copy()

			half = (surfc.get_height()-2)/2
			texttop = self.font.text(self.shardTypes[3-i]+":", half)
			textbot = self.font.text(str(sh[self.shardTypes[3-i].lower()]), half)

			surfc.blit(texttop.get(), (1,1))
			surfc.blit(textbot.get(), (1,1+half))
			self.img.blit(surfc, (self.getImg().get_width() - ((i+1)*2)*self.scaledTile[0],0))
	
	def cast(self, slot, *args):
		if self.eq[slot] is not None:
			return self.eq[slot].cast(*args)
		return False
	
	def tick(self, dt):
		for each in self.eq:
			if self.eq[each]:
				fraction = self.eq[each].tick(dt)
				if fraction and each != 8:
					surf = pg.Surface((self.scaledTile[0], self.scaledTile[1]*fraction))
					surf.fill(g.BLACK)
					surf.set_alpha(200)

					icon = pg.transform.scale(self.eq[each].getIcon(), self.scaledTile)
					icon.blit(surf, (0,0))

					# g.giveBorder(icon, g.BLACK, 1)

					self.img.blit(icon, (self.scaledTile[0]*each, 0))