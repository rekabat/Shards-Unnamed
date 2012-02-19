import pygame as pg

import general as g

class Attack:
	def __init__(self):
		self.duration = 0
		self.power = 0
		self.rect = pg.Rect((0,0), g.TILE_RES)
		self.img = None
		self.barimg = None
	
class sword(Attack):
	def __init__(self):#, **kwargs):
		WorldEvent.__init__(self)#, **kwargs)
		self.duration 