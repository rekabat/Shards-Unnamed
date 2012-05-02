'''
1 -> select tileset
2 -> set map dimension

f -> fill
b -> block

left -> down z level
right -> up z level

ESC -> exit


right click -> delete block
left click and drag -> place blocks
'''

import pygame as pg
from pygame.locals import *

import Tkinter
import tkFileDialog
import os

# the width.height of tiles in pixels
TILE_RES = (32, 32)
def pix2tile((x,y)):
	return (int(x/TILE_RES[0]), int(y/TILE_RES[1]))
def tile2rect((x, y)):
	return pg.Rect((x * TILE_RES[0], y * TILE_RES[1]), TILE_RES)

# some color constants
WHITE =	(255,	255,	255)
RED =	(255,	0,		0)
GREEN =	(0,		255,	0)
BLUE =	(0,		0,		255)
BLACK = (0,		0,		0)
GRAY =	(200,	200,	200)

# the width of the scroll bar in pixels
SB_WIDTH = 5

pg.init()
pg.display.init()

def runMaker():
	#############################
	#############################
	#############################
	WH = (1000, 800)

	screen = pg.display.set_mode(WH)
	ts_rect = pg.Rect((1,1), (WH[0]*.25, WH[1]-2))
	mp_rect = pg.Rect((4 + ts_rect.width,1), (WH[0] - 1 - 4 - ts_rect.width, WH[1]-2))
	ts = TS(screen.subsurface(ts_rect))
	mp = MP(screen.subsurface(mp_rect))

	screen.fill(GRAY)

	pg.draw.line(screen, BLACK, (0,0), (WH[0], 0))
	pg.draw.line(screen, BLACK, (0,0), (0, WH[1]))
	pg.draw.line(screen, BLACK, (WH[0]-1, 0), (WH[0]-1, WH[1]-1))
	pg.draw.line(screen, BLACK, (0, WH[1]-1), (WH[0]-1, WH[1]-1))

	pg.draw.line(screen, BLACK, (ts.get_width()+1, 0), (ts.get_width()+1, WH[1]))
	pg.draw.line(screen, WHITE, (ts.get_width()+2, 0), (ts.get_width()+2, WH[1]))
	pg.draw.line(screen, BLACK, (ts.get_width()+3, 0), (ts.get_width()+3, WH[1]))

	pg.display.flip()
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
		thingsChanged = False
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
					thingsChanged = True

				elif key == K_2:
					mp.setSize()
					thingsChanged = True

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
					if ts_rect.collidepoint(pos):
					# if (0 < pos[0]) and (pos[0] < ts.get_width()+1) \
					#  and (0 < pos[1]) and (pos[1] < WH[1]-2):
						ts.left_click_at((pos[0]-1, pos[1]-1))
						thingsChanged = True

					elif mp_rect.collidepoint(pos):
					# elif (ts.get_width()+3 < pos[0]) and (pos[0] < WH[1]) \
					#  and (0 < pos[1]) and (pos[1] < WH[1]-2):
					 	print 'working on it'
						# mp.left_click_at((pos[0]-ts.get_width()-4, pos[1]-1))
				else:
					print "other click!"
		#############################
		#############################
		#############################
		if thingsChanged: pg.display.flip()
		#############################
		#############################
		#############################

def endMM():
	quit()

class Box:
	def __init__(self, surf):
		self.surf = surf

	def get_width(self): return self.surf.get_width()
	def get_height(self): return self.surf.get_height()
	def blit(self, *args): self.surf.blit(*args)
	def fill(self, *args): self.surf.fill(*args)

class TS(Box):
	def __init__(self, surf):
		Box.__init__(self, surf)

		self.ts_selected = False
		self.ts_file = None
		self.ts_img = None

		self.selected_tile = None

	def tsSelected(self): return self.ts_selected

	def setCurrent(self):
		master = Tkinter.Tk()
		t0 = tkFileDialog.askopenfilename(initialdir = os.getcwd())
		master.destroy()

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

class MP(Box):
	def __init__(self, surf):
		Box.__init__(self, surf)

		self.tileSize_selected = False
		self.tileSize = None

	def setSize(self):
		if self.tileSize_selected:
			print "Can't change size once you've begun."
			return

		master = Tkinter.Tk()
		master.title("Map Size")
		frame = Tkinter.Frame(master)
		frame.pack()

		r = 0
		Tkinter.Label(frame, text="Choose an x & y:").grid(row=r, column=0, columnspan=2, sticky = Tkinter.W+Tkinter.E)

		r += 1
		Tkinter.Label(frame, text="X (in tiles):").grid(row=r, column=0, columnspan=1, sticky = Tkinter.W+Tkinter.E)
		x_entry = Tkinter.Entry(frame)
		x_entry.grid(row=r,column=1,columnspan=1,stick=Tkinter.W+Tkinter.E)

		r += 1
		Tkinter.Label(frame, text="Y (in tiles):").grid(row=r, column=0, columnspan=1, sticky = Tkinter.W+Tkinter.E)
		y_entry = Tkinter.Entry(frame)
		y_entry.grid(row=r,column=1,columnspan=1,stick=Tkinter.W+Tkinter.E)

		r += 1
		def submit():
			try:
				x = int(x_entry.get())
				y = int(y_entry.get())
			except:
				print "must be numbers"
				return

			self.tileSize = (x, y)
			self.tileSize_selected = True
			master.destroy()

			print self.tileSize
			
		submit_button = Tkinter.Button(frame, text='Submit', fg='black', command=submit)
		submit_button.grid(row=r,column=0,columnspan=2, sticky = Tkinter.W+Tkinter.E)

		master.mainloop()





if __name__ == '__main__': runMaker()