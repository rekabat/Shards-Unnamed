import pygame as pg
from pygame.locals import *

import display
import map
import player
import worldEvents
import text

TILE_RES = (32,32)
TRANSPARENT = (199,200,201)

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
			
		self.pressEnterDisplayed = False
	
	def clearWindow(self):
		self.window.fill(TRANSPARENT)
		self.window.set_colorkey(TRANSPARENT, pg.RLEACCEL)
	
	def flipPressEnterDisplayed(self):
		tx = text.Text("Press Enter", 50, text.RED).get()
		if self.pressEnterDisplayed:
			tx.fill(TRANSPARENT)
		self.window.blit(tx, (5, self.display.getWH()[1]-55))
		self.pressEnterDisplayed = not self.pressEnterDisplayed

	def createWorld(self, mapfile):
		self.map = map.Map(mapfile)
		self.eventForeground = worldEvents.EventForeground(mapfile)
		self.player = player.Player((12, 10))

	
	def dispatch(self, events):
		if self.state == "main-menu":
			pass

		elif self.state == "play":
			
			enterPressed = False
			
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
					if key == pg.K_RETURN:
						enterPressed = True
				
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
					
					# blits a message to self.window if your in proximity to an event
					bl = self.eventForeground.blocked(playerNewRect)
					if ( bl and (not self.pressEnterDisplayed)) or ((not bl) and self.pressEnterDisplayed):
						self.flipPressEnterDisplayed()
					# activates an event with enter outside of this function
					
					
					
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
			
			#enter overrides movements and triggers events
			if self.eventForeground.blocked(self.player.getRect()) and enterPressed:
				evt = self.eventForeground.getBlockedEvents(self.player.getRect())
				evt.execute(self)
				self.eventForeground.remove(evt)
				
			
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
		#gets optimal view frame based on player
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
		
		#retrieves all the events that happen to coincide with the view
		evtsToDisplay = self.eventForeground.getEventsInRect(view)
		#it goes through each and finds their relative position on the display based on their relative position to the map
		for each in evtsToDisplay:
			relRect=each.getRect().copy()
			relRect.center = (w*.5)+(relRect.centerx-viewx), (h*.5)+(relRect.centery-viewy)
			self.display.get().blit(each.getArt(), relRect)
		
		#gets a rect for player relative to the display screen as opposed to the map
		relativePlayerRect = pg.Rect((0,0),TILE_RES)
		relativePlayerRect.center = (w*.5)+(x-viewx), (h*.5)+(y-viewy)
		#blits the player to the screen (second highest layer)
		self.display.get().blit(self.player.getArt(), relativePlayerRect)
		
		#blits the window to the display over everything else (top layer)
		self.display.get().blit(self.window, (0,0))
		
		pg.display.flip()
