import pygame as pg
from pygame.locals import *

import display
import map
import player
import worldEvents
import text
import cursor

TILE_RES = (32,32)
TRANSPARENT = (199,200,201)

class GameInterface:
	def __init__(self, state="main-menu"):
		self.display = display.Display()
		self.map = None
		self.eventForeground = None
		self.player = None
		self.window = None
		self.clearWindow()
		self.cursr = cursor.Cursor()


		self.state = state
		if state == "main-menu":
			print "Not quite there yet"
		elif state == "play":
			self.createWorld('maps/mapgen_map')
			
			self.outlinedEvents = []
	
	def clearWindow(self):
		self.window = pg.Surface(self.display.getWH(), SRCALPHA, 32).convert_alpha()
	
	def flipOutlines(self, events):
		copy = self.outlinedEvents[:]
		for each in events:
			if each not in self.outlinedEvents:
				each.switchArt()
				self.outlinedEvents.append(each)
			else:
				copy.remove(each)
		for each in copy:
			each.switchArt()
			self.outlinedEvents.remove(each)
		


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
						self.player.movingDirection("U")
					if key == pg.K_s:
						self.player.movingDirection("D")
					if key == pg.K_a:
						self.player.movingDirection("L")
					if key == pg.K_d:
						self.player.movingDirection("R")
					if key == pg.K_RETURN:
						enterPressed = True
					if key == pg.K_t:
						self.display.toggleFull()
						self.cursr.flipVisible()
				
				elif event.type == pg.KEYUP:
					key = event.dict['key']
					if key == pg.K_w:
						self.player.stoppingDirection("U")
					if key == pg.K_s:
						self.player.stoppingDirection("D")
					if key == pg.K_a:
						self.player.stoppingDirection("L")
					if key == pg.K_d:
						self.player.stoppingDirection("R")
			
			self.player.turn()
			mv = self.player.overallDirection()

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
					
					# turns on outlines for near, blocked events
					self.flipOutlines(self.eventForeground.getBlockedEvents(playerNewRect))
					# activates an event with enter outside of this function
					
					
					
					#this loop triggers a chain of events that are stood on
					onEvent = self.eventForeground.onAndGetEvents(playerNewRect)
					if onEvent:
						onEvent.execute(self)
						self.eventForeground.remove(onEvent)
						#release player from any movements
						self.player.forgetMovement()
						#move the player UD to stay on the same spot and trigger any other events
						movePlayer("UD")
					
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
				#remove the press enter dialog
				self.flipOutlines(evt[1:])
				self.renderView()
				#execute the event
				evt[0].execute(self)
				self.eventForeground.remove(evt[0])
				#release player from any movements
				self.player.forgetMovement()
				#so that if it's now standing on event, that event will be activated
				movePlayer("UD")
				
			
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
