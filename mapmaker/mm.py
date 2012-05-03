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
	WH = (700, 500)

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
	def pos_rel_to_ts(pos): return (pos[0]-1, pos[1]-1)
	def pos_rel_to_mp(pos): return (pos[0]-ts.get_box_width()-4, pos[1]-1)
	#############################
	#############################
	#############################
	clock = pg.time.Clock()
	#############################
	#############################
	#############################
	b1_held = False
	b3_held = False
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
						ts.left_click_at(pos_rel_to_ts(pos))
						thingsChanged = True

					elif mp_rect.collidepoint(pos):
						mp.left_click_at(pos_rel_to_mp(pos), ts.selectedTile())
						thingsChanged = True
				
				elif button == 3:
					b3_held = True

					if ts_rect.collidepoint(pos):
						# ts.right_click_at(pos_rel_to_ts(pos))
						# thingsChanged = True
						pass

					elif mp_rect.collidepoint(pos):
						mp.right_click_at(pos_rel_to_mp(pos), ts.selectedTile())
						thingsChanged = True
			#############################
			#############################
			#############################
			elif evt.type == MOUSEBUTTONUP:
				button = evt.dict['button']
				pos = evt.dict['pos']

				if button == 1:
					b1_held = False

					if ts_rect.collidepoint(pos):
						ts.left_release_at(pos_rel_to_ts(pos))
						thingsChanged = True

					elif mp_rect.collidepoint(pos):
						mp.left_release_at(pos_rel_to_mp(pos))
						thingsChanged = True
				
				elif button == 3:
					b3_held = False
			#############################
			#############################
			#############################
		if b1_held:
			pos = pg.mouse.get_pos()

			if ts_rect.collidepoint(pos):
				ts.left_hold_at(pos_rel_to_ts(pos))
				thingsChanged = True

			elif mp_rect.collidepoint(pos):
				mp.left_hold_at(pos_rel_to_mp(pos))
				thingsChanged = True
		#############################
		#############################
		#############################
		if b3_held:
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

		# the colors of the scroll bar
		self.SB_COLOR = (240,240,240)
		self.B_COLOR  = (150,150,150)
		self.BR_COLOR = (180,180,180)

		# surface minus what belongs to SBs
		# relative to box
		self.surf_rect = pg.Rect((0,0), (surf.get_width()-self.SB_WIDTH, surf.get_height()-self.SB_WIDTH))
		self.surf = surf.subsurface(self.surf_rect)

		# hSB surfaces
		# relative to box
		self.hSB_rect = pg.Rect((0, self.get_height()), (self.get_width(), self.SB_WIDTH))
		self.hSB_surf = surf.subsurface(self.hSB_rect)
		# relative to vSB
		self.hB1_rect = pg.Rect((0,0), (self.SB_WIDTH, self.SB_WIDTH))
		self.hB1_surf = self.hSB_surf.subsurface(self.hB1_rect)
		self.hB2_rect = pg.Rect((self.hSB_rect.width-self.SB_WIDTH, 0), (self.SB_WIDTH, self.SB_WIDTH))
		self.hB2_surf = self.hSB_surf.subsurface(self.hB2_rect)
		self.hBR_rect = None
		self.hBR_surf = None
		self.h_imgpx_per_barpx = None

		self.hSB_surf.fill(self.SB_COLOR)
		self.hB1_surf.fill(self.B_COLOR)
		self.hB2_surf.fill(self.B_COLOR)

		# vSB surfaces
		# relative to box
		self.vSB_rect = pg.Rect((self.get_width(), 0), (self.SB_WIDTH, self.get_height()))
		self.vSB_surf = surf.subsurface(self.vSB_rect)
		# relative to vSB
		self.vB1_rect = pg.Rect((0,0), (self.SB_WIDTH, self.SB_WIDTH))
		self.vB1_surf = self.vSB_surf.subsurface(self.vB1_rect)
		self.vB2_rect = pg.Rect((0, self.vSB_rect.height-self.SB_WIDTH), (self.SB_WIDTH, self.SB_WIDTH))
		self.vB2_surf = self.vSB_surf.subsurface(self.vB2_rect)
		self.vBR_rect = None
		self.vBR_surf = None
		self.v_imgpx_per_barpx = None

		self.vSB_surf.fill(self.SB_COLOR)
		self.vB1_surf.fill(self.B_COLOR)
		self.vB2_surf.fill(self.B_COLOR)

		# self.vSB_surf.fill(RED)
		# self.hSB_surf.fill(GREEN)

		self.img = None
		self.img_rect = None

		self.holdingBar = None

	def get_width(self): return self.surf.get_width()
	def get_height(self): return self.surf.get_height()
	def blit(self, *args): self.surf.blit(*args)
	def fill(self, *args): self.surf.fill(*args)

	def get_box_width(self): return self.get_width() + self.SB_WIDTH
	def get_box_height(self): return self.get_height() + self.SB_WIDTH

	def setImg(self, img):
		self.img = img

		w = img.get_width()
		if img.get_width() > self.surf_rect.width:
			w = self.surf_rect.width
		h = img.get_height()
		if img.get_height() > self.surf_rect.height:
			h = self.surf_rect.height

		self.img_rect = pg.Rect((0,0), (w, h))

		self.blit(self.img.subsurface(self.img_rect), (0,0))

		h_fraction = float(self.get_width()) / img.get_width()
		if h_fraction < 1:
			if h_fraction < 0.05:
				h_fraction = 0.05

			h_maxbarsize = (self.hSB_rect.width - self.hB1_rect.width - self.hB2_rect.width)
			h_barsize = int(h_maxbarsize * h_fraction)

			self.hBR_rect = pg.Rect((self.SB_WIDTH, 0), (h_barsize, self.SB_WIDTH))
			self.hBR_surf = self.hSB_surf.subsurface(self.hBR_rect)

			self.hBR_surf.fill(self.BR_COLOR)

			self.h_imgpx_per_barpx = (img.get_width()-self.get_width()) / float(h_maxbarsize - h_barsize)


		v_fraction = float(self.get_height()) / img.get_height()
		if v_fraction < 1:
			if v_fraction < 0.05:
				v_fraction = 0.05
			v_maxbarsize = (self.vSB_rect.height - self.vB1_rect.height - self.vB2_rect.height)
			v_barsize = int(v_maxbarsize * v_fraction)

			self.vBR_rect = pg.Rect((0, self.SB_WIDTH), (self.SB_WIDTH, v_barsize))
			self.vBR_surf = self.vSB_surf.subsurface(self.vBR_rect)

			self.vBR_surf.fill(self.BR_COLOR)

			self.v_imgpx_per_barpx = (img.get_height()-self.get_height()) / float(v_maxbarsize - v_barsize)

	def rel2abs_pos(self, pos): #relative to where it's scrolled to
		return (pos[0] + self.img_rect.left, pos[1] + self.img_rect.top)

	def abs2rel_pos(self, pos):
		return (pos[0] - self.img_rect.left, pos[1] - self.img_rect.top)

	def refreshRelImg(self):
		self.fill(GRAY)
		self.blit(self.img.subsurface(self.img_rect), (0,0))

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

			if not (self.hBR_rect.left + pixChange > self.hB1_rect.width):
				pixChange = self.hB1_rect.width - self.hBR_rect.left
			elif not (self.hBR_rect.right + pixChange <= self.hSB_rect.width - self.hB2_rect.width):
				pixChange = (self.hSB_rect.width - self.hB2_rect.width) - self.hBR_rect.right

			self.hBR_rect = pg.Rect((self.hBR_rect.left + pixChange, self.hBR_rect.top), self.hBR_rect.size)
			self.hBR_surf = self.hSB_surf.subsurface(self.hBR_rect)

			self.hSB_surf.fill(self.SB_COLOR)
			self.hB1_surf.fill(self.B_COLOR)
			self.hB2_surf.fill(self.B_COLOR)
			self.hBR_surf.fill(self.BR_COLOR)

			self.holdingBar = (self.holdingBar[0], pos[0])


			barOver_px = self.hBR_rect.left - self.hB1_rect.width
			imgShift = int(barOver_px * self.h_imgpx_per_barpx)
			self.img_rect = pg.Rect((imgShift, self.img_rect.top), self.img_rect.size)
			self.refreshRelImg()

		elif self.holdingBar[0] == "v":
			pixChange = pos[1] - self.holdingBar[1]

			if not (self.vBR_rect.top + pixChange > self.vB1_rect.height):
				pixChange = self.vB1_rect.height - self.vBR_rect.top
			elif not (self.vBR_rect.bottom + pixChange <= self.vSB_rect.height - self.vB2_rect.height):
				pixChange = (self.vSB_rect.height - self.vB2_rect.height) - self.vBR_rect.bottom

			self.vBR_rect = pg.Rect((self.vBR_rect.left, self.vBR_rect.top + pixChange), self.vBR_rect.size)
			self.vBR_surf = self.vSB_surf.subsurface(self.vBR_rect)

			self.vSB_surf.fill(self.SB_COLOR)
			self.vB1_surf.fill(self.B_COLOR)
			self.vB2_surf.fill(self.B_COLOR)
			self.vBR_surf.fill(self.BR_COLOR)

			self.holdingBar = (self.holdingBar[0], pos[1])

			barOver_px = self.vBR_rect.top - self.vB1_rect.height
			imgShift = int(barOver_px * self.v_imgpx_per_barpx)
			self.img_rect = pg.Rect((self.img_rect.left, imgShift), self.img_rect.size)
			self.refreshRelImg()

	def left_release_at(self, pos):
		self.holdingBar = None



