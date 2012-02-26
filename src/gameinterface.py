import pygame as pg
from pygame.locals import *

import display
import map
import worldEvents
import font
import cursor
import item
import attacks
import moveables
import player
import enemies

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
		self.curAttacks = []

		self.curEnemies = []

		self.createWorld('maps/mapgen_map')
		self.renderView()

		self.view = None #primarily used to determine if player is on top or bottom half of the screen for events
		self.tabHeld = False #true if tab is currently pressed
		self.checkForImmediateEvents = True #check for immediate events? True at new maps and after events are activated.
		
		##########
		# Stuff for "pause"
		##########
		self.pmenu = pm.PMenu(self)
			
	def createWorld(self, mapfile):
		self.map = map.Map(mapfile, self.display.getWH())
		self.eventForeground = worldEvents.EventForeground(mapfile)
		self.player = player.Player((12,10), [0])

		self.player.setBeltSlot(0,attacks.fireball(alignment = 0))
		self.player.setBeltSlot(1,attacks.icefield(alignment = 0))
		self.player.setBeltSlot(2,attacks.fireball(alignment = 0))
		self.player.setBeltSlot(3,attacks.icefield(alignment = 0))
		self.player.setBeltSlot(4,attacks.fireball(alignment = 0))
		self.player.setBeltSlot(5,attacks.icefield(alignment = 0))
		self.player.setBeltSlot(6,attacks.fireball(alignment = 0))
		self.player.setBeltSlot(7,attacks.icefield(alignment = 0))

		self.player.giveItem(item.Item("weapon", "weapon", 3))
	
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

	def addEnemy(self, enemy):
		self.curEnemies.append(enemy)

	def dispatch(self, events, dt=0):
		froze = False

		#some things are handled the same way in all states:
		for event in events:
			if event.type == pg.QUIT:
				quit()
			elif event.type == pg.KEYDOWN:
				key = event.dict['key']

				if key == pg.K_TAB:
					self.tabHeld = True
			elif event.type == pg.KEYUP:
				key = event.dict['key']

				if key == pg.K_TAB:
					self.tabHeld = False



		if self.state == "main-menu":
			pass

		elif self.state == "play":
			
			enterPressed = False
			
			for event in events:
				if event.type == pg.KEYDOWN:
					key = event.dict['key']

					casted = False

					if key == pg.K_RETURN:
						enterPressed = True
					
					elif key == pg.K_ESCAPE:
						self.state = "pause"
						#release player from any movements
						self.player.forgetMovement()
						#launches the menu into its last opened state (or player state if this is the first time opening it)
						self.pmenu.changeState(self.pmenu.getState())
						return
					
					#movement control
					elif key == pg.K_UP: 	self.player.movingDirection("U")
					elif key == pg.K_DOWN: 	self.player.movingDirection("D")
					elif key == pg.K_LEFT: 	self.player.movingDirection("L")
					elif key == pg.K_RIGHT: self.player.movingDirection("R")
					
					#casting of belt items
					elif key == pg.K_q:		casted = self.player.cast(0, self.player.getRect(), self.player.getDirectionFacing())
					elif key == pg.K_w: 	casted = self.player.cast(1, self.player.getRect(), self.player.getDirectionFacing())
					elif key == pg.K_e: 	casted = self.player.cast(2, self.player.getRect(), self.player.getDirectionFacing())
					elif key == pg.K_r: 	casted = self.player.cast(3, self.player.getRect(), self.player.getDirectionFacing())
					elif key == pg.K_a: 	casted = self.player.cast(4, self.player.getRect(), self.player.getDirectionFacing())
					elif key == pg.K_s: 	casted = self.player.cast(5, self.player.getRect(), self.player.getDirectionFacing())
					elif key == pg.K_d: 	casted = self.player.cast(6, self.player.getRect(), self.player.getDirectionFacing())
					elif key == pg.K_f: 	casted = self.player.cast(7, self.player.getRect(), self.player.getDirectionFacing())
					if casted: #will be false if nothing is casted or an empty belt slot is used
						self.curAttacks.append(casted)
				
				elif event.type == pg.KEYUP:
					key = event.dict['key']

					if key == pg.K_UP: self.player.stoppingDirection("U")
					elif key == pg.K_DOWN: self.player.stoppingDirection("D")
					elif key == pg.K_LEFT: self.player.stoppingDirection("L")
					elif key == pg.K_RIGHT: self.player.stoppingDirection("R")
			
			mv = self.player.overallDirection()

			def doEvent(evt, outline=False):
				self.state = "WE"
				evt.execute(self)
				
				if evt.getOneTime():
					#remove the event and return to the "play" state
					self.eventForeground.remove(evt)
					if outline:
						#remove the red outline
						self.outlinedEvents.remove(evt)
						self.flipOutlines(self.outlinedEvents)
				self.state = "play"
				#release player from any movements
				self.player.forgetMovement()

				self.checkForImmediateEvents = True

				return True #froze = True

			############################################
			# Deal with immediate events ###############
			############################################

			if self.checkForImmediateEvents:
				im = self.eventForeground.immediates()
				if len(im)>0:
					for e in im:
						froze = doEvent(e)
				else:
					self.checkForImmediateEvents = False

			############################################
			############################################
			############################################


			############################################
			# Deal with "enter" ########################
			############################################

			#enter overrides movements and triggers events
			if len(self.outlinedEvents)>0 and enterPressed:
				evt = self.outlinedEvents[0]
				froze = doEvent(evt, outline=True)

			############################################
			############################################
			############################################


			############################################
			# Move player ##############################
			############################################
				
			def mvPlayer(mv,dt):
				self.player.move(mv, dt, suppressTurn = self.tabHeld)

				# Check if the movement is valid by making a smaller rectangle and seeing
				smallerRect=pg.Rect((0,0),(self.player.getRect().width*.87, self.player.getRect().height*.87))
				smallerRect.center = self.player.getRect().center
				# if any of the corners are on a blocked map tile or WE tile
				cantMove = \
				self.map.blocked(smallerRect, self.player.getZs()) or \
				self.eventForeground.blocked(smallerRect, self.player.getZs())
				#if any corners are on an enemy
				for e in self.curEnemies:
					cantMove = cantMove or e.getRect().colliderect(smallerRect)

				# If the movement is valid, move the player there
				if not cantMove:
					# couldntMove = False

					playerZs = self.player.getZs()
					playerZs.sort()
					playerZs.reverse()

					#try to to get a tile from the highest z the player is on, if nothing work your way down to lower zs the player's on
					for z in playerZs:
						atile = self.map.getTile(self.player.getRect().center, z)
						if atile:
							self.player.setZ(atile.getZs())
							break

					return True
				
				else:
					self.player.undoMove()
					if len(mv)>1:
						for m in mv:
							if mvPlayer(m, dt):
								return True

				# if couldntMove:
				# 	pass #implement sliding
				# 	#######################
				# 	#######################
				# 	#get rid of smallerRect
			############################################
			############################################
			############################################
			



			############################################
			############################################
			############################################
			def checkForEvents():
				playerZs = self.player.getZs()

				#tile the player's center pix is on
				tilePlayerOn = self.map.getTile(self.player.getRect().center, max(playerZs))
				#the events on that tile
				mustActivate = self.eventForeground.unlockedNotEnterableEventsOn([tilePlayerOn], playerZs)
				activateIfEnterOnTopOf = self.eventForeground.unlockedEnterableEventsOn([tilePlayerOn], playerZs)

				#the tile in front of the player (based on the way he faces)
				for z in playerZs:
					# will return false if there's no tile at those coords and z
					tileInFrontOfPlayer = self.map.getTile(self.player.getTilePixInFrontOf(), z)
					if tileInFrontOfPlayer:
						break
				#the events on that tile
				if tileInFrontOfPlayer:
					activateIfEnterInFrontOf = self.eventForeground.unlockedEnterableBlockedEventsOn([tileInFrontOfPlayer], playerZs)
				else:
					activateIfEnterInFrontOf = []
				

				# turns on outlines for events
				self.flipOutlines(activateIfEnterOnTopOf+activateIfEnterInFrontOf)
				# activates an event with enter outside of this function

				return mustActivate
			############################################
			############################################
			############################################



			############################################
			############################################
			############################################
			# def triggerStandOns(dt, mustActivate):
			# 	#this loop triggers a chain of events that are stood on
			# 	self.state = "WE"
			# 	#release player from any movements
			# 	self.player.forgetMovement()

			# 	mustActivate[0].execute(self)
			# 	if mustActivate[0].getOneTime():
			# 		self.eventForeground.remove(mustActivate[0])
			# 	self.state = "play"

			# 	doit("UD", dt)
			
			# 	return dt
			############################################
			############################################
			############################################
			def doit(mv, dt):
				if (len(mv)>0):
					mvPlayer(mv, dt)
				if (len(mv)>0):
					mustActivate = checkForEvents()
				if (len(mv)>0) and (len(mustActivate)>0):
					for e in mustActivate:
						froze = doEvent(e, outline=False)
					return froze
					# triggerStandOns(dt, mustActivate)
					# froze = True
			froze = froze or doit(mv, dt)



			############################################
			############################################
			############################################
			#handle enemies
			for e in self.curEnemies:
				atk = e.tick(dt, self.player)
				if atk:
					self.curAttacks.append(atk)
			############################################
			############################################
			############################################




			############################################
			############################################
			############################################
			#handle attacks
			for a in self.curAttacks:
				keepA = a.tick(dt)
				if not keepA:
					self.curAttacks.remove(a)

				#cause damage to player
				# if a.getAlignment() != self.player.getAlignment() and a.getRect().colliderect(self.player.getRect()):
				if a.getRect().colliderect(self.player.getRect()):
					a.hit(self.player)
					if self.player.getCurrentHP() <= 0:
						print "dead!!!!"
						quit()

				#cause damage to enemies
				else:
					for e in self.curEnemies:
						# if a.getAlignment() != e.getAlignment() and a.getRect().colliderect(e.getRect()):
						if a.getRect().colliderect(e.getRect()):
							a.hit(e)
							if e.getCurrentHP() <= 0:
								self.curEnemies.remove(e)
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
		return events, froze
	
	def clearWindow(self):
		self.window = pg.Surface(self.display.getWH(), SRCALPHA, 32).convert_alpha()
	
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
				for each in evtsToDisplay:
					blitRelRect(each.getRect(), each.getArt())

			#blit player to screen
			blitRelRect(self.player.getRect(), self.player.getArt())

			#blit enemies to screen
			for e in self.curEnemies:
				blitRelRect(e.getRect(), e.getArt())
			for e in self.curEnemies:
				blitRelRect(e.getHPBarRect(), e.getHPBar())

			#blit all the attacks to the screen
			for a in self.curAttacks:
				if a.getRect().colliderect(view):
					blitRelRect(a.getRect(), a.getImg())

			
			mapAbovePlayersZ = self.map.getImageOfAndAboveZ(playerOnZ+1, view) #returns false if player is on map's highest z
			if mapAbovePlayersZ:
				self.display.get().blit(mapAbovePlayersZ, (0,0))
			
			#retrieves all the events that happen to coincide with the view
			evtsToDisplay = self.eventForeground.getEventsOfAndAbove(playerOnZ+1, view)
			if evtsToDisplay:
				for each in evtsToDisplay:
					blitRelRect(each.getRect(), each.getArt())

			# then the players belt is blitted
			belt = self.player.getBelt().getImg()
			self.display.get().blit(belt, ((w-belt.get_width())/2.,h-g.TILE_RES[1]))

			#blits the window to the display over everything else (top layer)
			self.display.get().blit(self.window, (0,0))
			
			pg.display.flip()

			self.view = view
		
		elif self.state == "pause":
			self.display.get().blit(self.pmenu.getDisp(), (0,0))
			pg.display.flip()