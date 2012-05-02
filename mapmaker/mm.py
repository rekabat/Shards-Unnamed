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
import tkMessageBox

import os

# the width.height of tiles in pixels
TILE_RES = (32, 32)
def tile2rect((x, y)):
	return pg.Rect((x * TILE_RES[0], y * TILE_RES[1]), TILE_RES)
def pix2tile((x,y)):
	return (int(x/TILE_RES[0]), int(y/TILE_RES[1]))
def pix2tile2rect((x,y)):
	return tile2rect(pix2tile((x,y)))

# some color constants
WHITE =	(255,	255,	255)
RED =	(255,	0,		0)
GREEN =	(0,		255,	0)
BLUE =	(0,		0,		255)
BLACK = (0,		0,		0)
GRAY =	(200,	200,	200)

pg.init()
pg.display.init()

def runMaker():
	#############################
	#############################
	#############################
	WH = (1000, 800)

	screen = pg.display.set_mode(WH)

	screen.fill(GRAY)

	ts_rect = pg.Rect((1,1), (WH[0]*.25, WH[1]-2))
	mp_rect = pg.Rect((4 + ts_rect.width,1), (WH[0] - 1 - 4 - ts_rect.width, WH[1]-2))
	ts = TS(screen.subsurface(ts_rect))
	mp = MP(screen.subsurface(mp_rect))

	pg.draw.line(screen, BLACK, (0,0), (WH[0], 0))
	pg.draw.line(screen, BLACK, (0,0), (0, WH[1]))
	pg.draw.line(screen, BLACK, (WH[0]-1, 0), (WH[0]-1, WH[1]-1))
	pg.draw.line(screen, BLACK, (0, WH[1]-1), (WH[0]-1, WH[1]-1))

	pg.draw.line(screen, BLACK, (ts.get_box_width()+1, 0), (ts.get_box_width()+1, WH[1]))
	pg.draw.line(screen, WHITE, (ts.get_box_width()+2, 0), (ts.get_box_width()+2, WH[1]))
	pg.draw.line(screen, BLACK, (ts.get_box_width()+3, 0), (ts.get_box_width()+3, WH[1]))

	pg.display.flip()
	#############################
	#############################
	#############################
	clock = pg.time.Clock()
	#############################
	#############################
	#############################
	b1_held = False
	b2_held = False
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
			#############################
			#############################
			#############################
			if evt.type == QUIT:
				endMM()
			#############################
			#############################
			#############################
			elif evt.type == KEYDOWN:
				key = evt.dict['key']

				if key == K_1: #prompt the user for the tile file and open it up
					ts.setCurrent()
					thingsChanged = True

				elif key == K_2:
					mp.setSize()
					thingsChanged = True
				
				elif key == pg.K_ESCAPE:
					endMM()
			#############################
			#############################
			#############################
			elif evt.type == MOUSEBUTTONDOWN:
				button = evt.dict['button']
				pos = evt.dict['pos']

				if button == 1:
					b1_held = True

					if ts_rect.collidepoint(pos):
						ts.left_click_at((pos[0]-1, pos[1]-1))
						thingsChanged = True

					#CANT MOVE THE BAR UNLESS TS IS SLECETED AND A SPECIFIC TILE
					elif mp_rect.collidepoint(pos):
						if ts.tsSelected() and ts.selectedTile()[0]:
							mp.left_click_at((pos[0]-ts.get_box_width()-4, pos[1]-1), ts.selectedTile())
							thingsChanged = True
				
				elif button == 2:
					b2_held = True
			#############################
			#############################
			#############################
			elif evt.type == MOUSEBUTTONUP:
				button = evt.dict['button']
				pos = evt.dict['pos']

				if button == 1:
					b1_held = False

					if ts_rect.collidepoint(pos):
						ts.left_release_at(pos)
						thingsChanged = True

					elif mp_rect.collidepoint(pos):
						mp.left_release_at(pos)
						thingsChanged = True
				
				elif button == 2:
					b2_held = False
			#############################
			#############################
			#############################
		if b1_held:
			pos = pg.mouse.get_pos()

			if ts_rect.collidepoint(pos):
				ts.left_hold_at((pos[0]-1, pos[1]-1))
				thingsChanged = True

			elif mp_rect.collidepoint(pos):
				mp.left_hold_at((pos[0]-ts.get_box_width()-4, pos[1]-1))
				thingsChanged = True
		#############################
		#############################
		#############################
		if b2_held:
			pass
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
		# the width of the scroll bar in pixels
		self.SB_WIDTH = 17

		# surface minus what belongs to SBs
		# relative to box
		self.surf_rect = pg.Rect((0,0), (surf.get_width()-self.SB_WIDTH, surf.get_height()-self.SB_WIDTH))
		self.surf = surf.subsurface(self.surf_rect)

		# SB surfaces
		#relative to box
		self.vSB_rect = pg.Rect((self.get_width(), 0), (self.SB_WIDTH, self.get_height()))
		self.vSB_surf = surf.subsurface(self.vSB_rect)
		#relative to vSB
		self.vB1_rect = pg.Rect((0,0), (self.SB_WIDTH, self.SB_WIDTH))
		self.vB1_surf = self.vSB_surf.subsurface(self.vB1_rect)
		self.vB2_rect = pg.Rect((0, self.vSB_rect.height-self.SB_WIDTH), (self.SB_WIDTH, self.SB_WIDTH))
		self.vB2_surf = self.vSB_surf.subsurface(self.vB2_rect)
		self.vBR_rect = None
		self.vBR_surf = None

		self.vSB_surf.fill(WHITE)
		self.vB1_surf.fill(RED)
		self.vB2_surf.fill(GREEN)

		self.hSB_rect = pg.Rect((0, self.get_height()), (self.get_width(), self.SB_WIDTH))
		self.hSB_surf = surf.subsurface(self.hSB_rect)
		#relative to vSB
		self.hB1_rect = pg.Rect((0,0), (self.SB_WIDTH, self.SB_WIDTH))
		self.hB1_surf = self.hSB_surf.subsurface(self.hB1_rect)
		self.hB2_rect = pg.Rect((self.hSB_rect.width-self.SB_WIDTH, 0), (self.SB_WIDTH, self.SB_WIDTH))
		self.hB2_surf = self.hSB_surf.subsurface(self.hB2_rect)
		self.hBR_rect = None
		self.hBR_surf = None

		self.hSB_surf.fill(WHITE)
		self.hB1_surf.fill(RED)
		self.hB2_surf.fill(GREEN)

		# self.vSB_surf.fill(RED)
		# self.hSB_surf.fill(GREEN)

		self.img = None
		self.img_tl = None
		self.img_wh = None

		self.holdingBar = None

	def get_width(self): return self.surf.get_width()
	def get_height(self): return self.surf.get_height()
	def blit(self, *args): self.surf.blit(*args)
	def fill(self, *args): self.surf.fill(*args)

	def get_box_width(self): return self.get_width() + self.SB_WIDTH
	def get_box_height(self): return self.get_height() + self.SB_WIDTH

	def setImg(self, img):
		self.img = img

		self.img_tl = (0,0)
		self.img_wh = (img.get_width(), img.get_height())

		h_fraction = float(self.get_width()) / img.get_width()
		if h_fraction < 1:
			h_maxbarsize = (self.hSB_rect.width - self.hB1_rect.width - self.hB2_rect.width)
			h_barsize = int(h_maxbarsize * h_fraction)

			self.hBR_rect = pg.Rect((self.SB_WIDTH, 0), (h_barsize, self.SB_WIDTH))
			self.hBR_surf = self.hSB_surf.subsurface(self.hBR_rect)

			self.hBR_surf.fill(BLUE)

			imgh_per_pixel = img.get_height() / (h_maxbarsize - h_barsize)


		v_fraction = float(self.get_height()) / img.get_height()
		if v_fraction < 1:
			v_maxbarsize = (self.vSB_rect.height - self.vB1_rect.height - self.vB2_rect.height)
			v_barsize = int(v_maxbarsize * v_fraction)

			self.vBR_rect = pg.Rect((0, self.SB_WIDTH), (self.SB_WIDTH, v_barsize))
			self.vBR_surf = self.vSB_surf.subsurface(self.vBR_rect)

			self.vBR_surf.fill(BLUE)

			imgh_per_pixel = img.get_height() / (v_maxbarsize - v_barsize)

	def left_click_at(self, pos):
		if self.hSB_rect:
			if self.hSB_rect.collidepoint(pos):
				self.holdingBar = ("h", pos[0])
				return
		if self.vSB_rect:
			if self.vSB_rect.collidepoint(pos):
				self.holdingBar = ("v", pos[1])
				return

	def left_hold_at(self, pos):
		if not self.holdingBar:
			return
		elif self.holdingBar[0] == "h":
			pixChange = pos[0] - self.holdingBar[1]
		elif self.holdingBar[0] == "v":
			pixChange = pos[1] - self.holdingBar[1]

		print pixChange

	def left_release_at(self, pos):
		self.holdingBar = None








