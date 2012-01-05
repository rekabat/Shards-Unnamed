import pygame as pg
import time

import text
import worldEventsParser

TILE_RES = (32,32)

def tileRect((x, y), squareSize):
	return pg.Rect((x * squareSize[0], y * squareSize[1]), squareSize)

class EventForeground:
	def __init__(self, file):
		self.file = file + ".evt"
		self.eventDict, mapInTiles = worldEventsParser.parse(self.file, EVENT_IDS)
		self.mapSize = (mapInTiles[0] * TILE_RES[0],
						mapInTiles[1] * TILE_RES[1])

		self.img = pg.Surface(self.mapSize)

		for pos in self.eventDict:
			for event in self.eventDict[pos]:
				rect = tileRect(pos, TILE_RES)
				event.rect = rect
				sub = self.img.subsurface(rect)
				self.registerEvent(event, sub)

	def get(self):
		return self.img
	
	def registerEvent(self, event, subsurface):
		self.drawEvent(event, subsurface)
		# Somehow dispatch 
	
	def drawEvent(self, event, subsurface):
		artFile, artTile = event.imageInfo()
		artFile = pg.image.load(artFile).convert_alpha()
		artTile = tileRect(artTile, (32,32))
		subsurface.blit(artFile.subsurface(artTile), (0,0))


class WorldEvent:
	def __init__(self, on, blocked, event_id, one_time, art, art_tile, extra):
		self.on = on
		self.blocked = blocked
		self.event_id = event_id
		self.one_time = one_time
		self.art = art
		self.art_tile = art_tile
		self.extra = extra
		self.rect = None

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
