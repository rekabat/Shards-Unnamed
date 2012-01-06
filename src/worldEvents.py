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
		self.eventList, self.mapSize, self.img = worldEventsParser.parse(self.file, EVENT_IDS)

	def get(self):
		return self.img
	
	def onAndGetEvents(self, rect):
		for each in self.eventList:
			if each.rect.collidepoint(rect.center):
				return each
		return False
	
	def nearAndGetEvents(self,coord):
		pass
	
	def blocked(self, rect):
		for each in self.eventList:
			if each.rect.colliderect(rect) and each.blocked:
				return True
		return False
	
	def remove(self, event):
		erase = pg.Surface(event.art.get_size())
		erase.fill((199,200,201))
		self.get().blit(erase, event.rect)
		if event.behind != None:
			self.activate(event.behind)
		self.eventList.remove(event) #maybe at the top
	
	def activate(self, event):
		self.eventList.append(event)
		self.get().blit(event.art, event.rect)
		#draw to img
		print 'Working on it'
		
	# def registerEvent(self, event, subsurface):
	# 	self.drawEvent(event, subsurface)
	# 	# Somehow dispatch 
	
	# def drawEvent(self, event, subsurface):
	# 	artFile, artTile = event.imageInfo()
	# 	artFile = pg.image.load(artFile).convert_alpha()
	# 	artTile = tileRect(artTile, (32,32))
	# 	subsurface.blit(artFile.subsurface(artTile), (0,0))


class WorldEvent:
	def __init__(self, on, blocked, event_id, one_time, art, art_tile, extra):
		self.on = on
		self.blocked = blocked
		self.event_id = event_id
		self.one_time = one_time

		art = pg.image.load(art).convert_alpha()
		self.art = art.subsurface(tileRect(art_tile, TILE_RES)).copy()

		# self.art_tile = art_tile
		self.extra = extra
		self.rect = tileRect(on, TILE_RES)
		self.behind = None #WE get stacked behind other events on the same tile, that is, when one gets executed and removed the one behind it gets placed

	# def imageInfo(self):
	# 	return self.art, self.art_tile
	
	def setDeepest(self, WE):
		if self.behind is not None:
			self.behind.setDeepest(WE)
		else:
			self.behind = WE
		

class TwoWayDialog(WorldEvent):
	def __init__(self, **kwargs):
		WorldEvent.__init__(self, **kwargs)
	
	def execute(self, GI):
		print 'success', self
		new = text.Text("SUCCESS", 50)
		new.place(GI.window, (0,0), center=False)
		# pg.display.flip()
		GI.renderView()
		time.sleep(1)
		GI.clearWindow()
		GI.renderView()


EVENT_IDS = { 1: TwoWayDialog } #,
	  # 2: PickUpItem,
	  # 3: DeathByBurning }
