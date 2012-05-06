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
		self.foundOnePathAlready = False #used to prevent the pathfinding algorithm from being run more than once per cycle

		self.createWorld('maps/room1', (10,10), 0)
		self.renderView()

		self.view = None #primarily used to determine if player is on top or bottom half of the screen for events
		self.lockedOntoEnemy = None #true if tab is currently pressed
		self.checkForImmediateEvents = True #check for immediate events? True at new maps and after events are activated.
		
		##########
		# Stuff for "pause"
		##########
		self.pmenu = pm.PMenu_general(self, pg.Surface(self.display.getWH()))
			
	def createWorld(self, mapfile, playerPos, playerZ):
		# self.loadMap(mapfile, playerPos, playerZ)
		self.player = player.Player(playerPos, playerZ, self.font, self.display.getWH()[0])

		# self.player = player.Player(self.font, self.display.getWH()[0])
		self.loadMap(mapfile, playerPos, playerZ)

		self.player.giveFocus(attacks.fireball(alignment = 0, user = self.player, GI = self))
		self.player.giveFocus(attacks.icefield(alignment = 0, user = self.player, GI = self))
		self.player.giveFocus(attacks.sword(alignment = 0, user = self.player, GI = self))

		self.player.equip(0, self.player.focuses[0])
		self.player.equip(1, self.player.focuses[1])
		self.player.equip(8, self.player.focuses[2])

		self.player.giveItem(item.Item("weapon", "weapon", 3))

	def loadMap(self, mapfile, playerPos, playerZ):
		self.map = map.Map(mapfile, self.display.getWH())
		self.staticMap = self.map.getTotalImg()
		self.eventForeground = worldEvents.EventForeground(mapfile)

		self.outlinedEvents = []
		self.curAttacks = []
		self.curEnemies = []

		self.lockedOntoEnemy = None

		self.player.setPlace(playerPos, playerZ)


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

	def collision_point(self, point, z, player = True, enemies = True, tiles = True, events = True, ignoreEnemy = None):
		#if point is in player
		if player and (self.player.getZ() == z) and (self.player.getRect().collidepoint(point)):
			return True

		#if point is in enemy
		if enemies:
			for e in self.curEnemies:
				if (e is not ignoreEnemy) and (e.getZ() == z) and (e.getRect().collidepoint(point)):
					return True

		#if point is on a blocked tile
		if tiles:
			try:
				if self.map.getTile(point, z).blocked(): #tile exists and is blocked
					return True
			except: #tile doesn't exist
				return True

		#if point is on a blocked WE
		if events and (self.eventForeground.blocked(g.pix2tile2rect(point), z)):
			return True


	def collisionWithBlockedTile(self, tile, z, player = True, enemies = True, tiles = True, events = True, ignoreEnemy = None):
		rect = g.tile2rect(tile)

		#if any corners are on player
		if player and self.player.getRect().colliderect(rect):
			return True

		#if any corners are on an enemy
		if enemies:
			for e in self.curEnemies:
				if e is not ignoreEnemy:
					if e.getRect().colliderect(rect):
						return True

		# if any of the corners are on a blocked map tile or WE tile
		if tiles:
			try:
				if self.map.getTile(tile, z, pixel = False).blocked():
				# if self.map.blocked(rect, zs):
					return True
			except:
				return True
				pass
			# 	print "blocked on tile", tile, "and z", z
			# 	quit()

		# if any of the corners are on a WE tile
		if events and self.eventForeground.blocked(rect, z):
			return True


	def collisionWithBlockedRect(self, rect, z, player = True, enemies = True, tiles = True, events = True, ignoreEnemy = None):
		#if any corners are on player
		if player and self.player.getRect().colliderect(rect):
			return True

		#if any corners are on an enemy
		if enemies:
			for e in self.curEnemies:
				if e is not ignoreEnemy:
					if e.getRect().colliderect(rect):
						# print "enemy"
						return True
		
		# if any of the corners are on a blocked map tile or WE tile
		if tiles and self.map.blocked(rect, z):
			# print "map"
			return True 

		# if any of the corners are on a WE tile
		if events and self.eventForeground.blocked(rect, z):
			# print "event"
			return True

	def dispatch(self, events, dt=0):
		froze = False

		#some things are handled the same way in all states:
		for event in events:
			if event.type == pg.QUIT:
				quit()
			# elif event.type == pg.KEYDOWN:
			# 	key = event.dict['key']

			# elif event.type == pg.KEYUP:
			# 	key = event.dict['key']

			# 	if key == pg.K_TAB:
			# 		self.tabPressed = False



		if self.state == "main-menu":
			pass

		elif self.state == "play":
			
			enterPressed = False
			self.foundOnePathAlready = False
			
			for event in events:
				if event.type == pg.KEYDOWN:
					key = event.dict['key']

					casted = False

					if key == pg.K_RETURN:
						enterPressed = True

					elif key == pg.K_TAB:
						if self.lockedOntoEnemy == None:
							if len(self.curEnemies) > 0:
								lock = 0
								dist = g.distance(self.player.getRect().center, self.curEnemies[0].getRect().center)
								for i in range(len(self.curEnemies))[1:]:
									d = g.distance(self.player.getRect().center, self.curEnemies[i].getRect().center)
									if d<dist:
										lock = i+0
										dist = d+0
								self.lockedOntoEnemy = self.curEnemies[lock]
						else:
							self.lockedOntoEnemy = None
					
					elif key == pg.K_ESCAPE:
						self.state = "pause"
						#release player from any movements
						self.player.forgetMovement()
						#launches the menu into its last opened state (or player state if this is the first time opening it)
						# self.pmenu.changeState(self.pmenu.getState())
						return 0, True
					
					#movement control
					elif key == pg.K_UP: 	self.player.movingDirection("U")
					elif key == pg.K_DOWN: 	self.player.movingDirection("D")
					elif key == pg.K_LEFT: 	self.player.movingDirection("L")
					elif key == pg.K_RIGHT: self.player.movingDirection("R")
					
					#casting of belt items
					elif key == pg.K_q:		casted = self.player.cast(0)
					elif key == pg.K_w: 	casted = self.player.cast(1)
					elif key == pg.K_e: 	casted = self.player.cast(2)
					elif key == pg.K_r: 	casted = self.player.cast(3)
					elif key == pg.K_a: 	casted = self.player.cast(4)
					elif key == pg.K_s: 	casted = self.player.cast(5)
					elif key == pg.K_d: 	casted = self.player.cast(6)
					elif key == pg.K_f: 	casted = self.player.cast(7)
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
				if self.lockedOntoEnemy is not None:
					self.player.move(mv, dt, forceTurn = self.lockedOntoEnemy.getRect().center)
				else:
					self.player.move(mv, dt)

				# Check if the movement is valid by making a smaller rectangle and seeing
				smallerRect=pg.Rect((0,0),(self.player.getRect().width*.87, self.player.getRect().height*.87))
				smallerRect.center = self.player.getRect().center
				# corners = (	g.pix2tile(smallerRect.topleft), \
				# 			g.pix2tile(smallerRect.topright), \
				# 			g.pix2tile(smallerRect.bottomleft), \
				# 			g.pix2tile(smallerRect.bottomright) )
				corners = (	smallerRect.topleft, \
							smallerRect.topright, \
							smallerRect.bottomleft, \
							smallerRect.bottomright )
				validZs = self.player.getZ()
				validZs = [validZs+1, validZs, validZs-1]

				# If the movement is valid, move the player there
				highestZC = validZs[2]
				for c in corners:

					thisCBlocked = True
					for z in validZs:
						# if not self.collisionWithBlockedTile(c, z, player=False):
						if not self.collision_point(c, z, player=False):
							thisCBlocked = False
							if z > highestZC: highestZC = z
							break

					if thisCBlocked:
						self.player.undoMove()
						if len(mv)>1:
							for m in mv:
								# if mvPlayer(m, dt):
									# self.player.setZ(highestZC)
									# return True
								mvPlayer(m,dt)
						return False
				
				self.player.setZ(highestZC)
				return True
					# if not self.collisionWithBlockedRect(smallerRect, z, player = False):
						# couldntMove = False


						#try to to get a tile from the highest z the player is on
						#if nothing work your way down to lower zs the player's on
						# for z in playerZs:
				# 		atile = self.map.getTile(self.player.getRect().center, z)
				# 		if atile:
				# 			self.player.setZ(atile.getZ())
				# 			return True
				
				# # else:
				# self.player.undoMove()
				# if len(mv)>1:
				# 	for m in mv:
				# 		if mvPlayer(m, dt):
				# 			return True

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
				playerZs = self.player.getZ()
				playerZs = [playerZs+1, playerZs, playerZs-1]

				#tile the player's center pix is on
				for z in playerZs:
					tilePlayerOn = self.map.getTile(self.player.getRect().center, z)
					if tilePlayerOn:
						break
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
			rectInFrontOfPlayer = self.player.getRect().copy()
			if self.player.facing == "U": rectInFrontOfPlayer.top -= g.TILE_RES[1]
			elif self.player.facing == "D": rectInFrontOfPlayer.top += g.TILE_RES[1]
			elif self.player.facing == "L": rectInFrontOfPlayer.left -= g.TILE_RES[0]
			else: rectInFrontOfPlayer.left += g.TILE_RES[0]

			for e in self.curEnemies:
				atk, found = e.tick(dt, self.foundOnePathAlready)
				self.foundOnePathAlready = self.foundOnePathAlready or found
				if atk:
					self.curAttacks.append(atk)

				#deal with players sword attack
				if rectInFrontOfPlayer.colliderect(e.getRect()):
					casted = self.player.cast(8)
					if casted:
						self.curAttacks.append(casted)
			############################################
			############################################
			############################################



			############################################
			############################################
			############################################
			#handle player animations (to come) and spell cool downs
			self.player.tick(dt)
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
				if a.getRect().colliderect(self.player.getRect()) and (a.getZ() == self.player.getZ()):
					a.hit(self.player)
					if self.player.getCurStat('hp') <= 0:
						print "dead!!!!"
						quit()

				#cause damage to enemies
				for e in self.curEnemies:
					# if a.getAlignment() != e.getAlignment() and a.getRect().colliderect(e.getRect()):
					if a.getRect().colliderect(e.getRect()) and (a.getZ() == e.getZ()):
						a.hit(e)
						if e.getCurrentHP() <= 0:
							self.curEnemies.remove(e)
							if self.lockedOntoEnemy == e:
								self.lockedOntoEnemy = None
			############################################
			############################################
			############################################

				

		elif self.state == "pause":
			if not self.cursr.visible:
				self.cursr.flipVisible()


			for event in events:
				if event.type == pg.KEYDOWN:
					key = event.dict['key']
					if key == pg.K_ESCAPE:
						self.state = "play"
						# self.pmenu.clearall()

						if self.cursr.visible:
							self.cursr.flipVisible()

						return 0, True
			
			self.pmenu.dispatch(events)
				
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

	'''
	def renderView(self):
		if self.state == "main-menu":
			pass

		elif self.state == "play" or self.state == "WE":
			belt = self.player.getBelt().getImg()

			#gets optimal view frame based on player
			
			mapx, mapy = self.map.getDrawingSize()

			# mapx, mapy = self.map.getMapSizePx()
			x, y = self.player.getRect().center
			w = self.display.getWH()[0]
			h = self.display.getWH()[1] - belt.get_height()
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
			playerOnZ = self.player.getZ()
			self.display.get().blit(self.map.getImageOfAndBelowZ(playerOnZ, view), (0,0))
			
			#retrieves all the events that happen to coincide with the view
			evtsToDisplay = self.eventForeground.getEventsOfAndBelow(playerOnZ, view)
			if evtsToDisplay:
				for each in evtsToDisplay:
					blitRelRect(each.getRect(), each.getArt())

			#blit player to screen
			blitRelRect(self.player.getRect(), self.player.getArt())

			# #blit enemies to screen
			for e in self.curEnemies:
				blitRelRect(e.getRect(), e.getArt(outline = (e is self.lockedOntoEnemy)))




			# surf = pg.Surface(g.TILE_RES)
			# surf.fill(g.GREEN)
			# surf.set_alpha(50)
			# for e in self.curEnemies:
			# 	blitRelRect(e.getRect(), e.getArt())
			# 	temp = e.currentPath
			# 	while temp != None:
			# 		rect = g.tile2rect(temp.tile)
			# 		blitRelRect(rect, surf)
			# 		temp = temp.parent





			#blit healthbars to screen
			for e in self.curEnemies:
				if e.getAggro():
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
			# belt = self.player.getBelt().getImg()
			self.display.get().blit(belt, (0,h))

			#blits the window to the display over everything else (top layer)
			self.display.get().blit(self.window, (0,0))
			
			pg.display.flip()

			self.view = view
		
		elif self.state == "pause":
			self.display.get().blit(self.pmenu.getDisp(), (0,0))
			pg.display.flip()
	'''


	def renderView(self):
		if self.state == "main-menu":
			pass

		elif self.state == "play" or self.state == "WE":
			belt = self.player.getBelt().getImg()

			#gets optimal view frame based on player
			
			mapx, mapy = self.map.getDrawingSize()

			# mapx, mapy = self.map.getMapSizePx()
			x, y = self.player.getRect().center
			w = self.display.getWH()[0]
			h = self.display.getWH()[1] - belt.get_height()
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
			self.display.get().blit(self.staticMap.subsurface(view), (0,0))

			maxZ = self.map.maxZ
			playerOnZ = self.player.getZ()
			for z in range(maxZ+1):
				tilesOccupied = set()

				evtsToDisplay = self.eventForeground.getEventsOf(z, view)
				if evtsToDisplay:
					for each in evtsToDisplay:
						blitRelRect(each.getRect(), each.getArt())

						for t0 in self.map.getTilesInRect(each.getRect()):
							tilesOccupied.add(t0)

				#enemies second
				for e in self.curEnemies:
					if e.getZ() == z:
						blitRelRect(e.getRect(), e.getArt(outline = (e is self.lockedOntoEnemy)))
						#hp bar if they're aggroed
						if e.getAggro():
							blitRelRect(e.getHPBarRect(), e.getHPBar())

						for t0 in self.map.getTilesInRect(e.getRect()):
							tilesOccupied.add(t0)

				#blit player to screen
				if z == playerOnZ:
					blitRelRect(self.player.getRect(), self.player.getArt())

					for t0 in self.map.getTilesInRect(self.player.getRect()):
						tilesOccupied.add(t0)

				for a in self.curAttacks:
					if (a.getZ() == z) and (a.getRect().colliderect(view)):
						blitRelRect(a.getRect(), a.getImg())

						for t0 in self.map.getTilesInRect(a.getRect()):
							tilesOccupied.add(t0)

				for t0 in tilesOccupied:
					if t0.getZ() > z:
						blitRelRect(t0.getRect(), t0.getImg())

			# surf = pg.Surface(g.TILE_RES)
			# surf.fill(g.GREEN)
			# surf.set_alpha(50)
			# for e in self.curEnemies:
			# 	blitRelRect(e.getRect(), e.getArt())
			# 	temp = e.currentPath
			# 	while temp != None:
			# 		rect = g.tile2rect(temp.tile)
			# 		blitRelRect(rect, surf)
			# 		temp = temp.parent

			# then the players belt is blitted
			# belt = self.player.getBelt().getImg()
			self.display.get().blit(belt, (0,h))

			#blits the window to the display over everything else (top layer)
			self.display.get().blit(self.window, (0,0))
			
			pg.display.flip()

			self.view = view
		
		elif self.state == "pause":
			self.display.get().blit(self.pmenu.getDisp(), (0,0))
			pg.display.flip()