class TS(Box):
	def __init__(self, surf):
		Box.__init__(self, surf)

		self.ts_selected = False
		self.ts_file = None

		self.selected_tile = None

	def tsSelected(self): return self.ts_selected
	def selectedTile(self): return self.selected_tile

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

		pos = self.rel2abs_pos(pos)
		pos = pix2tile(pos)

		

		# reset the old selected tile (if it's not the first time)
		if self.selected_tile:
			#if it's the same tile do nothing
			if self.selected_tile.xy == pos:
				return

			rect = tile2rect(self.selected_tile.xy)
			self.img.blit(self.selected_tile.img, rect.topleft)

		# set the new tile
		rect = tile2rect(pos)
		self.selected_tile = Tile(self.ts_file, pos, self.img.subsurface(rect).copy())

		# highlight the new tile
		surf = pg.Surface(TILE_RES)
		surf.fill(BLACK)
		surf.set_alpha(100)
		self.img.blit(surf, rect.topleft)

		self.refreshRelImg()

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

		self.currentZ = 0

		self.pos_z_tile = {}

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

			#fill up the tile dict
			for i in range(x):
				for j in range(y):
					self.pos_z_tile[(i,j)] = {}

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

		if tile is None:
			return

		tile_img = tile.img.copy()

		# prepare the image by drawing the graph lines
		pg.draw.line(tile_img, BLACK, (0, 0), (TILE_RES[0]-1, 0))
		pg.draw.line(tile_img, BLACK, (0, 0), (0, TILE_RES[1]-1))

		# blit the tile to the img
		pos = self.rel2abs_pos(pos)
		self.img.blit(tile_img, pix2tile2rect(pos))

		self.refreshRelImg()

		# put it in the tile dict
		tile.place(pix2tile(pos), self.currentZ, False)
		self.pos_z_tile[pix2tile(pos)][self.currentZ] = tile

	def right_click_at(self, pos, tile):
		originalImg = tile.img.copy()

		#make red square
		surf = pg.Surface(TILE_RES)
		surf.fill(RED)
		surf.set_alpha(50)
		#put it on the tile img
		tile.img.blit(surf, (0,0))

		self.left_click_at(pos, tile)

		tile.blocked = True
		tile.img = originalImg
		print self.pos_z_tile[pix2tile(pos)][self.currentZ].blocked



	# def left_hold_at(self, pos):
	# 	if self.surf_rect.collidepoint(pos):
	# 		pass
	# 	else:
	# 		Box.left_hold_at(pos)

class Tile:
	def __init__(self, tileset, xy, img):
		self.ts = tileset #the files the tile comes from
		self.xy = xy #the xy tile coord of the tile img
		self.img = img #th surface (image) of the tile

		self.pos = None #the location on the map
		self.z = None #what z the tile is on
		self.blocked = None #whether or not the tile is blocked

	def place(self, pos, z, blocked):
		self.pos = pos
		self.z = z
		self.blocked = blocked


if __name__ == '__main__': runMaker()