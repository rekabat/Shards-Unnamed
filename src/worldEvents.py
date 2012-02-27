import pygame as pg
from pygame.locals import *
import time

import worldEventsParser

import general as g
import enemies

class EventForeground:
	def __init__(self, file):
		self.file = file + ".evt"
		self.eventList = worldEventsParser.parse(self.file, EVENT_IDS)

	def getEventsOfAndBelow(self, z, partial = False):
		ret=[]
		for each in self.eventList:
			if each.getZ() <= z:
				ret.append(each)
		return ret
	
	def getEventsOfAndAbove(self, z, partial = False):
		ret=[]
		for each in self.eventList:
			if each.getZ() >= z:
				ret.append(each)
		return ret

	def immediates(self):
		ret = []
		for e in self.eventList:
			if e.immediate:
				ret.append(e)
		return ret

	def unlockedEnterableEventsOn(self, tileList, zlist):
		ret = []
		for tile in tileList:
			for each in self.eventList:
				if each.enter and (not each.locked) and (each.z in zlist) and each.getRect().colliderect(tile.getRect()):
					ret.append(each)
		return ret

	def unlockedEnterableBlockedEventsOn(self, tileList, zlist):
		ret = []
		for tile in tileList:
			for each in self.eventList:
				if each.enter and (not each.locked) and (each.blocked) and (each.z in zlist) and each.getRect().colliderect(tile.getRect()):
					ret.append(each)
		return ret
	
	def unlockedNotEnterableEventsOn(self, tileList, zlist):
		ret = []
		for tile in tileList:
			for each in self.eventList:
				if (not each.enter) and (not each.locked) and (each.z in zlist) and (each.getRect().colliderect(tile.getRect())):
					ret.append(each)
		return ret
	
	def blocked(self, rect, zlist):
		for each in self.eventList:
			if each.getZ() in zlist:
				if each.rect.colliderect(rect) and each.blocked:
					return True
		return False
	
	def remove(self, event):
		#activate the event beind it
		if event.behind != None:
			#add event to the list
			self.eventList.append(event.behind)
		#remove the event
		self.eventList.remove(event)
		#call the events terminate function so it can do anythin specific that it needs to
		event.terminate()


	
	def activate(self, event):
		pass


class WorldEvent:
	def __init__(self, event_id, art, art_tile, on, z, blocked, enter, one_time, locked, immediate, extra):
		self.event_id 	= event_id 	#the type of event
		self.on 		= on 		#tile position
		self.z 			= z 		#z level
		self.blocked 	= blocked 	#whether or not the event causes the tile to be blocked
		self.enter 		= enter 	#whether it's activated by enter or stepping on (T/F)
		self.one_time 	= one_time 	#whther it can be activated once or inifinite times (T/F)
		self.locked 	= locked 	#whether the event is currently available or not (T/F)
		self.immediate 	= immediate #whether the event is activated as soon as it's available (T/F)
		self.extra 		= extra		#the text in the evt file that defines the specific event

		if art is not None:
			art = pg.image.load(art).convert_alpha()
			self.art = art.subsurface(g.tile2rect(art_tile)).copy()
			self.art_outlined = self.makeOutlinedArt()
		else:
			self.art = pg.Surface(g.TILE_RES, SRCALPHA, 32).convert_alpha()
			self.art_outlined = self.art.copy()
			for i in range(g.TILE_RES[0]):
				self.art_outlined.set_at((i, 0), g.RED)
				self.art_outlined.set_at((i, g.TILE_RES[1]-1), g.RED)
			for i in range(g.TILE_RES[1]):
				self.art_outlined.set_at((0, i), g.RED)
				self.art_outlined.set_at((g.TILE_RES[0]-1, i), g.RED)
		

		
		self.rect = g.tile2rect(on)
		self.behind = None #WE get stacked behind other events on the same tile, that is, when one gets executed and removed the one behind it gets placed

	def getArt(self): return self.art
	def getOutlinedArt(self): return self.art_outlined
	def getRect(self): return self.rect
	def getZ(self): return self.z
	def getOneTime(self): return self.one_time
	
	def switchArt(self):
		temp = self.art
		self.art = self.art_outlined
		self.art_outlined = temp
	
	def makeOutlinedArt(self):
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
	
	def setDeepest(self, WE):
		if self.behind is not None:
			self.behind.setDeepest(WE)
		else:
			self.behind = WE

	def execute(self): pass
	def terminate(self): pass
		

