import pygame as pg
from pygame.locals import *

BAR_FRACT = 0.2

"""
player
	inventory
	~equipped
	stats
save/load
	save
	load
options
	graphics
	audio
resume
exit
	confirm
"""

class PMenu:
	def __init__(self, GI, surfaceToUse, child):
		self.GI = GI
		self.wh = surfaceToUse.get_size()

		self.whole_surf = surfaceToUse

		self.parent_rect = pg.Rect((0,0), (self.wh[0], self.wh[1] * BAR_FRACT))
		self.parent_surf = surfaceToUse.subsurface(self.parent_rect)

		self.child_rect = pg.Rect((0,self.parent_rect.height), (self.wh[0], self.wh[1] - self.parent_rect.height))
		self.child_surf = surfaceToUse.subsurface(self.child_rect)

		if child:
			self.child = child(GI, self.child_surf)
		else:
			self.child = None
	
	def makeButtons(self, lst, size):
		#lst is a list of strings that are the button texts you want
		#size is the font size you want in pixels
		#returns a list of buttons of equal size in the same order
		lst = [self.GI.font.text(l, size) for l in lst]
		maxLength = max([each.getLength() for each in lst])

		#assuming button decoration is 10 pixels in widt (20 = 10*2)
		return [makeAButton(maxLength+20+4, size+20+4, l) for l in lst]

	def dispatch(self, events):
		for evt in events:
			if evt.type == MOUSEBUTTONDOWN:
				button = evt.dict['button']
				pos = evt.dict['pos']

				if button == 1:
					self.left_click_at(pos)

	def pos_rel_to_child(self, pos):
		return (pos[0], pos[1] - self.parent_rect.height)

	def left_click_at(self, pos):
		if self.child and self.child_rect.collidepoint(pos):
			self.child.left_click_at(self.pos_rel_to_child(pos))
			return

		self.left_click_at_action(pos)

class PMenu_general(PMenu):
	def __init__(self, GI, surfaceToUse):
		PMenu.__init__(self, GI, surfaceToUse, PMenu_player)

		self.parent_surf.fill((100,100,100))

		button_list = self.makeButtons(["Player", "Save/Load", "Options", "Resume", "Quit"], 30)

		self.player_b_rect = pg.Rect((0,0), button_list[0].get_size())
		self.player_b_surf = self.parent_surf.subsurface(self.player_b_rect)
		self.player_b_surf.blit(button_list[0], (0,0))

		self.saveload_b_rect = pg.Rect((200,0), button_list[1].get_size())
		self.saveload_b_surf = self.parent_surf.subsurface(self.saveload_b_rect)
		self.saveload_b_surf.blit(button_list[1], (0,0))

		self.options_b_rect = pg.Rect((400,0), button_list[2].get_size())
		self.options_b_surf = self.parent_surf.subsurface(self.options_b_rect)
		self.options_b_surf.blit(button_list[2], (0,0))

		self.resume_b_rect = pg.Rect((600,0), button_list[3].get_size())
		self.resume_b_surf = self.parent_surf.subsurface(self.resume_b_rect)
		self.resume_b_surf.blit(button_list[3], (0,0))

		self.quit_b_rect = pg.Rect((800,0), button_list[3].get_size())
		self.quit_b_surf = self.parent_surf.subsurface(self.quit_b_rect)
		self.quit_b_surf.blit(button_list[4], (0,0))

	def getDisp(self): return self.whole_surf

	def left_click_at_action(self, pos):
		if self.player_b_rect.collidepoint(pos):
			self.child = PMenu_player(self.GI, self.child_surf)
		elif self.saveload_b_rect.collidepoint(pos):
			self.child = PMenu_saveload(self.GI, self.child_surf)
		elif self.options_b_rect.collidepoint(pos):
			self.child = PMenu_options(self.GI, self.child_surf)
		elif self.resume_b_rect.collidepoint(pos):
			self.GI.dispatch([pg.event.Event(KEYDOWN, {'key': K_ESCAPE})])
		elif self.quit_b_rect.collidepoint(pos):
			self.child = PMenu_quit(self.GI, self.child_surf)
		else:
			print "oh yeah! general!", pos

