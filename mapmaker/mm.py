'''
1 -> select tileset
2 -> set map dimension
3 -> save map

f -> fill

~left -> down z level
~right -> up z level

ESC -> exit


(on tileset)
left click ->  select a tile (unblocked)
right click -> select a tile (blocked)

(on map)
left click -> place a tile
right click -> remove a tile
left click and drag -> place tiles



THINGS TO ADD:
) loading maps
) deleting tiles needs to leave the image from lower zs instead of erasing it too
		(but it will come back as soon as you change zs again)
) make z levels below you slightly transparent
) exiting should prompt to save more intelligently (asks if you scroll on map)
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

#some folder constants
MAPART_DIR 	= "../art/map/"
SAVE_DIR	= "../maps/"

pg.init()
pg.display.init()

def runMaker():
	#############################
	#############################
	#############################
	WH = (700, 500)

	screen = pg.display.set_mode(WH)
	# pg.display.set_icon(pg.image.load('icon.png').convert())
	pg.display.set_caption('Shattered Map Maker (ShaMM)')

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

	saved = True
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
				endMM(saved)
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
					saved = False

				elif key == K_3:
					saved = mp.saveMap()

				elif key = K_4:
					mp.loadMap()
					thingsChanged = True

				elif key == K_f:
					mp.fillWith(ts.selectedTile())
					thingsChanged = True
					saved = False

				elif key == K_RIGHT or key == K_UP:
					mp.changeZLevel(1)
					thingsChanged = True

				elif key == K_LEFT or key == K_DOWN:
					mp.changeZLevel(-1)
					thingsChanged = True
				
				elif key == K_SPACE:
					pass
					# pos = pg.mouse.get_pos()

					# if mp_rect.collidepoint(pos):
					# 	mp.space_at(pos_rel_to_mp(pos))
					# 	thingsChanged = True

				elif key == pg.K_ESCAPE:
					endMM(saved)
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
						saved = False
				
				elif button == 3:
					b3_held = True

					if ts_rect.collidepoint(pos):
						ts.right_click_at(pos_rel_to_ts(pos))
						thingsChanged = True

					elif mp_rect.collidepoint(pos):
						mp.right_click_at(pos_rel_to_mp(pos))
						thingsChanged = True
						saved = False
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
				mp.left_hold_at(pos_rel_to_mp(pos), ts.selectedTile())
				thingsChanged = True
				saved = False
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

def endMM(saved):
	if not saved:
		master = Tkinter.Tk()
		t0 = tkMessageBox.askyesno("Exit", "Are you sure you want to exit without saving?")
		master.destroy()

		if t0:
			quit()
		else:
			return
	else:
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
		t0 = os.path.relpath(tkFileDialog.askopenfilename(initialdir = MAPART_DIR))
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

	def left_click_at(self, pos, highlight = GREEN):
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
			# #if it's the same tile do nothing
			# if self.selected_tile.xy == pos:
			# 	return

			# not anymore because you can right click to make it blocked

			rect = tile2rect(self.selected_tile.xy)
			self.img.subsurface(rect).fill(GRAY)
			self.img.blit(self.selected_tile.img, rect.topleft)

		# set the new tile
		rect = tile2rect(pos)
		self.selected_tile = Tile(self.ts_file, pos, self.img.subsurface(rect).copy())

		if highlight is GREEN:
			self.selected_tile.setBlocked(False)
		elif highlight is RED:
			self.selected_tile.setBlocked(True)
		else:
			print "invalid color choice for highlight/block"


		# highlight the new tile
		surf = pg.Surface(TILE_RES)
		surf.fill(highlight)
		surf.set_alpha(75)
		self.img.blit(surf, rect.topleft)

		self.refreshRelImg()

	def right_click_at(self, pos):
		self.left_click_at(pos, highlight = RED)

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
		self.currentZ_img = None
		self.z_img = {}

		self.gridlines = None

		self.pos_z_tile = {}

		self.leftClickOnMap = False

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

			self.currentZ_img = pg.Surface(self.img.get_size(), pg.SRCALPHA, 32).convert_alpha()

			self.gridlines = pg.Surface(self.img.get_size(), pg.SRCALPHA, 32).convert_alpha()
			for i in range(x+1):
				pg.draw.line(self.gridlines, BLACK, (i*TILE_RES[0], 0), (i*TILE_RES[0], self.img.get_height()-1))
			for i in range(y+1):
				pg.draw.line(self.gridlines, BLACK, (0, i*TILE_RES[1]), (self.img.get_width()-1, i*TILE_RES[1]))

			self.img.blit(self.gridlines, (0,0))
			self.blit(self.img, (0,0))

			#fill up the tile dict
			for i in range(x):
				for j in range(y):
					self.pos_z_tile[(i,j)] = {}

		submit_button = Tkinter.Button(frame, text='Submit', fg='black', command=submit)
		submit_button.grid(row=r,column=0,columnspan=2, sticky = Tkinter.W+Tkinter.E)

		master.mainloop()

	def left_click_at(self, pos, tile, automated_clicking = False):
		# the x/y has not been set
		if not self.tileSize_selected:
			return
		# the click was on the scroll bars BUT automated_clicking bypasses boundaries (for function fillWith)
		elif (not self.surf_rect.collidepoint(pos)) and (not automated_clicking):
			Box.left_click_at(self, pos)
			return
		#turn click on
		else:
			self.leftClickOnMap = True

		#click is outside of map but not on scroll bars (small map)
		if not ((pos[0] < self.img.get_width()) and (pos[1] < self.img.get_height())):
			return
		#clcik is right on the border (the right and bottom gridlines)
		elif (self.rel2abs_pos(pos)[0] >= self.img.get_width()-1) or (self.rel2abs_pos(pos)[1] >= self.img.get_height()-1):
			return
		#no tile has been selected yet
		elif tile is None:
			return

		tile_img = tile.img.copy()
		if tile.blocked:
			#make red square
			surf = pg.Surface(TILE_RES)
			surf.fill(RED)
			surf.set_alpha(50)
			#put it on the tile img
			tile_img.blit(surf, (0,0))

		# # prepare the image by drawing the graph lines
		# pg.draw.line(tile_img, BLACK, (0, 0), (TILE_RES[0]-1, 0))
		# pg.draw.line(tile_img, BLACK, (0, 0), (0, TILE_RES[1]-1))

		# blit the tile to the currentZ_img
		pos = self.rel2abs_pos(pos)
		rect = pix2tile2rect(pos)
		self.currentZ_img.blit(tile_img, rect)

		# place on main img: /gray, transparent z's below,/ itself, transparent zs above, gridline
		
		# for z in self.z_img:
		# 	if z > self.currentZ:
		# 		temp = self.z_img[z].subsurface(rect).convert()
		# 		temp.set_alpha(100)
		# 		tile_img.blit(temp, (0,0))
		tile_img.blit(self.gridlines.subsurface(rect), (0,0))
		self.img.blit(tile_img, rect)

		self.refreshRelImg()

		# put it in the tile dict
		tile.setCoords(pix2tile(pos), self.currentZ)
		self.pos_z_tile[pix2tile(pos)][self.currentZ] = tile

	def left_hold_at(self, pos, tile):
		if not self.leftClickOnMap:
			Box.left_hold_at(self, pos)
			return

		self.left_click_at(pos, tile)

	def left_release_at(self, pos):
		if not self.leftClickOnMap:
			Box.left_hold_at(self, pos)
			return

		self.leftClickOnMap = False

	def right_click_at(self, pos):
		if not self.tileSize_selected:
			return

		if not self.surf_rect.collidepoint(pos):
			return
		elif not ((pos[0] < self.img.get_width()) and (pos[1] < self.img.get_height())):
			return

		try:
			del(self.pos_z_tile[pix2tile(pos)][self.currentZ])
		except:
			return

		#make a gray tile with graph lines
		blank = pg.Surface(TILE_RES)
		blank.fill(GRAY)
		pg.draw.line(blank, BLACK, (0, 0), (TILE_RES[0]-1, 0))
		pg.draw.line(blank, BLACK, (0, 0), (0, TILE_RES[1]-1))

		# blit the tile to the img
		pos = self.rel2abs_pos(pos)
		self.img.blit(blank, pix2tile2rect(pos))

		self.refreshRelImg()

	def fillWith(self, tile):
		if not tile:
			return
		elif not self.tileSize_selected:
			return


		master = Tkinter.Tk()
		t0 = tkMessageBox.askyesno("Fill", "Are you sure you want to fill the entire map with this? It will overwrite all spots, not just empty ones.")
		master.destroy()

		if t0:
			for i in range(self.tileSize[0]):
				for j in range(self.tileSize[1]):
					self.left_click_at((i*TILE_RES[0], j*TILE_RES[1]), tile, automated_clicking = True)

			self.left_release_at((0,0))

	def changeZLevel(self, ud):
		if not self.tileSize_selected:
			return

		if self.currentZ + ud < 0:
			return

		# save this z's image
		self.z_img[self.currentZ] = self.currentZ_img.copy()

		# go to new z and announce it
		self.currentZ += ud
		print "Z level =", self.currentZ

		try:
			#load the old z_img
			self.currentZ_img = self.z_img[self.currentZ]
		except:
			# make new currentZ_img
			self.currentZ_img = pg.Surface(self.img.get_size(), pg.SRCALPHA, 32).convert_alpha()

		# main img: gray, transparent z's below, itself, transparent zs above, gridline
		self.img.fill(GRAY)
		# for z in self.z_img:
		# 	temp = self.z_img[z] 

		# 	if z != self.currentZ:
		# 		temp = temp.copy()
		# 		temp.set_alpha(50)

		# 	self.img.blit(temp, (0,0))

		for z in self.z_img:
			if z <= self.currentZ:
				temp = self.z_img[z] 

				if z != self.currentZ:
					temp = temp.copy()
					temp.set_alpha(50)

				self.img.blit(temp, (0,0))

		self.img.blit(self.gridlines, (0,0))

		self.refreshRelImg()


	def saveMap(self):
		if not self.tileSize_selected:
			return True

		master = Tkinter.Tk()
		fileName = tkFileDialog.asksaveasfilename(initialdir = SAVE_DIR)
		master.destroy()

		# leave if they choose cancel
		if not fileName:
			return False

		# go through once to get all the unique tile sets
		tileSets = set() 
		for i in range(self.tileSize[0]):
			for j in range(self.tileSize[1]):
				try:
					for z in self.pos_z_tile[(i, j)]:
						tile = self.pos_z_tile[(i, j)][z]
						tileSets.add(tile.ts)
				except:
					pass #no tiles at this pos

		#open file
		file = open(fileName, "w")
		#give header
		file.write(">>> Tile Source [size x:y]\n")
		#add the tilesets and make a dict
		ts_number = {}
		i = 0
		for ts in tileSets:
			file.write(str(i) + "-> " + ts[3:] + " [32:32]\n") #[3:] to remove ../
			ts_number[ts] = i
			i+=1
		#give intermediate stuff
		file.write(">>> Map Size in Tiles (x/y)\n" + \
			str(self.tileSize[0])+":"+str(self.tileSize[1])+"\n" + \
			">>> Setup (Source-> Map col:row/Tile col:row)")

		# go through once more to fill file
		for i in range(self.tileSize[0]):
			for j in range(self.tileSize[1]):
				# position on map
				k = 0
				line = "\n" + str(i)+":"+str(j)+"+"
				for z in self.pos_z_tile[(i, j)]:
					tile = self.pos_z_tile[(i, j)][z]

					#divider if there are more than one zs at this position
					if k>0:
						line += "|"

					# file number
					line += (str(ts_number[tile.ts]))+"->"
					# tile coord in tileset
					line += str(tile.xy[0]) + ":" + str(tile.xy[1])
					# blocked
					if tile.blocked:
						line += "(1)"
					else:
						line += "(0)"
					# z
					line += "[" + str(tile.z) + "]"

					k+=1

				if k > 0:
					file.write(line)

		file.close()

		return True

	def loadMap(self):
		print "working on it"


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

	def setCoords(self, pos, z):
		self.pos = pos
		self.z = z

	def setBlocked(self, blocked):
		self.blocked = blocked


if __name__ == '__main__': runMaker()