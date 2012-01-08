import pygame as pg
import general as g

def tileToMap(mapSurface, tileCoordsTo, tileSubsurface, squaresize):
	toRect = g.tile2rect(tileCoordsTo, squaresize)
	mapSurface.blit(tileSubsurface, toRect)

def genMap(file_base):
	file = file_base + '.map'

	tileFile, tileSize, mapSize, setup = parse(file)
	img =  pg.Surface((mapSize[0]*tileSize[0], mapSize[1]*tileSize[1]))

	tm = TileMap(tileFile, tileSize)

	for pos in setup.keys():
		tileToMap(img, pos, tm.get(setup[pos].type()), tileSize)
	
	if tileSize != g.TILE_RES:
		print tileSize, g.TILE_RES
		print "Warning: Tile size inconsistency"
		raise KeyboardInterrupt

	return {'img':img, 'tileFile':tileFile, 'tileSize':tileSize, 
			'mapSize':mapSize, 'setup':setup}

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
	# Future: Check tileSize vs. TILE_RES
	tileSize = tuple([int(theMap[3]), int(theMap[4])])
	mapSize = tuple([int(theMap[6]), int(theMap[7])])
	
	# setup = [[],[]]
	setup = {}
	for line in theMap[9:]:
		# first, second = each.split("/")
		pos, tile = parseMapLine(line)
		setup[pos] = tile
	return tileFile, tileSize, mapSize, setup

class Tile:
	def __init__(self, type, blocked):
		self.Type = type
		self.Blocked = blocked
		self.Blocked_orig = blocked
		self.under = None
		self.mapSubsurface = None
	
	def type(self):
		return self.Type
	
	def blocked(self):
		return self.Blocked
	
	'''
	def addEvents(self, event, mapSubsurface):
		self.Events.extend(event)
		self.genEvent(mapSubsurface)
		
		
		for each in self.Events:
	
	def genEvent(self, mapSubsurface):
		evt = self.Events[0]

		if evt.blocked:
			self.Blocked = True
		
		# get the art
		artfile, arttile = evt.imageInfo()
		artfile = pg.image.load(artfile).convert_alpha()
		
		# place it on map
		self.under = mapSubsurface.copy()
		self.mapSubsurface = mapSubsurface
		arttile = g.tile2rect(arttile, (32,32))
		mapSubsurface.blit(artfile.subsurface(arttile), (0,0))
		
		# change tile info (such as blocked)
	
	def removeEvent(self):
		# Event is finished, reinstate original blocked val
		self.Blocked = self.Blocked_orig

		del(self.Events[0])
		
		# replace old tile
		self.mapSubsurface.blit(self.under, (0,0))
		
		# call genEvent on next event if there is one
		if len(self.Events) >0:
			self.genEvent(self.mapSubsurface)
	'''
	
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
				tile = g.tile2rect((x, y), squareSize)
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
