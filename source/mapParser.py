import pygame as pg

import worldEvents

TILE_RESOLUTION = 32

def tileRect((x, y), squareSize):
	return pg.Rect((x * squareSize[0], y * squareSize[1]), squareSize)

def tileToMap(mapSurface, tileCoordsTo, tileSubsurface, squaresize):
	toRect = tileRect(tileCoordsTo, squaresize)
	mapSurface.blit(tileSubsurface, toRect)

def parseMapLine(line):
	pos, tile = line.split("/")

	# construct map position x,y coords
	pos = tuple([int(i) for i in pos.split(":")])

	# tile source position (type)
	tile = tile.split("(")
	type = tuple([int(i) for i in tile[0].split(":")])
	tile = tile[1]

	# blocked = cannot be walked on (1 is blocked)
	blocked = True if tile[:-1] == "1" else False

	return pos, Tile(type, blocked)
	

def parse(file):
	theMap = [line.strip() for line in open(file, 'r').readlines()]
	
	tileFile = theMap[1]
	tileSize = [int(theMap[3]), int(theMap[4])]
	mapSize = [int(theMap[6]), int(theMap[7])]
	
	# setup = [[],[]]
	setup = {}
	for line in theMap[9:]:
		# first, second = each.split("/")
		# print first, second
		pos, tile = parseMapLine(line)
		setup[pos] = tile
	return tileFile, tileSize, mapSize, setup

class Tile:
	def __init__(self, type, blocked):
		self.Type = type
		self.Blocked = blocked
		self.Events = []
		self.under = None
		self.mapSubsurface = None
	
	def type(self):
		return self.Type
	
	def blocked(self):
		return self.Blocked
	
	def addEvents(self, event, mapSubsurface):
		self.Events.extend(event)
		self.genEvent(mapSubsurface)
		
		
		# for each in self.Events:
			
	def genEvent(self, mapSubsurface):
		evt = self.Events[0]
		
		#get the art
		artfile, arttile = evt.imageInfo()
		artfile = pg.image.load(artfile).convert_alpha()
		
		#place it on map
		self.under = mapSubsurface.copy()
		self.mapSubsurface = mapSubsurface
		arttile = tileRect(arttile, (32,32))
		mapSubsurface.blit(artfile.subsurface(arttile), (0,0))
		
		#change tile info (such as blocked)
	
	def removeEvent(self):
		del(self.Events[0])
		
		#replace old tile
		self.mapSubsurface.blit(self.under, (0,0))
		
		#call genEvent on next event if there is one
		if len(self.Events) >0:
			self.genEvent(self.mapSubsurface)
	
	def hasEvent(self):
		# if len(self.WorldEvents) > 0:
			# print self.WorldEvents
		# print self.WorldEvents
		for each in self.Events:
			each.execute()
			self.removeEvent()

class TileMap:
	def __init__(self, tileFile, squareSize):
		self.tileFile = tileFile
		self.tileImg = pg.image.load(self.tileFile).convert()
		self.tileDict = self.genSubsurfaces(squareSize)
	
	def get(self, coords):
		return self.tileDict[coords]
	
	def genSubsurfaces(self, squareSize):
		tileDict = {}
		imgRect = self.tileImg.get_rect()
		x, y = 0, 0
		morey = True
		while morey:
			while True:
				tile = tileRect((x, y), squareSize)
				if imgRect.contains(tile):
					tileDict[(x, y)] = self.tileImg.subsurface(tile)
					x += 1
				else:
					if x == 0:
						morey = False
					else:
						x = 0
					break
			y += 1
		return tileDict


class Map:
	def __init__(self, file):
		self.file = file + ".map"
		self.evtFile = file + ".evt"

		self.tileFile, self.tileSize, self.mapSize, self.setup = parse(self.file)

		self.img = pg.Surface((self.mapSize[0]*self.tileSize[0], self.mapSize[1]*self.tileSize[1]))

		tm = TileMap(self.tileFile, self.tileSize)
		we = worldEvents.parse(self.evtFile)

		for pos in self.setup.keys():
			tileToMap(self.img, pos, tm.get(self.setup[pos].type()), self.tileSize)
		
		self.img_eventless = self.img.copy()
		
		for pos in self.setup.keys():
			if pos in we:
				mapSubsurface = self.img.subsurface(tileRect(pos, self.tileSize))
				self.setup[pos].addEvents(we[pos], mapSubsurface)
				

	def get(self):
		return self.img
	
	def get_eventless(self):
		return self.img_eventless
	
	def get_rect(self):
		return self.img.get_rect()
	
	def tile2pix(self,(x, y)):
		if x > self.mapSize[0] or y > self.mapSize[1] or x < 0 or y < 0:
			print "out of bounds"
			raise KeyboardInterrupt
		# print (x+.5), self.tileSize[0], (y+.5), self.tileSize[1], int((x+.5)*self.tileSize[0]), int((y+.5)*self.tileSize[1])
		return (int((x+.5)*self.tileSize[0]), int((y+.5)*self.tileSize[1]))
	
	def pix2tile(self,(x,y)):
		return (int(x/self.tileSize[0]), int(y/self.tileSize[1]))
	
	def getTileSize(self):
		return self.tileSize
	
	def getTile(self, coords, pixel=True): #false means tile
		if pixel:
			return self.setup[self.pix2tile(coords)]
		else:
			return self.setup[coords]
	
	def blocked(self, coords, pixel=True): #false means tile
		if pixel:
			return self.setup[self.pix2tile(coords)].blocked()
		else:
			return self.setup[coords].blocked()
	
	def hasEvent(self, coords, pixel=True): # false means tile
		if pixel:
			return self.setup[self.pix2tile(coords)].hasEvent()
		else:
			return self.setup[coords].hasEvent()