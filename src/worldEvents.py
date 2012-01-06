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
	
	def nearAndGetBlockedEvents(self, rect):
		#actually... same as blocked, just pass it the full sized rectangle instead of the shrunken one
		pass
	def getBlockedEvents(self, rect):
		for each in self.eventList:
			if each.rect.colliderect(rect) and each.blocked:
				return each
	
	def blocked(self, rect):
		for each in self.eventList:
			if each.rect.colliderect(rect) and each.blocked:
				return True
		return False
	
	def remove(self, event):
		#create a transparent tile
		erase = pg.Surface(event.getArt().get_size())
		erase.fill((199,200,201))
		#put over the current event artwork
		self.get().blit(erase, event.rect)
		#activate the event beind it
		if event.behind != None:
			self.activate(event.behind)
		#remove the event
		self.eventList.remove(event)
	
	def activate(self, event):
		#add event to the list
		self.eventList.append(event)
		#draw to the event foreground surface
		self.get().blit(event.getArt(), event.rect)


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

	def getArt(self):
		return self.art
	
	def setDeepest(self, WE):
		if self.behind is not None:
			self.behind.setDeepest(WE)
		else:
			self.behind = WE
		

class TwoWayDialog(WorldEvent):
	def __init__(self, **kwargs):
		WorldEvent.__init__(self, **kwargs)
	
	def execute(self, GI):
		new = text.Text("SUCCESS", 50)
		new.place(GI.window, (0,0), center=False)
		GI.renderView()
		time.sleep(1)
		GI.clearWindow()
		GI.renderView()


EVENT_IDS = { 1: TwoWayDialog } #,
	  # 2: PickUpItem,
	  # 3: DeathByBurning }
