import pygame as pg
from pygame.locals import *

import mapParser
import general as g

class Map:
	def __init__(self, file, screenres):
		self.screenres = screenres
		self.file = file + ".map"
		self.evtFile = file + ".evt"

		mapData = mapParser.parse(file)

		self.mapSizeTiles = mapData['mapSize']
		self.mapSizePx = mapData['mapSizePx']
		self.maxZ = mapData['maxZ']

		if self.screenres[0] > self.mapSizePx[0]:
			x = int((self.screenres[0]-self.mapSizePx[0])/2.)
			w = self.screenres[0]
		else:
			x = 0
			w = self.mapSizePx[0]
		if self.screenres[1] > self.mapSizePx[1]:
			y = int((self.screenres[1]-self.mapSizePx[1])/2.)
			h = self.screenres[1]
		else:
			y=0
			h = self.mapSizePx[1]
		self.drawingSize = (w,h)
		self.mapDrawingDif = (x,y)
		self.mapRectOnImg = pg.Rect((x,y), self.mapSizePx)


		#dictionary where key = pos, gives dict where key = z, gives tile
		self.pos_z_tile = mapData['setup']

		#dictionary where key = z, gives dict where key = pos, gives tile
		self.z_pos_tile = {}
		for z in range(self.maxZ+1):
			self.z_pos_tile[z] = {}
		for pos in self.pos_z_tile:
			for z in self.pos_z_tile[pos]:
				self.z_pos_tile[z][pos] = self.pos_z_tile[pos][z]


	def getMapSizePx(self): return self.mapSizePx
	def getMapSizeTiles(self): return self.mapSizeTiles
	def getDrawingSize(self): return self.drawingSize
	def getMapDrawingDif(self): return self.mapDrawingDif
	# def getDict_Z_Pos_gives_Blocked(self): return self.zsetup2_blocked

	def getTotalImg(self):
		img = pg.Surface(self.drawingSize)
		zimg = img.subsurface(self.mapRectOnImg)
		
		for z in range(self.maxZ+1):
			for pos in self.z_pos_tile[z]:
				tile = self.z_pos_tile[z][pos]
				zimg.blit(tile.getImg(), tile.getRect())
		
		return img

	def pix2tile(self, pix):
		return g.pix2tile((pix[0]-self.mapDrawingDif[0], pix[1]-self.mapDrawingDif[1]))
	def tile2rect(self, (x,y)):
		return pg.Rect((x * g.TILE_RES[0] + self.mapDrawingDif[0], y * g.TILE_RES[1] + self.mapDrawingDif[1]), g.TILE_RES)

	def getTile(self, coords, z, pixel=True): #false means tile
		if pixel:
			coords = g.pix2tile(coords)
		# print coords
		# if coords in self.zsetup2[z].keys():
		#     return self.zsetup2[z][coords]
		# else:
		#     return False
		try:
			return self.z_pos_tile[z][coords]
		except:
			return False
	
	def blocked(self, rect, z):#coords, pixel=True): #false means tile
		corners = (g.pix2tile(rect.topleft), \
			g.pix2tile(rect.topright), \
			g.pix2tile(rect.bottomleft), \
			g.pix2tile(rect.bottomright) )
		for corner in corners:
			try: #if a tile exists at this z and IS blocked, return true
				if self.z_pos_tile[z][corner].blocked():
					return True
			except: #if a tile doesn't exist at this z, return true (it is blocked here)
				return True
		return False

	# def blocked_tile(self, tile, zlist):
	#     ret = True
	#     for z in zlist:
	#         blockedAtThisZ = False
	#         try: #if a tile exists at this z and IS blocked, return true
	#             bl = self.zsetup2[z][tile].blocked()
	#             blockedAtThisZ = blockedAtThisZ or bl
	#         except: #if a tile doesn't exist at this z, return true (it is blocked here)
	#             blockedAtThisZ = True
	#             break
	#         ret = ret and blockedAtThisZ
	#     return ret

	
	def tileExists(self,rect,z):
		corners = (g.pix2tile(rect.topleft), \
			g.pix2tile(rect.topright), \
			g.pix2tile(rect.bottomleft), \
			g.pix2tile(rect.bottomright) )
		for corner in corners:
			if corner not in self.z_pos_tile[z].keys():
				return False
		return True

	def getTilesInRect(self, rect): #assumes rect is size 1 tile, returns all tiles in rect from all zs
		tl = g.pix2tile(rect.topleft)
		br = g.pix2tile(rect.bottomright)

		ret = []

		i = tl[0]
		while i<=br[0] and i<self.mapSizeTiles[0] and i>=0:
			j = tl[1]
			while j<=br[1] and j<self.mapSizeTiles[1] and j>=0:
				for z in self.pos_z_tile[(i,j)]:
					ret.append(self.pos_z_tile[(i,j)][z])
				j+=1
			i+=1
				
		return ret

class Tile:
	def __init__(self, img, blocked, posOnMap, z):
		self.img = img
		self.Blocked = blocked
		self.rect = g.tile2rect(posOnMap)
		self.z = z
	
	def getImg(self): return self.img
	def blocked(self): return self.Blocked
	def getRect(self): return self.rect
	def getZ(self): return self.z