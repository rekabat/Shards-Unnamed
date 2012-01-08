import pygame as pg
from pygame.locals import *

import display
import map
import player
import worldEvents
import text
import cursor

import general as g

class GameInterface:
	def __init__(self, state="main-menu"):
		self.display = display.Display()
		self.map = None
		self.eventForeground = None
		self.player = None
		self.window = None
		self.clearWindow()
		self.cursr = cursor.Cursor()
		self.view = None


		self.state = state
		if state == "main-menu":
			print "Not quite there yet"
		elif state == "play":
			self.outlinedEvents = []

			self.createWorld('maps/mapgen_map')
			self.renderView()
			
			
	
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
		self.player = player.Player((12, 10), [0])

	
	def dispatch(self, events):
		#some things are handled the same way in all states:
		for event in events:
			if event.type == pg.QUIT:
				quit()


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
				smallerRect=pg.Rect((0,0),(playerNewRect.width*.87, playerNewRect.height*.87))
				smallerRect.center = playerNewRect.center
				cantMove = \
					self.map.blocked(smallerRect) or \
					self.eventForeground.blocked(smallerRect)
				
				# If the movement is valid, move the player there
				if not cantMove:
					mv = ""
					self.player.move(playerNewRect)
					
					tilePlayerOn = self.player.getTileOn()
					tileInFrontOfPlayer = self.player.getTileInFrontOf()

					tileList = [self.map.getTile(tilePlayerOn, False), self.map.getTile(tileInFrontOfPlayer, False)]

					mustActivate = self.eventForeground.unlockedNotEnterableEventsOn(tileList[0:1])
					activateIfEnterOnTopOf = self.eventForeground.unlockedEnterableEventsOn(tileList[0:1])
					activateIfEnterInFrontOf = self.eventForeground.unlockedEnterableBlockedEventsOn(tileList[1:2])

					#this loop triggers a chain of events that are stood on
					if len(mustActivate)>0:
						self.state = "WE"
						mustActivate[0].execute(self)
						self.state = "play"
						self.eventForeground.remove(mustActivate[0])
						#release player from any movements
						self.player.forgetMovement()
						#move the player UD to stay on the same spot and trigger any other events
						movePlayer("UD")
					
						return True
					 
					# tilesToFlip = self.eventForeground.get
					# turns on outlines for near, blocked events
					self.flipOutlines(activateIfEnterOnTopOf+activateIfEnterInFrontOf)
					# activates an event with enter outside of this function
					
				else:
					if len(mv) > 1:
						if not movePlayer(mv[0]):
							movePlayer(mv[1:])
					else:
						#this compensates for turning but not moving and having new events get outlined
						movePlayer("UD")
			
			#enter overrides movements and triggers events
			if len(self.outlinedEvents)>0 and enterPressed:
				evt = self.outlinedEvents.pop()
				#remove the press enter dialog
				self.flipOutlines(self.outlinedEvents)
				self.renderView()
				#execute the event
				self.state = "WE"
				evt.execute(self)
				self.state = "play"
				self.eventForeground.remove(evt)
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
		
		elif self.state == "WE":
			pass
		
		#it returns all events that are not executed in the general state
		return events
	
	def playerOnTopHalf(self):
		if self.view.centery+5 < self.player.getRect().centery:
			return False
		else:
			return True

	def renderView(self):
		#gets optimal view frame based on player
		mapx, mapy = self.map.getMapSizePx()
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
		tilesToDisplay = self.map.getTilesInRect(view)
		for each in tilesToDisplay:
			relRect=each.getRect().copy()
			relRect.center = (w*.5)+(relRect.centerx-viewx), (h*.5)+(relRect.centery-viewy)
			self.display.get().blit(each.getArt(), relRect)
		
		#retrieves all the events that happen to coincide with the view
		evtsToDisplay = self.eventForeground.getEventsInRect(view)
		#it goes through each and finds their relative position on the display based on their relative position to the map
		for each in evtsToDisplay:
			relRect=each.getRect().copy()
			relRect.center = (w*.5)+(relRect.centerx-viewx), (h*.5)+(relRect.centery-viewy)
			self.display.get().blit(each.getArt(), relRect)
		
		#gets a rect for player relative to the display screen as opposed to the map
		relativePlayerRect = pg.Rect((0,0),g.TILE_RES)
		relativePlayerRect.center = (w*.5)+(x-viewx), (h*.5)+(y-viewy)
		#blits the player to the screen (second highest layer)
		self.display.get().blit(self.player.getArt(), relativePlayerRect)
		
		#blits the window to the display over everything else (top layer)
		self.display.get().blit(self.window, (0,0))
		
		pg.display.flip()

		self.view = view