class PMenu_player(PMenu):
	def __init__(self, GI, surfaceToUse):
		PMenu.__init__(self, GI, surfaceToUse, PMenu_inventory)

		self.parent_surf.fill((100,100,200))

		button_list = self.makeButtons(["Inventory", "Stats"], 30)

		self.inventory_b_rect = pg.Rect((0,0), button_list[0].get_size())
		self.inventory_b_surf = self.parent_surf.subsurface(self.inventory_b_rect)
		self.inventory_b_surf.blit(button_list[0], (0,0))

		self.stats_b_rect = pg.Rect((200,0), button_list[1].get_size())
		self.stats_b_surf = self.parent_surf.subsurface(self.stats_b_rect)
		self.stats_b_surf.blit(button_list[1], (0,0))

	def left_click_at_action(self, pos):
		if self.inventory_b_rect.collidepoint(pos):
			self.child = PMenu_inventory(self.GI, self.child_surf)
		elif self.stats_b_rect.collidepoint(pos):
			self.child = PMenu_stats(self.GI, self.child_surf)
		else:
			print "oh yeah! player!", pos

class PMenu_inventory(PMenu):
	def __init__(self, GI, surfaceToUse):
		PMenu.__init__(self, GI, surfaceToUse, None)

		self.whole_surf.fill((200,100,100))

	def left_click_at_action(self, pos):
		print "oh yeah! inventory!", pos

class PMenu_stats(PMenu):
	def __init__(self, GI, surfaceToUse):
		PMenu.__init__(self, GI, surfaceToUse, None)

		self.whole_surf.fill((200,200,100))

	def left_click_at_action(self, pos):
		print "oh yeah! stats!", pos

class PMenu_saveload(PMenu):
	def __init__(self, GI, surfaceToUse):
		PMenu.__init__(self, GI, surfaceToUse, PMenu_save)

		self.parent_surf.fill((100,100,200))

		button_list = self.makeButtons(["Save", "Load"], 30)

		self.save_b_rect = pg.Rect((0,0), button_list[0].get_size())
		self.save_b_surf = self.parent_surf.subsurface(self.save_b_rect)
		self.save_b_surf.blit(button_list[0], (0,0))

		self.load_b_rect = pg.Rect((200,0), button_list[1].get_size())
		self.load_b_surf = self.parent_surf.subsurface(self.load_b_rect)
		self.load_b_surf.blit(button_list[1], (0,0))

	def left_click_at_action(self, pos):
		if self.save_b_rect.collidepoint(pos):
			self.child = PMenu_save(self.GI, self.child_surf)
		elif self.load_b_rect.collidepoint(pos):
			self.child = PMenu_load(self.GI, self.child_surf)
		else:
			print "oh yeah! saveload!", pos

class PMenu_save(PMenu):
	def __init__(self, GI, surfaceToUse):
		PMenu.__init__(self, GI, surfaceToUse, None)

		self.whole_surf.fill((200,100,100))

	def left_click_at_action(self, pos):
		print "oh yeah! save!", pos

class PMenu_load(PMenu):
	def __init__(self, GI, surfaceToUse):
		PMenu.__init__(self, GI, surfaceToUse, None)

		self.whole_surf.fill((200,200,100))

	def left_click_at_action(self, pos):
		print "oh yeah! load!", pos

class PMenu_options(PMenu):
	def __init__(self, GI, surfaceToUse):
		PMenu.__init__(self, GI, surfaceToUse, PMenu_graphics)

		self.parent_surf.fill((100,200,200))

		button_list = self.makeButtons(["Graphics", "Audio"], 30)

		self.graphics_b_rect = pg.Rect((0,0), button_list[0].get_size())
		self.graphics_b_surf = self.parent_surf.subsurface(self.graphics_b_rect)
		self.graphics_b_surf.blit(button_list[0], (0,0))

		self.audio_b_rect = pg.Rect((200,0), button_list[1].get_size())
		self.audio_b_surf = self.parent_surf.subsurface(self.audio_b_rect)
		self.audio_b_surf.blit(button_list[1], (0,0))

	def left_click_at_action(self, pos):
		if self.graphics_b_rect.collidepoint(pos):
			self.child = PMenu_graphics(self.GI, self.child_surf)
		elif self.audio_b_rect.collidepoint(pos):
			self.child = PMenu_audio(self.GI, self.child_surf)
		else:
			print "oh yeah! options!", pos

