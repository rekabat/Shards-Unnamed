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
		self.eventList = worldEventsParser.parse(self.file, EVENT_IDS)
	
	def onAndGetEvents(self, rect):
		for each in self.eventList:
			if each.rect.collidepoint(rect.center):
				return each
		return False
	
	def nearAndGetBlockedEvents(self, rect):
		#actually... same as blocked, just pass it the full sized rectangle instead of the shrunken one
		pass
	def getBlockedEvents(self, rect):
		ret = []
		for each in self.eventList:
			if each.rect.colliderect(rect) and each.blocked:
				ret.append(each)
		return ret
	
	def getEventsInRect(self, rect):
		ret = []
		for each in self.eventList:
			if each.rect.colliderect(rect):
				ret.append(each)
		return ret

	
	def blocked(self, rect):
		for each in self.eventList:
			if each.rect.colliderect(rect) and each.blocked:
				return True
		return False
	
	def remove(self, event):
		#activate the event beind it
		if event.behind != None:
			self.activate(event.behind)
		#remove the event
		self.eventList.remove(event)
	
	def activate(self, event):
		#add event to the list
		self.eventList.append(event)


class WorldEvent:
	def __init__(self, on, blocked, event_id, one_time, art, art_tile, extra):
		self.on = on
		self.blocked = blocked
		self.event_id = event_id
		self.one_time = one_time

		art = pg.image.load(art).convert_alpha()
		self.art = art.subsurface(tileRect(art_tile, TILE_RES)).copy()
		self.art_outlined = self.getOutlinedArt()

		# self.art_tile = art_tile
		self.extra = extra
		self.rect = tileRect(on, TILE_RES)
		self.behind = None #WE get stacked behind other events on the same tile, that is, when one gets executed and removed the one behind it gets placed

	def getArt(self):
		return self.art
	
	def getOutlinedArt(self):
		return self.art_outlined
	
	def switchArt(self):
		temp = self.art
		self.art = self.art_outlined
		self.art_outlined = temp
	
	def getOutlinedArt(self):
		newArt = self.art.copy()
		#sets top to red
		for i in range(TILE_RES[0]):
			for j in range(TILE_RES[1]):
				if tuple(newArt.get_at((i,j)))[3] != 0:
					newArt.set_at((i,j), (255,0,0))
					break
		#sets bottom to red
		for i in range(TILE_RES[0]):
			for j in range(TILE_RES[1])[::-1]:
				if tuple(newArt.get_at((i,j)))[3] != 0:
					newArt.set_at((i,j), (255,0,0))
					break
		#sets left to red
		for j in range(TILE_RES[0]):
			for i in range(TILE_RES[1]):
				if tuple(newArt.get_at((i,j)))[3] != 0:
					newArt.set_at((i,j), (255,0,0))
					break
		#sets right to red
		for j in range(TILE_RES[0]):
			for i in range(TILE_RES[1])[::-1]:
				if tuple(newArt.get_at((i,j)))[3] != 0:
					newArt.set_at((i,j), (255,0,0))
					break
		return newArt
	
	def getRect(self):
		return self.rect
	
	def setDeepest(self, WE):
		if self.behind is not None:
			self.behind.setDeepest(WE)
		else:
			self.behind = WE
		

class dialog(WorldEvent):
	def __init__(self, **kwargs):
		WorldEvent.__init__(self, **kwargs)
	
	def execute(self, GI):
		# if player is on the top half of the screen or exactly in the middle, make a text box on the bottom
		# otherwise, if player's on the bottom half, make it on the top.
		# and wait for an enter key press to go to the next line


		
		box = pg.Surface((int(GI.display.getWH()[0]), int(GI.display.getWH()[1]*.25)))
		box.fill((96,123,139))
		for each in self.extra[1:]:
			speaker, words = each.split(":] ")
			# words = words.split(' ')

			GI.window.blit(box, (0,0))

			speaker = text.Text(speaker+":", 20, (10,50,10))
			speaker.place(GI.window, (3,3), center=False)

			words = text.Text(words, 50, text.BLACK)
			words.place(GI.window, (10,25), center=False)

			GI.renderView()
			GI.clearWindow()
			
			gotEnter = False
			while not gotEnter:
				evt = pg.event.wait()
				if evt.type == pg.KEYDOWN:
					if evt.dict['key'] == pg.K_RETURN:
						gotEnter = True
						break

			
		GI.renderView()



EVENT_IDS = { 1: dialog } #,
	  # 2: PickUpItem,
	  # 3: DeathByBurning }
