import pygame as pg
import time

import text
import worldEventsParser

import general as g

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
		self.art = art.subsurface(tileRect(art_tile, g.TILE_RES)).copy()
		self.art_outlined = self.getOutlinedArt()

		# self.art_tile = art_tile
		self.extra = extra
		self.rect = tileRect(on, g.TILE_RES)
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
		for i in range(g.TILE_RES[0]):
			for j in range(g.TILE_RES[1]):
				if tuple(newArt.get_at((i,j)))[3] != 0:
					newArt.set_at((i,j), (255,0,0))
					break
		#sets bottom to red
		for i in range(g.TILE_RES[0]):
			for j in range(g.TILE_RES[1])[::-1]:
				if tuple(newArt.get_at((i,j)))[3] != 0:
					newArt.set_at((i,j), (255,0,0))
					break
		#sets left to red
		for j in range(g.TILE_RES[0]):
			for i in range(g.TILE_RES[1]):
				if tuple(newArt.get_at((i,j)))[3] != 0:
					newArt.set_at((i,j), (255,0,0))
					break
		#sets right to red
		for j in range(g.TILE_RES[0]):
			for i in range(g.TILE_RES[1])[::-1]:
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
		namesize = 20 #height in pixels for the speaker's name
		namepadding = 3 #pixels away from the edge of the box for the name placement
		dialogsize = 35 #height in pixels
		dialogwidthfraction = .90 #the fraction of the width of the box that the lines of dialog take

		# if player is on the top half of the screen or exactly in the middle, make a text box on the bottom
		# otherwise, if player's on the bottom half, make it on the top.
		# and wait for an enter key press to go to the next line

		box = pg.Surface((int(GI.display.getWH()[0]), int(GI.display.getWH()[1]*.25)))
		box.fill((96,123,139))

		enter = text.Text("PRESS ENTER", namesize, (10,50,10))
		enter.place(box, (box.get_rect().width-namepadding-enter.getLength(), namepadding), center=False)

		dialogLinesPerBox = (box.get_rect().height - namesize - namepadding*2) / dialogsize
		linesPx = [(int(box.get_rect().width*((1-dialogwidthfraction)/2)), int(namesize + namepadding*2))]
		for i in range(dialogLinesPerBox-1):
			linesPx.append((linesPx[i][0], int(linesPx[i][1]+dialogsize)))

		dialogWidth = int(box.get_rect().width*dialogwidthfraction)

		# make a space and ellipses
		space = text.Text(" ",   dialogsize, text.BLACK)
		ooo   = text.Text("...", dialogsize, text.BLACK)

		dialogLines = self.extra[1:]

		q = 0
		while q < (len(dialogLines)):
			boxc = box.copy()

			speaker, words = dialogLines[q].split(":] ")

			if speaker == "%PLAYER":
				speaker = GI.player.getName()
			speaker = text.Text(speaker+":", namesize, (10,50,10))
			speaker.place(boxc, (namepadding,namepadding), center=False)

			words = words.split(' ')
			for i in range(len(words)):
				words[i] = text.Text(words[i], dialogsize, text.BLACK)

			line = 0
			lines = []
			
			word = 1
			lines.append(words[0])
			while word < len(words):
				if lines[line].getLength() + space.getLength() + words[word].getLength() <= dialogWidth:
					lines[line] = lines[line].concatenate([space, words[word]])
				else:
					line+=1
					lines.append(words[word])
				word +=1
			
			passback = speaker.getStr()+"] "
			for i in range(len(lines)):
				if i < dialogLinesPerBox:
					lines[i].place(boxc, linesPx[i], center=False)
				else:
					passback += lines[i].getStr()
					if i != len(lines)-1:
						passback+=" "
			if i >= dialogLinesPerBox:
				dialogLines.insert(q+1, passback)
			
			if GI.playerOnTopHalf():
				pos = (0,GI.display.getWH()[1]-boxc.get_rect().height)
			else:
				pos = (0,0)
			GI.window.blit(boxc, pos)

			GI.renderView()
			GI.clearWindow()
			
			gotEnter = False
			while not gotEnter:
				#wait only gets the first event that happens, so it's not a list
				evt = pg.event.wait()
				evt = GI.dispatch([evt])
				if len(evt) > 0:
					evt = evt[0]
					if evt.type == pg.KEYDOWN:
						if evt.dict['key'] == pg.K_RETURN:
							gotEnter = True
							break
			q+=1

		GI.renderView()



EVENT_IDS = { 1: dialog } #,
	  # 2: PickUpItem,
	  # 3: DeathByBurning }
