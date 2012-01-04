import pygame

TILE_RESOLUTION = 32

def tilePos(tileCoord, squareSize): #return topleft pixel
	return (tileCoord[0]*squareSize[0], tileCoord[1]*squareSize[1])
	

def tileOntoMap(surfaceFrom, surfaceTo, topLeftFrom, topLeftTo, squareSize):
	fromRect = pygame.Rect(topLeftFrom[0], topLeftFrom[1], squareSize[0], squareSize[1])
	toRect = pygame.Rect(topLeftTo[0], topLeftTo[1], squareSize[0], squareSize[1])
	fromTile = surfaceFrom.subsurface(fromRect)
	surfaceTo.blit(fromTile, toRect)
	

def parse(file):
	theMap = [line.strip() for line in open(file, 'r').readlines()]
	
	tileSource = theMap[1]
	tileSize = [int(theMap[3]), int(theMap[4])]
	mapSize = [int(theMap[6]), int(theMap[7])]
	
	setup = [[],[]]
	for each in theMap[9:]:
		# first, second = each.split("/")
		# print first, second
		setup[0].append((int(each[:each.find(':')]), int(each[each.find(':')+1:each.find('/')])))
		secondpart = each[each.find('/')+1:] 
		setup[1].append((int(secondpart[:secondpart.find(':')]), int(secondpart[secondpart.find(':')+1:])))
		
	return tileSource, tileSize, mapSize, setup

class Map:
	def __init__(self, file):
		self.file = file
		self.tileSource, self.tileSize, self.mapSize, self.setup = parse(self.file)
		self.img = pygame.Surface((self.mapSize[0]*self.tileSize[0], self.mapSize[1]*self.tileSize[1]))
		
		self.tileFile = pygame.image.load(self.tileSource).convert()
		
		for i in range(len(self.setup[0])):
			tileOntoMap(self.tileFile, self.img, tilePos(self.setup[1][i], self.tileSize), tilePos(self.setup[0][i], self.tileSize), self.tileSize)
			
		
			
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
			
			
			