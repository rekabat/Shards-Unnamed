import pygame as pg
from pygame.locals import *

import display
import map
import player
import worldEvents
import font
import cursor
import item

import pauseMenu as pm

import general as g

class GameInterface:
	def __init__(self, state="main-menu"):
		self.display = display.Display()
		self.cursr = cursor.Cursor()
		self.font = font.Font()


		self.state = state
		##########
		# stuff for "main-menu"
		##########
			#
		
		##########
		# Stuff for "play"
		##########
		self.map = None
		self.eventForeground = None
		self.player = None
		self.window = None
		self.clearWindow()

		self.outlinedEvents = []

		self.createWorld('maps/mapgen_map')
		self.renderView()

		self.view = None #primarily used to determine if player is on top or bottom half of the screen for events
		
		##########
		# Stuff for "pause"
		##########
		self.pmenu = pm.PMenu(self)
			
			
	
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
		self.map = map.Map(mapfile, self.display.getWH())
		self.eventForeground = worldEvents.EventForeground(mapfile)
		self.player = player.Player((12,10), [0])

		self.player.giveItem(item.Item("weapon", "weapon", 3))
	
	def dispatch(self, events, dt=0):
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
					if key == pg.K_UP:
						self.player.movingDirection("U")
					if key == pg.K_DOWN:
						self.player.movingDirection("D")
					if key == pg.K_LEFT:
						self.player.movingDirection("L")
					if key == pg.K_RIGHT:
						self.player.movingDirection("R")
					
					if key == pg.K_RETURN:
						enterPressed = True
					
					if key == pg.K_ESCAPE:
						self.state = "pause"
						#release player from any movements
						self.player.forgetMovement()

						#launches the menu into its last opened state (or player state if this is the first time opening it)
						self.pmenu.changeState(self.pmenu.getState())
						return
				
				elif event.type == pg.KEYUP:
					key = event.dict['key']
					if key == pg.K_UP:
						self.player.stoppingDirection("U")
					if key == pg.K_DOWN:
						self.player.stoppingDirection("D")
					if key == pg.K_LEFT:
						self.player.stoppingDirection("L")
					if key == pg.K_RIGHT:
						self.player.stoppingDirection("R")
			


			mv = self.player.overallDirection()


			############################################
			# Deal with "enter" ########################
			############################################

			#enter overrides movements and triggers events
			if len(self.outlinedEvents)>0 and enterPressed:
				evt = self.outlinedEvents[0]
				#execute the event while in the "WE" state
				self.state = "WE"
				evt.execute(self)
				
				if evt.getOneTime():
					#remove the event and return to the "play" state
					self.eventForeground.remove(evt)
					#remove the red outline
					self.outlinedEvents.remove(evt)
					self.flipOutlines(self.outlinedEvents)
				self.state = "play"
				#release player from any movements
				self.player.forgetMovement()
				#so that if it's now standing on event, that event will be activated
				mv = "UD"

			############################################
			############################################
			############################################

			self.player.turn()

			############################################
			# Move player ##############################
			############################################
			def mvPlayer(mv, dt):
				couldntMove = True
				for m in mv:
					# Get the rect that the player would go to given the buttons pressed
					playerNewRect = self.player.ifMoved(m, dt)

					# Check if the movement is valid by making a smaller rectangle and seeing
					smallerRect=pg.Rect((0,0),(playerNewRect.width*.87, playerNewRect.height*.87))
					smallerRect.center = playerNewRect.center
					# if any of the corners are on a blocked map tile or WE tile
					cantMove = \
					self.map.blocked(smallerRect, self.player.getZs()) or \
					self.eventForeground.blocked(smallerRect, self.player.getZs())

					# cantMove = \
					# self.map.blocked(playerNewRect, self.player.getZs()) or \
					# self.eventForeground.blocked(playerNewRect, self.player.getZs())
				

				
					# If the movement is valid, move the player there
					if not cantMove:
						couldntMove = False

						playerZs = self.player.getZs()
						playerZs.sort()
						playerZs.reverse()

						#try to to get a tile from the highest z the player is on, if nothing work your way down to lower zs the player's on
						for z in playerZs:
							atile = self.map.getTile(self.player.getRect().center, z)
							if atile:
								self.player.move(playerNewRect, atile.getZs())
								break
				
				if couldntMove:
					pass #implement sliding
					#######################
					#######################
					#get rid of smallerRect
			if len(mv) > 0:
				mvPlayer(mv, dt)
			############################################
			############################################
			############################################
			



			############################################
			############################################
			############################################

			def checkForEventsAndTriggerStandOns(dt):
				playerZs = self.player.getZs()

				tilePlayerOn = self.map.getTile(self.player.getRect().center, max(playerZs))

				for z in playerZs:
					# will return false if there's no tile at those coords and z
					tileInFrontOfPlayer = self.map.getTile(self.player.getTilePixInFrontOf(), z)
					if tileInFrontOfPlayer:
						break

				if tilePlayerOn:
					mustActivate = self.eventForeground.unlockedNotEnterableEventsOn([tilePlayerOn], playerZs)
					activateIfEnterOnTopOf = self.eventForeground.unlockedEnterableEventsOn([tilePlayerOn], playerZs)
				else:
					mustActivate = []
					activateIfEnterOnTopOf = []
				
				if tileInFrontOfPlayer:
					activateIfEnterInFrontOf = self.eventForeground.unlockedEnterableBlockedEventsOn([tileInFrontOfPlayer], playerZs)
				else:
					activateIfEnterInFrontOf = []
			
				#this loop triggers a chain of events that are stood on
				if len(mustActivate)>0:
					self.state = "WE"
					#release player from any movements
					self.player.forgetMovement()

					mustActivate[0].execute(self)
					if mustActivate[0].getOneTime():
						self.eventForeground.remove(mustActivate[0])
					self.state = "play"
					#move the player UD to stay on the same spot and trigger any other events
					mvPlayer("UD", dt)
					checkForEventsAndTriggerStandOns(dt)
				
					return True
				 
				# turns on outlines for events
				self.flipOutlines(activateIfEnterOnTopOf+activateIfEnterInFrontOf)
				# activates an event with enter outside of this function
			if (len(mv)>0):
				checkForEventsAndTriggerStandOns(dt)
			############################################
			############################################
			############################################
			
				

		elif self.state == "pause":
			for event in events:
				if event.type == pg.KEYDOWN:
					key = event.dict['key']
					if key == pg.K_ESCAPE:
						self.state = "play"
						self.pmenu.clearall()
						return
					else:
						self.pmenu.dispatch(key)
				
				# elif event.type == pg.KEYUP:
			
		
		elif self.state == "WE":
			pass
		
		#it returns all events that are not executed in the general state
		return events
	
	def playerOnTopHalf(self): #with a slight tolerance
		if self.view.centery+5 < self.player.getRect().centery: 
			return False
		else:
			return True

	def renderView(self):
		if self.state == "main-menu":
			pass

		elif self.state == "play" or self.state == "WE":
			#gets optimal view frame based on player
			
			mapx, mapy = self.map.getDrawingSize()

			# mapx, mapy = self.map.getMapSizePx()
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

			#get rect relactive to view assuming it's also relative to map (like view is) and blit it to the screen with the art
			mapdifx, mapdify = self.map.getMapDrawingDif()
			def blitRelRect(rect, art):
				relRect = rect.copy()
				relRect.center = (w*.5)+(relRect.centerx-viewx)+mapdifx, (h*.5)+(relRect.centery-viewy)+mapdify
				self.display.get().blit(art, relRect)

			#blits a subsurface of the map to the display (lowest layer)
			playerOnZ = max(self.player.getZs())
			self.display.get().blit(self.map.getImageOfAndBelowZ(playerOnZ, view), (0,0))
			
			#retrieves all the events that happen to coincide with the view
			evtsToDisplay = self.eventForeground.getEventsOfAndBelow(playerOnZ, view)
			if evtsToDisplay:
				# print "below", evtsToDisplay
				for each in evtsToDisplay:
					blitRelRect(each.getRect(), each.getArt())
			
			blitRelRect(self.player.getRect(), self.player.getArt())
			
			mapAbovePlayersZ = self.map.getImageOfAndAboveZ(playerOnZ+1, view) #returns false if player is on map's highest z
			if mapAbovePlayersZ:
				self.display.get().blit(mapAbovePlayersZ, (0,0))
			
			#retrieves all the events that happen to coincide with the view
			evtsToDisplay = self.eventForeground.getEventsOfAndAbove(playerOnZ+1, view)
			if evtsToDisplay:
				# print "above", evtsToDisplay
				for each in evtsToDisplay:
					blitRelRect(each.getRect(), each.getArt())

			#blits the window to the display over everything else (top layer)
			self.display.get().blit(self.window, (0,0))
			
			pg.display.flip()

			self.view = view
		
		elif self.state == "pause":
			self.display.get().blit(self.pmenu.getDisp(), (0,0))
			pg.display.flip()