class PMenu_graphics(PMenu):
	def __init__(self, GI, surfaceToUse):
		PMenu.__init__(self, GI, surfaceToUse, None)

		self.whole_surf.fill((200,100,100))

		self.button_list = self.makeButtons(["Fullscreen On", "Fullscreen Off"], 30)

		self.fullscreen_b_rect = pg.Rect((0,0), self.button_list[0].get_size())
		self.fullscreen_b_surf = self.parent_surf.subsurface(self.fullscreen_b_rect)

		if self.GI.display.isFull:
			self.fullscreen_b_surf.blit(self.button_list[1], (0,0))
		else:
			self.fullscreen_b_surf.blit(self.button_list[0], (0,0))

	def left_click_at_action(self, pos):
		if self.fullscreen_b_rect.collidepoint(pos):
			self.GI.display.toggleFull()
			if self.GI.display.isFull:
				self.fullscreen_b_surf.blit(self.button_list[1], (0,0))
			else:
				self.fullscreen_b_surf.blit(self.button_list[0], (0,0))
		else:
			print "oh yeah! graphics!", pos

class PMenu_audio(PMenu):
	def __init__(self, GI, surfaceToUse):
		PMenu.__init__(self, GI, surfaceToUse, None)

		self.whole_surf.fill((200,200,100))

	def left_click_at_action(self, pos):
		print "oh yeah! audio!", pos

class PMenu_quit(PMenu):
	def __init__(self, GI, surfaceToUse):
		PMenu.__init__(self, GI, surfaceToUse, None)

		self.whole_surf.fill((100,100,200))

		button_list = self.makeButtons(["Confirm"], 30)

		self.confirm_b_rect = pg.Rect((0,0), button_list[0].get_size())
		self.confirm_b_surf = self.parent_surf.subsurface(self.confirm_b_rect)
		self.confirm_b_surf.blit(button_list[0], (0,0))

	def left_click_at_action(self, pos):
		if self.confirm_b_rect.collidepoint(pos):
			self.GI.dispatch([pg.event.Event(QUIT, {})])
		else:
			print "oh yeah! quit!", pos

def makeAButton(width, height, text):
	width = int(width)
	height = int(height)

	button_corner = pg.image.load("art/pausemenu/button_corner.png").convert_alpha() #assumes X by X
	button_sliver = pg.image.load("art/pausemenu/button_sliver.png").convert_alpha() #assumes 1 by X

	button_color = (255, 85, 85)

	if (width < button_corner.get_width()*2) or (height < button_corner.get_height()*2):
		raise KeyboardInterrupt("Buttons can't be this small, need higher resolution.")

	#cannot have transparent corners b/c of these lines
	button = pg.Surface((width, height), SRCALPHA, 32).convert_alpha()
	button.fill(button_color)

	# place corners
	button.blit(button_corner, (0,0))
	button_corner = pg.transform.rotate(button_corner, 90)
	button.blit(button_corner, (0,height-button_corner.get_width()))
	button_corner = pg.transform.rotate(button_corner, 90)
	button.blit(button_corner, (width-button_corner.get_width(),height-button_corner.get_width()))
	button_corner = pg.transform.rotate(button_corner, 90)
	button.blit(button_corner, (width-button_corner.get_width(),0))
	button_corner = pg.transform.rotate(button_corner, 90)

	extra_w = width - 2 * button_corner.get_width()
	# place top row
	for i in range(extra_w):
		button.blit(button_sliver, (i+button_corner.get_width(), 0))
	#place bottom row
	button_sliver = pg.transform.rotate(button_sliver, 180)
	for i in range(extra_w):
		button.blit(button_sliver, (i+button_corner.get_width(), height - button_sliver.get_height()))
	button_sliver = pg.transform.rotate(button_sliver, 180)

	extra_h = height -  2 * button_corner.get_width()
	# place top 
	button_sliver = pg.transform.rotate(button_sliver, 90)
	for i in range(extra_h):
		button.blit(button_sliver, (0, i+button_corner.get_width()))
	# place top 
	button_sliver = pg.transform.rotate(button_sliver, 180)
	for i in range(extra_h):
		button.blit(button_sliver, (width - button_corner.get_width(), i+button_corner.get_width()))
	button_sliver = pg.transform.rotate(button_sliver, 90)

	# place text!!!!!!!!!!!!!
	x = button_corner.get_width() + (width - 2*button_corner.get_width() - text.getLength()) / 2
	y = button_sliver.get_height() + (height - 2*button_sliver.get_height() - text.getSize()) / 2

	button.blit(text.get(), (x,y))

	return button