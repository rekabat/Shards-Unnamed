import pygame as pg
import time

import text

class WorldEvent:
	def __init__(self, on, blocked, event_id, one_time, art, art_tile, extra):
		self.on = on
		self.blocked = blocked
		self.event_id = event_id
		self.one_time = one_time
		self.art = art
		self.art_tile = art_tile
		self.extra = extra

	def imageInfo(self):
		return self.art, self.art_tile
		

class TwoWayDialog(WorldEvent):
	def __init__(self, **kwargs):
		WorldEvent.__init__(self, **kwargs)
	
	def execute(self, GI):
		print 'success', self
		new = text.Text("SUCCESS", 50)
		new.place(pg.display.get_surface(), (0,0), center=False)
		# pg.display.flip()
		time.sleep(1)
		GI.map.setup[self.on].removeEvent()


EVENT_IDS = { 1: TwoWayDialog } #,
	  # 2: PickUpItem,
	  # 3: DeathByBurning }
