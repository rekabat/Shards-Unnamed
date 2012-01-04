import pygame

TILE_RESOLUTION = 32

def tilePos(tileCoord, squareSize): #return topleft pixel
	return (tileCoord[0]*squareSize[0], tileCoord[1]*squareSize[1])

def tileOntoMap(surfaceFrom, surfaceTo, topLeftFrom, topLeftTo, squareSize):
	# fromRect = pygame.Rect(topLeftFrom[0], topLeftFrom[1], squareSize[0], squareSize[1])
	# toRect = pygame.Rect(topLeftTo[0], topLeftTo[1], squareSize[0], squareSize[1])
	# fromTile = pygame.Surface((squareSize[0], squareSize[1]))
	
	for i in range(squareSize[0]):
		for j in range(squareSize[1]):
			surfaceTo.set_at((topLeftTo[0]+i, topLeftTo[1]+j), surfaceFrom.get_at((topLeftFrom[0]+i, topLeftFrom[1]+j)))
	# fromTile.blit(surfaceFrom, fromRect)
	# surfaceTo.blit(fromTile, toRect)

def parse(file):
	theMap = [line.strip() for line in open(file).readlines()]
	
	tileSource = theMap[1]
	tileSize = [int(theMap[3]), int(theMap[4])]
	mapSize = [int(theMap[6]), int(theMap[7])]
	
	setup = [[],[]]
	for each in theMap[9:]:
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
