'''
1 -> select tileset
2 -> set map dimension

f -> fill
b -> block

ESC -> exit
'''

import pygame as pg
from pygame.locals import *

import Tkinter
import tkFileDialog
import os

TILE_RES = (32, 32)

def pix2tile((x,y)):
	return (int(x/TILE_RES[0]), int(y/TILE_RES[1]))
def tile2rect((x, y)):
	return pg.Rect((x * TILE_RES[0], y * TILE_RES[1]), TILE_RES)

WHITE =	(255,	255,	255)
RED =	(255,	0,		0)
GREEN =	(0,		255,	0)
BLUE =	(0,		0,		255)
BLACK = (0,		0,		0)
GRAY =	(100,	100,	100)

pg.init()
pg.display.init()

def runMaker():
	#############################
	#############################
	#############################
	WH = (1800, 800)

	screen = pg.display.set_mode(WH)
	ts = TS(screen.subsurface(pg.Rect((1,1), (WH[0]*.25, WH[1]-2))))
	mp = MP(screen.subsurface(pg.Rect((4 + ts.get_width(),1), (WH[0] - 1 - 4 - ts.get_width(), WH[1]-2))))

	screen.fill(GRAY)

	pg.draw.line(screen, BLACK, (0,0), (WH[0], 0))
	pg.draw.line(screen, BLACK, (0,0), (0, WH[1]))
	pg.draw.line(screen, BLACK, (WH[0]-1, 0), (WH[0]-1, WH[1]-1))
	pg.draw.line(screen, BLACK, (0, WH[1]-1), (WH[0]-1, WH[1]-1))

	pg.draw.line(screen, BLACK, (ts.get_width()+1, 0), (ts.get_width()+1, WH[1]))
	pg.draw.line(screen, WHITE, (ts.get_width()+2, 0), (ts.get_width()+2, WH[1]))
	pg.draw.line(screen, BLACK, (ts.get_width()+3, 0), (ts.get_width()+3, WH[1]))
	#############################
	#############################
	#############################
	clock = pg.time.Clock()
	#############################
	#############################
	#############################
	while True:
		#############################
		#############################
		#############################
		clock.tick(30)
		#############################
		#############################
		#############################
		for evt in pg.event.get():
			if evt.type == QUIT:
				endMM()

			elif evt.type == KEYDOWN:
				key = evt.dict['key']

				if key == K_1: #prompt the user for the tile file and open it up
					ts.setCurrent()

				elif key == pg.K_RETURN:
					pass

				elif key == pg.K_TAB:
					pass
				
				elif key == pg.K_ESCAPE:
					endMM()

			elif evt.type == MOUSEBUTTONUP:
				button = evt.dict['button']
				pos = evt.dict['pos']

				if button == 1:
					if (0 < pos[0]) and (pos[0] < ts.get_width()+1) \
					 and (0 < pos[1]) and (pos[1] < WH[1]-2):
						ts.left_click_at((pos[0]-1, pos[1]-1))
					elif (ts.get_width()+3 < pos[0]) and (pos[0] < WH[1]) \
					 and (0 < pos[1]) and (pos[1] < WH[1]-2):
					 	print 'working on it'
						# mp.left_click_at((pos[0]-ts.get_width()-4, pos[1]-1))
				else:
					print "other click!"
		#############################
		#############################
		#############################
		pg.display.flip()
		#############################
		#############################
		#############################

def endMM():
	quit()

class TS:
	def __init__(self, surf):
		self.surf = surf

		self.ts_selected = False
		self.ts_file = None
		self.ts_img = None

		self.selected_tile = None

	def tsSelected(self): return self.ts_selected

	def get_width(self): return self.surf.get_width()
	def get_height(self): return self.surf.get_height()
	def blit(self, *args): self.surf.blit(*args)
	def fill(self, *args): self.surf.fill(*args)

	def setCurrent(self):
		t0 = tkFileDialog.askopenfilename(initialdir = os.getcwd())

		# leave if they choose cancel
		if not t0:
			return

		# leave if it isn't a supported file type
		try:
			t1 = pg.image.load(t0).convert()
		except:
			return

		self.ts_file = t0
		self.ts_img = t1
		self.ts_selected = True

		self.selected_tile = None

		self.fill(GRAY)
		self.blit(self.ts_img, (0,0))

	def left_click_at(self, pos):
		if not self.ts_selected:
			return

		if not ((pos[0] < self.ts_img.get_width()) and (pos[1] < self.ts_img.get_height())):
			return

		self.selected_tile = pix2tile(pos)

		surf = pg.Surface(TILE_RES)
		surf.fill(GREEN)
		surf.set_alpha(50)
		rect = tile2rect(self.selected_tile)

		self.fill(GRAY)
		self.blit(self.ts_img, (0,0))
		self.blit(surf, rect)

class MP:
	def __init__(self, surf):
		self.surf = surf

	def get_width(self): return self.surf.get_width()
	def get_height(self): return self.surf.get_height()

	def blit(self, *args): self.surf.blit(*args)

if __name__ == '__main__': runMaker()