class TS(Box):
	def __init__(self, surf):
		Box.__init__(self, surf)

		self.ts_selected = False
		self.ts_file = None

		self.selected_tile = None
		self.selected_tile_img = None

	def tsSelected(self): return self.ts_selected
	def selectedTile(self): return (self.selected_tile, self.selected_tile_img)

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
		self.setImg(t1)
		self.ts_selected = True

		self.selected_tile = None

		self.fill(GRAY)
		self.blit(self.img, (0,0))

	def left_click_at(self, pos):
		if not self.ts_selected:
			return

		if not self.surf_rect.collidepoint(pos):
			Box.left_click_at(self, pos)
			return
		elif not ((pos[0] < self.img.get_width()) and (pos[1] < self.img.get_height())):
			return

		self.selected_tile = pix2tile(pos)

		surf = pg.Surface(TILE_RES)
		surf.fill(GREEN)
		surf.set_alpha(50)
		rect = tile2rect(self.selected_tile)

		self.selected_tile_img = self.img.subsurface(rect).copy()

		self.fill(GRAY)
		self.blit(self.img, (0,0))
		self.blit(surf, rect)

	# def left_hold_at(self, pos):
	# 	if self.surf_rect.collidepoint(pos):
	# 		pass
	# 	else:
	# 		Box.left_hold_at(pos)
	# 		return

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
			failed = False

			try:
				x = int(x_entry.get())
				y = int(y_entry.get())

				if x < 1 or y < 1:
					failed = True
			except:
				failed = True

			if failed:
				tkMessageBox.showerror("X/Y Error", "X and Y must be positive integers.")
				return

			master.destroy()

			self.tileSize = (x, y)
			self.tileSize_selected = True

			self.setImg(pg.Surface((TILE_RES[0]*x + 1, TILE_RES[1]*y + 1))) # +1 for the last gridline
			self.img.fill(GRAY)

			for i in range(x+1):
				pg.draw.line(self.img, BLACK, (i*TILE_RES[0], 0), (i*TILE_RES[0], self.img.get_height()-1))
			for i in range(y+1):
				pg.draw.line(self.img, BLACK, (0, i*TILE_RES[1]), (self.img.get_width()-1, i*TILE_RES[1]))

			self.blit(self.img, (0,0))

		submit_button = Tkinter.Button(frame, text='Submit', fg='black', command=submit)
		submit_button.grid(row=r,column=0,columnspan=2, sticky = Tkinter.W+Tkinter.E)

		master.mainloop()

	def left_click_at(self, pos, tile):
		if not self.tileSize_selected:
			return

		if not self.surf_rect.collidepoint(pos):
			Box.left_click_at(self, pos)
			return
		elif not ((pos[0] < self.img.get_width()) and (pos[1] < self.img.get_height())):
			return

		tile_xy = tile[0]
		tile_img = tile[1]

		pg.draw.line(tile_img, BLACK, (0, 0), (TILE_RES[0]-1, 0))
		pg.draw.line(tile_img, BLACK, (0, 0), (0, TILE_RES[1]-1))

		self.img.blit(tile_img, pix2tile2rect(pos))

		self.blit(self.img, (0,0))

	# def left_hold_at(self, pos):
	# 	if self.surf_rect.collidepoint(pos):
	# 		pass
	# 	else:
	# 		Box.left_hold_at(pos)





if __name__ == '__main__': runMaker()