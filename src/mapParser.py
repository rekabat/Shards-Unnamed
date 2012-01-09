import pygame as pg
import general as g
import map

def parse(file_base):
	file = file_base + '.map'

	theMap = [line.strip() for line in open(file, 'r').readlines()]
	
	line = 1

	tileFiles = []
	while not theMap[line].startswith(">>>"):
		tileFiles.append(theMap[line])
		line+=1
	for i in range(len(tileFiles)):
		number, temp = tileFiles[i].split("-> ")
		number = int(number)
		source, xy = temp.split(" [")
		xy = xy[:-1].split(":")
		xy = (int(xy[0]), int(xy[1]))
		tileFiles[i]=source
		#check that all tileFiles have same res and that they match the given res
		if xy != g.TILE_RES:
			print "Warning: Tile size inconsistency from tile files"
			raise KeyboardInterrupt
	
	for i in range(len(tileFiles)):
		tileFiles[i] = TileMap(tileFiles[i], g.TILE_RES)

	line+=1

	mapSize = tuple([int(i) for i in theMap[line].split(":")])

	line+=2

	onward = line

	setup={}
	for line in theMap[onward:]:
		posOnMap, tiles = line.split("+")
		posOnMap = posOnMap.split(":")
		posOnMap = (int(posOnMap[0]), int(posOnMap[1]))

		tiles = tiles.split("|")

		setup[posOnMap] = []
		for each in tiles:
			source, temp = each.split("->")
			source = int(source)

			posOnTileFile, temp = temp.split("(")
			posOnTileFile = posOnTileFile.split(":")
			posOnTileFile = (int(posOnTileFile[0]), int(posOnTileFile[1]))

			blocked, zs = temp.split(")[")
			blocked = True if blocked == "1" else False

			zs=[int(z) for z in zs[:-1].split(",")]

			setup[posOnMap].append(map.Tile(source, posOnTileFile, blocked, zs, posOnMap))
		
	for pos in setup.keys():
		for each in setup[pos]:
			each.setArt(tileFiles[each.source()].get(each.type()))

	mapSizePx = (mapSize[0]*g.TILE_RES[0], mapSize[1]*g.TILE_RES[1])

	return {'mapSize':mapSize, 'mapSizePx': mapSizePx, 'setup':setup}

	
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
				tile = g.tile2rect((x, y))
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
