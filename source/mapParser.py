import pygame

TILE_RESOLUTION = 32

def tilePos(tileCoord, squareSize): #return topleft pixel
	return (tileCoord[0]*squareSize[0], tileCoord[1]*squareSize[1])
	

def tileOntoMap(surfaceFrom, surfaceTo, topLeftFrom, topLeftTo, squareSize):
	fromRect = pygame.Rect(topLeftFrom[0], topLeftFrom[1], squareSize[0], squareSize[1])
	toRect = pygame.Rect(topLeftTo[0], topLeftTo[1], squareSize[0], squareSize[1])
	fromTile = surfaceFrom.subsurface(fromRect)
	surfaceTo.blit(fromTile, toRect)

def parseMapLine(line):
	pos, tile = line.split("/")

	# construct map position x,y coords
	pos = tuple([int(i) for i in pos.split(":")])

	# tile source position (type)
	tile = tile.split("(")
	type = tuple([int(i) for i in tile[0].split(":")])
	tile = tile[1]

	# blocked = cannot be walked on (1 is blocked)
	tile = tile.split(")[")
	blocked = True if tile[0] == "1" else False
	tile = tile[1][:-1]

	# events attached to a tile
	events = [int(i) for i in tile.split(",")]

	return pos, Tile(type, blocked, events)
	

def parse(file):
	theMap = [line.strip() for line in open(file, 'r').readlines()]
	
	tileSource = theMap[1]
	tileSize = [int(theMap[3]), int(theMap[4])]
	mapSize = [int(theMap[6]), int(theMap[7])]
	
	# setup = [[],[]]
	setup = {}
	for line in theMap[9:]:
		# first, second = each.split("/")
		# print first, second
		pos, tile = parseMapLine(line)
		setup[pos] = tile
	return tileSource, tileSize, mapSize, setup

class Tile:
	def __init__(self, type, blocked, events):
		self.Type = type
		self.Blocked = blocked
		self.Events = events
	
	def type(self):
		return self.Type
	
	def blocked(self):
		return self.Blocked

	def events(self):
		return self.Events

class Map:
	def __init__(self, file):
		self.file = file
		self.tileSource, self.tileSize, self.mapSize, self.setup = parse(self.file)
		self.img = pygame.Surface((self.mapSize[0]*self.tileSize[0], self.mapSize[1]*self.tileSize[1]))
		
		self.tileFile = pygame.image.load(self.tileSource).convert()

		for pos in self.setup.keys():
			tileOntoMap(self.tileFile, self.img, tilePos(self.setup[pos].type(), self.tileSize), tilePos(pos, self.tileSize), self.tileSize)			
		
			
	def get(self):
		return self.img
	
	def get_rect(self):
		return self.img.get_rect()
	
	def tile2pix(self,(x, y)):
		if x > self.mapSize[0] or y > self.mapSize[1] or x < 0 or y < 0:
			print "out of bounds"
			raise KeyboardInterrupt
		print (x+.5), self.tileSize[0], (y+.5), self.tileSize[1], int((x+.5)*self.tileSize[0]), int((y+.5)*self.tileSize[1])
		return (int((x+.5)*self.tileSize[0]), int((y+.5)*self.tileSize[1]))
	
	def pix2tile(self,(x,y)):
		return (int(x/self.tileSize[0]), int(y/self.tileSize[1]))
	
	def getTileSize(self):
		return self.tileSize
	
	def getTile(self, coords, pixel=True): #false means tile
		if pixel:
			return self.setup(pix2tile(coords))
		else:
			return self.setup(coords)
	
	def blocked(self, coords, pixel=True): #false means tile
		if pixel:
			return self.setup(pix2tile(coords)).blocked()
		else:
			return self.setup(coords).blocked()
