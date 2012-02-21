import pygame as pg

class PMenu:
	def __init__(self, GI):
		self.GI = GI
		self.wh = self.GI.display.getWH()

		self.state = [pg.K_1, pg.K_q]
		
		self.states = ("general", self.generalDispatch, { 
			pg.K_1: ("player", self.playerDispatch, {
				pg.K_q: ("inventory", self.inventoryDispatch, {} ),
				pg.K_w: ("equipped", self.equippedDispatch, {} ),
				pg.K_e: ("stats", self.statsDispatch, {} )
			} ),
			pg.K_2: ("saveload", self.saveloadDispatch, {
				pg.K_q: ("save", self.saveDispatch, {} ),
				pg.K_w: ("load", self.loadDispatch, {} )
			} ),
			pg.K_3: ("options", self.optionsDispatch, {
				pg.K_q: ("screen", self.screenDispatch, {} ), #togglefs, resolution
				pg.K_w: ("sound", self.soundDispatch, {} ) #mute
			} )
		} )



		"""
		player
			inventory
			belt
			stats
		options
			screen
				togglefs
				resolution
			sound
				mute
		"""

		self.menus = {}
		self.makeMenus()

		self.displayed = None
	
	# def genDisp(self):
		
	def getState(self): return self.state
	def getDisp(self):
		if self.displayed is None:
			self.dispatch(pg.K_1)
		return self.displayed
	
	def changeState(self, newstate):
		self.state = newstate

	def clearall(self):
		self.displayed = None
	
	def makeMenus(self):
		disp = pg.Surface(self.wh).convert_alpha()
		disp.fill((223, 163, 43))

		y=0

		########################################
		########################################
		t = self.GI.font.text("1)Player | 2)Save/Load | 3)Options | (ESC)Resume", 26)
		t.place(disp, (int(self.wh[0]/2.), y+13))
		y+=26
		pg.draw.line(disp, (255,255,255), (0, y+1), (self.wh[0], y+1), 3)
		y+=3
		########################################
		########################################
		temp = disp.copy()
		tempy = y
		t = self.GI.font.text("Q) Inventory || W) Equipped || E) Stats", 30)
		t.place(temp, (int(self.wh[0]/2.), tempy+15))
		tempy+=30
		pg.draw.line(temp, (255,255,255), (0, tempy+1), (self.wh[0], tempy+1), 3)
		tempy+=3
		self.menus["player"] = temp
		########################################
		temp = disp.copy()
		tempy = y
		t = self.GI.font.text("Q) Save || W) Load", 30)
		t.place(temp, (int(self.wh[0]/2.), tempy+15))
		tempy+=30
		pg.draw.line(temp, (255,255,255), (0, tempy+1), (self.wh[0], tempy+1), 3)
		tempy+=3
		self.menus["saveload"] = temp
		########################################
		temp = disp.copy()
		tempy = y
		t = self.GI.font.text("Q) Screen || W) Sound", 30)
		t.place(temp, (int(self.wh[0]/2.), tempy+15))
		tempy+=30
		pg.draw.line(temp, (255,255,255), (0, tempy+1), (self.wh[0], tempy+1), 3)
		tempy+=3
		self.menus["options"] = temp
		########################################
		y+=30
		y+=3
		########################################
		########################################
	
	def dispatch(self, key):
		toDispatch = self.states
		for each in self.state:
			if key in toDispatch[2].keys():
				break
			toDispatch = toDispatch[2][each]
		
		toDispatch[1](key, toDispatch[2])

	def generalDispatch(self, key, choices):
		if key in choices.keys():
			self.state = [key]
			self.displayed = self.menus[choices[key][0]]
			choices[key][1](pg.K_q, choices[key][2])


	
	def playerDispatch(self, key, choices):
		# change = choices[key][0]

		if key == pg.K_q: #show inventory
			self.displayed = self.menus["player"].copy()
			t = self.GI.font.text(str(self.GI.player.getSortedInv()), 20)
			t.place(self.displayed, (0, 75), center=False)

			self.state = [pg.K_1, pg.K_q]

		elif key == pg.K_w:
			self.displayed = self.menus["player"].copy()
			t = self.GI.font.text(str(self.GI.player.belt)+" - Belt Stuff!", 20)
			t.place(self.displayed, (0, 75), center=False)

			self.state = [pg.K_1, pg.K_w]

		elif key == pg.K_e:
			self.displayed = self.menus["player"].copy()
			t = self.GI.font.text(str(self.GI.player.stats)+" - yo' stats!", 20)
			t.place(self.displayed, (0, 75), center=False)

			self.state = [pg.K_1, pg.K_e]

	def inventoryDispatch(self, key, choices):
		pass

	def equippedDispatch(self, key, choices):
		pass

	def statsDispatch(self, key, choices):
		pass


	def saveloadDispatch(self, key, choices):

		if key == pg.K_q: #saving
			self.displayed = self.menus["saveload"].copy()
			t = self.GI.font.text("There ain't no stinking saves.", 20)
			t.place(self.displayed, (0, 75), center=False)

			self.state = [pg.K_2, pg.K_q]

		if key == pg.K_w: #loading
			self.displayed = self.menus["saveload"].copy()
			t = self.GI.font.text("There ain't no stinking loads.", 20)
			t.place(self.displayed, (0, 75), center=False)

			self.state = [pg.K_2, pg.K_w]

	def saveDispatch(self, key, choices):
		pass

	def loadDispatch(self, key, choices):
		pass


	def optionsDispatch(self, key, choices):

		if key == pg.K_q: #screen options
			self.displayed = self.menus["options"].copy()
			t = self.GI.font.text("A) Toggle Fullscreen On/Off", 20)
			t.place(self.displayed, (int(self.wh[0]/2.), 75), center=True)

			self.state = [pg.K_3, pg.K_q]

		if key == pg.K_w: #sound options
			self.displayed = self.menus["options"].copy()
			t = self.GI.font.text("A) Toggle Mute On/Off", 20)
			t.place(self.displayed, (int(self.wh[0]/2.), 75), center=True)

			self.state = [pg.K_3, pg.K_w]
	
	def screenDispatch(self, key, choices):#togglefs, resolution
		if key == pg.K_a:
			self.GI.display.toggleFull()
			self.GI.cursr.flipVisible()

	def soundDispatch(self, key, choices):#mute
		pass