class dialog(WorldEvent):
	def __init__(self, **kwargs):
		WorldEvent.__init__(self, **kwargs)
	
	def execute(self, GI):
		namesize = 20 #height in pixels for the speaker's name
		namepadding = 3 #pixels away from the edge of the box for the name placement
		dialogwidthfraction = .90 #the fraction of the width of the box that the lines of dialog take
		linesPerBox = 3 #how many lines of text in the box

		# if player is on the top half of the screen or exactly in the middle, make a text box on the bottom
		# otherwise, if player's on the bottom half, make it on the top.
		# and wait for an enter key press to go to the next line

		box = pg.Surface((int(GI.display.getWH()[0]*.80), int(GI.display.getWH()[1]*.25)))
		box.fill((96,123,139))
		box.set_alpha(180)
		alph = (99,100,101)
		box.set_colorkey(alph)
		n3 = namepadding*3
		x1 = 0
		y1 = n3
		x2 = namepadding
		y2 = namepadding
		x3 = n3
		y3 = 0
		y = .5*((x1**2+y1**2)*(x3-x2) + (x2**2+y2**2)*(x1-x3) + (x3**2+y3**2)*(x2-x1)) / (y1*(x3-x2)+y2*(x1-x3)+y3*(x2-x1))
		radius = g.distance((y,y), (namepadding, namepadding))

		for i in range(n3):
			for j in range(n3):
				if g.distance((i,j),(y,y)) > radius:
					box.set_at((i,j), alph)
					box.set_at((box.get_rect().width - i, j), alph)
					box.set_at((i, box.get_rect().height - j), alph)
					box.set_at((box.get_rect().width - i, box.get_rect().height - j), alph)


		enter = GI.font.text("PRESS ENTER", namesize)
		enter.place(box, (box.get_rect().width-namepadding-enter.getLength(), namepadding), center=False)

		# dialogLinesPerBox = (box.get_rect().height - namesize - namepadding*2) / dialogsize
		dialogsize = (box.get_rect().height - namesize - namepadding*3) / linesPerBox
		linesPx = [(int(box.get_rect().width*((1-dialogwidthfraction)/2)), int(namesize + namepadding*2))]
		for i in range(linesPerBox-1):
			linesPx.append((linesPx[i][0], int(linesPx[i][1]+dialogsize)))

		dialogWidth = int(box.get_rect().width*dialogwidthfraction)

		# make a space and ellipses
		space = GI.font.text(" ",   dialogsize)
		ooo   = GI.font.text("...", dialogsize)

		dialogLines = self.extra[1:]

		q = 0
		while q < (len(dialogLines)):
			boxc = box.copy()
			boxc = pg.Surface(box.get_size())
			boxc.set_colorkey(alph)
			boxc.fill(alph)

			speaker, words = dialogLines[q].split(":] ")

			if speaker == "%PLAYER":
				speaker = GI.player.getName()
			speaker = GI.font.text(speaker+":", namesize)
			speaker.place(boxc, (namepadding,namepadding), center=False)

			words = words.split(' ')
			for i in range(len(words)):
				words[i] = GI.font.text(words[i], dialogsize)

			line = 0
			lines = []
			
			word = 1
			lines.append(words[0])
			while word < len(words):
				# if (line != 0) and ((line-1)%linesPerBox == 0):
				# 	print line, linesPerBox, linesPerBox%line
				# 	this = lines[line].getLength() + space.getLength() + words[word].getLength() + ooo.getLength()
				# else:
				# 	this = lines[line].getLength() + space.getLength() + words[word].getLength()
				# if this <= dialogWidth:
				# 	if (line != 0) and ((line-1)%linesPerBox == 0):
				# 		lines[line] = lines[line].concatenate([space, words[word], ooo])
				# 	else:
				# 		lines[line] = lines[line].concatenate([space, words[word]])
				# else:
				# 	line+=1
				# 	lines.append(words[word])
				# word +=1
				this = lines[line].getLength() + space.getLength() + words[word].getLength()
				if this <= dialogWidth:
					lines[line] = lines[line].concatenate([space, words[word]])
				else:
					line+=1
					lines.append(words[word])
				word +=1
			
			passback = speaker.getStr()+"] "
			for i in range(len(lines)):
				if i < linesPerBox:
					lines[i].place(boxc, linesPx[i], center=False)
				else:
					passback += lines[i].getStr()
					if i != len(lines)-1:
						passback+=" "
			if i >= linesPerBox:
				dialogLines.insert(q+1, passback)
			
			if GI.playerOnTopHalf():
				pos = ((GI.display.getWH()[0] - boxc.get_rect().width) /2.,
						GI.display.getWH()[1]-boxc.get_rect().height-g.TILE_RES[1]*1.5)
			else:
				pos = ((GI.display.getWH()[0] - boxc.get_rect().width) /2.,
						g.TILE_RES[1]*1.5)
			GI.window.blit(box, pos)
			GI.window.blit(boxc, pos)

			GI.renderView()
			GI.clearWindow()
			
			gotEnter = False
			while not gotEnter:
				#wait only gets the first event that happens, so it's not a list
				evt = pg.event.wait()
				evt, trash0 = GI.dispatch([evt])
				if len(evt) > 0:
					evt = evt[0]
					if evt.type == pg.KEYDOWN:
						if evt.dict['key'] == pg.K_RETURN:
							gotEnter = True
							break
			q+=1

		GI.renderView()

class teleport(WorldEvent):
	def __init__(self, **kwargs):
		WorldEvent.__init__(self, **kwargs)
	
	def execute(self, GI):
		tileTo = tuple([int(each) for each in self.extra[1].split(":")])
		zTo = [int(each) for each in self.extra[2].split(",")]

		GI.player.setPlace(tileTo, zTo)

class enemy(WorldEvent):
	def __init__(self, **kwargs):
		WorldEvent.__init__(self, **kwargs)

	def execute(self, GI):
		# moveables.Moveable(enemyCatalog[self.extra[1]])
		GI.addEnemy(enemies.Enemy(GI, self.on, [self.getZ()], (1,1), 'art/playersprite.png', 75))
		




EVENT_IDS = {	'dialog': dialog,
				'teleport': teleport, 
				'enemy': enemy} #,
	  # 2: PickUpItem,
	  # 3: DeathByBurning }
