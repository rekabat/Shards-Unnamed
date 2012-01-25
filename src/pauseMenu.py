import pygame as pg

class PMenu:
	def __init__(self, wh):
		self.wh = wh
		self.state = "player"
		"""
		player
			items
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
		
	
	def getDisp(self):
		if self.displayed is None:
			self.displayed = pg.Surface(self.wh).convert_alpha()
			self.displayed.fill((35, 5, 0))
		return self.displayed
	
	def clearall(self):
		self.displayed = None