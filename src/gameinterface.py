import pygame as pg
from pygame.locals import *

import display
import map
import player
import worldEvents

TILE_RES = (32,32)

class GameInterface:
	def __init__(self, state="main-menu"):
		self.display = display.Display()
		self.map = None
		self.eventForeground = None
		self.player = None
		self.window = pg.Surface(self.display.getWH())
		self.clearWindow()

		self.state = state
		if state == "main-menu":
			print "Not quite there yet"
		elif state == "play":
			self.createWorld('maps/mapgen_map')
	
	def clearWindow(self):
		self.window.fill((199,200,201))
		self.window.set_colorkey((199,200,201))

	def createWorld(self, mapfile):
		self.map = map.Map(mapfile)
		self.eventForeground = worldEvents.EventForeground(mapfile)
		self.player = player.Player((12, 10))

	
	def dispatch(self, events):
		if self.state == "main-menu":
			pass

		elif self.state == "play":
			for event in events:
				if event.type == pg.KEYDOWN:
					key = event.dict['key']
					if key == pg.K_w:
						self.player.udlr[0] = True
					if key == pg.K_s:
						self.player.udlr[1] = True
					if key == pg.K_a:
						self.player.udlr[2] = True
					if key == pg.K_d:
						self.player.udlr[3] = True
				
				elif event.type == pg.KEYUP:
					key = event.dict['key']
					if key == pg.K_w:
						self.player.udlr[0] = False
					if key == pg.K_s:
						self.player.udlr[1] = False
					if key == pg.K_a:
						self.player.udlr[2] = False
					if key == pg.K_d:
						self.player.udlr[3] = False
			
			mv = ""
			mv += "U" if self.player.udlr[0] else ""
			mv += "D" if self.player.udlr[1] else ""
			mv += "L" if self.player.udlr[2] else ""
			mv += "R" if self.player.udlr[3] else ""

			def movePlayer(mv):
				# Get the rect that the player would go to given the buttons pressed
				playerNewRect = self.player.ifMoved(mv)

				# Check if the movement is valid by making a smaller rectangle and seeing
				# if any of the corners are on a blocked map tile or WE tile
				cp = playerNewRect.copy()
				smallerRect=pg.Rect((0,0),(1,1))
				smallerRect.size = (cp.width*.9, cp.height*.9)
				smallerRect.center = cp.center
				cantMove = \
					self.map.blocked(smallerRect.topleft)     or \
					self.map.blocked(smallerRect.topright)    or \
					self.map.blocked(smallerRect.bottomleft)  or \
					self.map.blocked(smallerRect.bottomright) or \
					self.eventForeground.blocked(smallerRect)
				
				# If the movement is valid, move the player there
				if not cantMove:
					mv = ""
					self.player.move(playerNewRect)
					
					# Player can be either standing on event or moved next to an event
					
					#this loop triggers a chain of events that are stood on
					while 1:
						onEvent = self.eventForeground.onAndGetEvents(playerNewRect)
						if onEvent:
							onEvent.execute(self)
							self.eventForeground.remove(onEvent)
						else:
							break
					
					return True
				else:
					if len(mv) > 1:
						if not movePlayer(mv[0]):
							movePlayer(mv[1:])
					else:
						return False
			
			if len(mv) > 0:
				movePlayer(mv)
			

			# WE = self.player.move(mv)

			# if WE is not None:
			#     for each in WE:
			#         each.execute(self)
			#         self.player.place(self.player.rect, True)

		elif self.state == "pause":
			pass
	
	def renderView(self):
		#gets optimal view frame
		mapx, mapy = self.map.get().get_size()
		x, y = self.player.getRect().center
		w, h = self.display.getWH()
		viewx, viewy = x+0, y+0
		
		if (x < (w*.5)):
			viewx = w*.5
		elif (x > (mapx - (w*.5))):
			viewx = mapx - (w*.5)
		if (y < (h*.5)):
			viewy = h*.5
		elif (y > (mapy - (h*.5))):
			viewy = mapy - (h*.5)

		view = pg.Rect((0, 0), (w, h))
		view.center = viewx, viewy
		
		#blits a subsurface of the map to the display (lowest layer)
		self.display.get().blit(self.map.get().subsurface(view), (0,0))
		
		#blits a subsurface of the foreground event to the display (second layer)
		self.display.get().blit(self.eventForeground.get().subsurface(view), (0,0))
		
		#gets a rect for player relative to the display screen as opposed to the map
		relativePlayerRect = pg.Rect((0,0),TILE_RES)
		relativePlayerRect.center = (w*.5)+(x-viewx), (h*.5)+(y-viewy)
		#blits the player to the screen (second highest layer)
		self.display.get().blit(self.player.getArt(), relativePlayerRect)
		
		#blits the window to the display over everything else (top layer)
		self.display.get().blit(self.window, (0,0))
		
		'''
		##### INEFFECIENT, only copy the view portion of the maps (optimally)
		
		# make a copy of the map image
		tempSurf = self.map.get().copy()
		# blit the event foreground onto that copy
		tempSurf.blit(self.eventForeground.get(), (0,0))
		# put the player's image onto the correct spot of the map copy
		tempSurf.blit(self.player.getArt(), self.player.getRect())

		# tempSurf becomes size of view, push window on top
		tempSurf = tempSurf.subsurface(view).copy()
		tempSurf.blit(self.window, (0, 0))

		#tempSurf.blit("self.window", view)

		self.display.get().blit(tempSurf, (0,0))
		'''
		
		pg.display.flip()
