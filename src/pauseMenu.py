import pygame as pg

class PMenu:
	def __init__(self, GI):
		self.GI = GI
		self.wh = self.GI.display.getWH()
		self.state = "player"
		"""
		player
			inventory
			stats
			spellbar
		options
			screen
				togglefs
				resolution
			sound
				mute
		"""

		self.displayed = None
	
	# def genDisp(self):
		
	def getState(self):
		return self.state

	def changeState(self, newstate):
		self.state = newstate

	def getDisp(self):
		if self.displayed is None:
			self.blankdisplay()
			self.dispatch(self.state)
		return self.displayed

	def clearall(self):
		self.displayed = None

	def blankdisplay(self):
		self.displayed = pg.Surface(self.wh).convert_alpha()
		self.displayed.fill((223, 163, 43))
	
	def playerdisplay(self): #defaults to inventory
		self.blankdisplay()
		t = self.GI.font.text("(P)layer   |   (O)ptions", 30)
		t.place(self.displayed, (int(self.wh[0]/2.), 15))
		t = self.GI.font.text("(I)nventory | (B)elt | (S)tats", 30)
		t.place(self.displayed, (int(self.wh[0]/2.), 45))
	
	def optionsdisplay(self):
		self.blankdisplay()
		t = self.GI.font.text("(O)ptions   |   (P)layer", 30)
		t.place(self.displayed, (int(self.wh[0]/2.), 15))
		t = self.GI.font.text("(S)ound | S(c)reen", 30)
		t.place(self.displayed, (int(self.wh[0]/2.), 45))
	
	def dispatch(self, key):
		if key == pg.K_p or key == "player":
			self.state = "player"
			self.playerdisplay()
			
		elif key == pg.K_o or key == "options":
			self.state = "options"
			self.optionsdisplay()
		
		if self.state == "player":
			if key == pg.K_i: #show inventory
				t = self.GI.font.text(str(self.GI.player.getSortedInv()), 20)
				t.place(self.displayed, (0, 70), center=False)
		
		elif self.state == "options":
			if key == pg.K_c: #show inventory
				t = self.GI.font.text("(T)oggle Fullscreen", 20)
				t.place(self.displayed, (int(self.wh[0]/2.), 70), center=True)
		# if key == pg.K_ESCAPE:
		# 	GI.state = "play"
		# 	GI.pmenu.clearall()
		# 	return
		
