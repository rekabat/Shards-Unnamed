import pygame as pg

import general as g
import moveables
import attacks


class nodule:
	def __init__(self, tile, cost, parent, cameFrom):
		self.tile = tile
		self.cost = cost
		self.parent = parent
		self.cameFrom = cameFrom
		if self.parent is None:
			self.tilesOnPath = 1
		else:
			self.tilesOnPath = self.parent.tilesOnPath + 1
	
def bottomNodule(nod):
		while nod.parent != None:
			nod = nod.parent
		return nod

def deleteBottomNodule(nod):
		if nod.parent == None:
			return False
		else:
			while nod.parent != None:
				if nod.parent.parent != None:
					nod = nod.parent
				else:
					nod.parent = None
			return True

	# def copy(self):
	# 	return nodule((self.tile[0]+0, self.tile[1]+0), self.cost+0, self.parent)


class Enemy(moveables.Moveable):
	def __init__(self, GI, position, zs, size= (1,1), img='art/playersprite.png', pixStep = 75):
		moveables.Moveable.__init__(self, position, zs, size, img, pixStep)

		self.GI = GI
		self.targetTile = None
		self.currentTile = None
		self.headingFor = None

		self.aggroRange = 7 #tiles (width)
		self.aggro = False
		self.origin = self.rect.topleft

		self.alignment = 1
		self.spells = [attacks.fireball(alignment = self.alignment)]
		self.atkRate = 1 #how many attacks per second
		self.secondSinceAtk = 0

		self.stats = {	'lvl': 	0,	\
						'hp': 	5,	\
						'def': 	1,	\
						'mag': 	1,	\
						'atk': 	1	} #stats

		self.currentHP = 5

		#hp bar with a black border
		self.HPBar = pg.Surface((g.TILE_RES[0], int(g.TILE_RES[1]/4.)))
		for x in range(g.TILE_RES[0]):
			for y in range(int(g.TILE_RES[1]/4.)):
					if (x == 0) or (y == 0) or (x == g.TILE_RES[0]-1) or (y == int(g.TILE_RES[1]/4.)-1):
						self.HPBar.set_at((x,y), g.BLACK)
		self.updateHPBar()
		self.HPBarRect = None
		self.placeHPBar()

	def getAggro(self): return self.aggro
	def getAlignment(self): return self.alignment
	def getStat(self, stat): return self.stats[stat]
	def getCurrentHP(self): return self.currentHP
	def getHPBar(self): return self.HPBar
	def getHPBarRect(self): return self.HPBarRect

	def Astar(self, currentTile, targetTile, limit = None):
		current = nodule(currentTile, 100*(abs(currentTile[0]-targetTile[0])+abs(currentTile[1]-targetTile[1])), None, (0,0))
			
		open = {current.tile: current}
		openByCost = {current.cost: [current]}
		closed = []

		while 1:
			# mincost = nodule(None, 999999999999999999999, None)
			# for each in open.keys():
			# 	if open[each].cost < mincost.cost:
			# 		mincost = open[each]

			# if mincost.tile == targetTile or len(open.keys()) == 0:
			# 	break


			#it should only need open!!!!!
			#it should only need open!!!!!
			#it should only need open!!!!!
			#it should only need open!!!!!
			#it should only need open!!!!!
			#it should only need open!!!!!
			#it should only need open!!!!!
			#it should only need open!!!!!
			#it should only need open!!!!!
			if len(open) == 0 or len(openByCost) == 0:
				mincost = None
				break

			mincost = openByCost[min(openByCost)][0]

			if mincost.tile == targetTile:
				break

			#remove from open
			del(open[mincost.tile])
			#remove from openByCost
			openByCost[mincost.cost].remove(mincost)
			if len(openByCost[mincost.cost]) == 0:
				del(openByCost[mincost.cost])
			#add to closed
			closed.append(mincost.tile)

			tooFar = False
			if limit:
				if mincost.tilesOnPath > limit:
					tooFar = True
			if not tooFar:
				def makeRelNode((x,y), cost):
					new = (mincost.tile[0]+x, mincost.tile[1]+y)
					
					if new not in closed: #not rejected yet
						cost = mincost.cost + cost + 10*(abs(new[0]-targetTile[0])+abs(new[1]-targetTile[1]))
						
						if new in open: #already tested on another route
							oldcost = open[new].cost
							if cost < oldcost: #it's a better route than the last one found to get here
								#remove from openByCost
								openByCost[oldcost].remove(open[new])
								if len(openByCost[oldcost]) == 0:
									del(openByCost[oldcost])
								#replace in open
								open[new].cost = cost
								open[new].parent = mincost
								open[new].cameFrom = (x,y)
								#put in openByCost
								if cost not in openByCost.keys():
									openByCost[cost] = []
								openByCost[cost].append(open[new])

						else: #not tested yet
							
							# if self.GI.collisionWithBlockedRect(g.tile2rect(new), self.getZs(), player = False, ignoreEnemy=self):
							
							#off of the map\
							if new[0]<0 or new[1]<0 or new[0]>=self.GI.map.getMapSizeTiles()[0] or new[1]>=self.GI.map.getMapSizeTiles()[1]:
									return False
							#blocked
							if self.GI.collisionWithBlockedTile(new, self.getZs(), player = False, ignoreEnemy=self):
							 	closed.append(new)
							 	return False
							
							#add to open
							nod = nodule(new, cost, mincost, (x,y))
							open[new] = nod
							#add to openByCost
							if cost not in openByCost.keys():
								openByCost[cost] = []
							openByCost[cost].append(nod)
					return True

				# if you can't go up or left, an up-left movement (even if it was valid)
				# would clip through blocked tiles, so those need to be avoided


				#original
				# up = makeRelNode((0,-1), 10) #u
				# down = makeRelNode((0,+1), 10) #d

				# if makeRelNode((-1,0), 10): #l
				# 	if up: #u
				# 		makeRelNode((-1,-1), 14)#ul
				# 	if down: #d
				# 		makeRelNode((-1,+1), 14)#dl
				# if makeRelNode((+1,0), 10): #r
				# 	if up: #u
				# 		makeRelNode((+1,-1), 14)#ur
				# 	if down: #d
				# 		makeRelNode((+1,+1), 14)#dr


				#seems to be working
				# up = (mincost.cameFrom != (0,+1)) and makeRelNode((0,-1), 10) #u
				# down = (mincost.cameFrom != (0,-1)) and makeRelNode((0,+1), 10) #d
				# left =(mincost.cameFrom != (+1,0)) and  makeRelNode((-1,0), 10)
				# right =(mincost.cameFrom != (-1,0)) and  makeRelNode((+1,0), 10)

				# if left: #l
				# 	if up: #u
				# 		makeRelNode((-1,-1), 14)#ul
				# 	if down: #d
				# 		makeRelNode((-1,+1), 14)#dl
				# if right: #r
				# 	if up: #u
				# 		makeRelNode((+1,-1), 14)#ur
				# 	if down: #d
				# 		makeRelNode((+1,+1), 14)#dr

				#seems best
				# cameFrom                     ``up``                         ``down``                         ``left``                        ``right``
				up    = (mincost.cameFrom != (0,+1))                                  and (mincost.cameFrom != (+1,0)) and (mincost.cameFrom != (-1,0)) and makeRelNode((0,-1), 10)
				down  =                                  (mincost.cameFrom != (0,-1)) and (mincost.cameFrom != (+1,0)) and (mincost.cameFrom != (-1,0)) and makeRelNode((0,+1), 10)
				left  = (mincost.cameFrom != (0,+1)) and (mincost.cameFrom != (0,-1)) and (mincost.cameFrom != (+1,0))                                  and makeRelNode((-1,0), 10)
				right = (mincost.cameFrom != (0,+1)) and (mincost.cameFrom != (0,-1))                                  and (mincost.cameFrom != (-1,0)) and makeRelNode((+1,0), 10)

				if left or up: #l
					makeRelNode((-1,-1), 14)#ul
				if left or down: #d
					makeRelNode((-1,+1), 14)#dl
				if right or up: #u
					makeRelNode((+1,-1), 14)#ur
				if right or down: #d
						makeRelNode((+1,+1), 14)#dr





		self.headingFor = mincost

	def tick(self, dt, foundOnePathAlready):
		player = self.GI.player

		if self.secondSinceAtk != 0:
			self.secondSinceAtk += dt
			if self.secondSinceAtk >= self.atkRate:
				self.secondSinceAtk = 0

		#touching the player
		if self.getRect().colliderect(player.getRect()):
			self.undoMove()
			if self.secondSinceAtk == 0:
				self.secondSinceAtk+=.001
				return self.spells[0].cast(self.getRect(), self.facing), False

		currentTile = g.pix2tile(self.getRect().center)

		if g.distance(player.getRect().center, self.getRect().center) < self.aggroRange*g.TILE_RES[0]:
			targetTile = g.pix2tile(player.getRect().center)
			self.aggro = True
			toOrigin = False
		# elif g.distance(self.origin, self.getRect().center) > 3: #tolerance of 5 pixels from the origin
			# toOrigin = True
		else:
			targetTile = g.pix2tile(self.origin)
			self.aggro = False
			toOrigin = True
			# self.headingFor = None
			# return False, False
		
		if currentTile[0] == targetTile[0] and currentTile[1] == targetTile[1]:
			return False, False

		if self.targetTile == targetTile and self.headingFor != None:
			bottom = bottomNodule(self.headingFor).tile
			if bottom != currentTile:
				xp, yp = g.tile2pix(bottom, center = False)
				xs, ys = self.getRect().topleft

				mv = ""

				if xp-xs<0:
					mv += "L"
				elif xp-xs>0:
					mv += "R"

				if yp-ys<0:
					mv += "U"
				elif yp-ys>0:
					mv += "D"

				self.forgetMovement()
				for m in mv:
					self.movingDirection(m)

				if len(mv) == 2:
					mv = [mv, mv[0], mv[1]]
				else:
					mv = [mv]
				for each in mv:
					self.move(each, dt)

					# Check if the movement is valid by making a smaller rectangle and seeing
					smallerRect=pg.Rect((0,0),(self.getRect().width*.87, self.getRect().height*.87))
					smallerRect.center = self.getRect().center

					if self.GI.collisionWithBlockedRect(smallerRect, self.getZs(), player = False, ignoreEnemy=self):
						self.undoMove()
					else:
						break

				self.placeHPBar()

				return False, False
				
			else:
				if not deleteBottomNodule(self.headingFor):
					self.headingFor = None
		elif not foundOnePathAlready:
			self.targetTile = targetTile	
			self.currentTile = currentTile

			if toOrigin:
				self.Astar(currentTile, targetTile)
			else:
				self.Astar(currentTile, targetTile, limit = 1.5*self.aggroRange)

			return False, True
		return False, False





	def tick1(self, dt, foundOnePathAlready):
		player = self.GI.player

		if g.distance(player.getRect().center, self.getRect().center) >= self.aggroRange*g.TILE_RES[0]:
			self.aggro = False
			if g.distance(self.origin, self.getRect().center) > 5: #tolerance of 5 pixels from the origin
				xp, yp = self.origin
			else:
				return
		else:
			self.aggro = True
			xp, yp = player.getRect().center

		xs, ys = self.getRect().center

		rel = (xp-xs, yp-ys)


		#distance between a point (x0, y0) and line (ax+by+c=0)
			# |a*x0 + b*y0 + c| / sqrt(a^2 + b^2)
		
		u_d = abs(xs-xp)
		l_r = abs(ys-yp)
		#y =  x + (ys-xs)   ->  (-x) + y + (-ys+xs) = 0
		ul_dr = abs(-xp+yp+(xs-ys)) / 1.41421356 #sqrt(2)
		#y = -x + (ys+xs)   ->   x   + y + (-ys-xs) = 0
		dl_ur = abs(xp+yp-(ys+xs)) / 1.41421356 #sqrt(2)

		mv = ""

		if u_d <= ul_dr and u_d <= dl_ur and u_d<=l_r:
			if rel[1]<0:
				mv = "U"
			elif rel[1]>0:
				mv = "D"
		elif l_r <= ul_dr and l_r <= dl_ur:
			if rel[0]<0:
				mv = "L"
			elif rel[0]>0:
				mv = "R"
		elif ul_dr <= dl_ur:
			if rel[1]<0:
				mv = "UL"
			elif rel[1]>0:
				mv = "DR"
		else:
			if rel[1]<0:
				mv = "UR"
			elif rel[1]>0:
				mv = "DL"

		self.forgetMovement()
		for m in mv:
			self.movingDirection(m)

		self.move(mv, dt)

		self.placeHPBar()

		if self.secondSinceAtk != 0:
			self.secondSinceAtk += dt
			if self.secondSinceAtk >= self.atkRate:
				self.secondSinceAtk = 0

		#touching the player
		if self.getRect().colliderect(player.getRect()):
			self.undoMove()
			if self.secondSinceAtk == 0:
				self.secondSinceAtk+=.001
				return self.spells[0].cast(self.getRect(), self.facing)

		return False


	def tick0(self, dt, foundOnePathAlready):
		player = self.GI.player

		if g.distance(player.getRect().center, self.getRect().center)>= self.aggroRange*g.TILE_RES[0]:
			if g.distance(self.origin, self.getRect().center) > 5: #tolerance of 5 pixels from the origin
				xp, yp = self.origin
			else:
				return
		else:
			xp, yp = player.getRect().center

		xs, ys = self.getRect().center

		rel = (xp-xs, yp-ys)

		mv = ""

		if rel[0]<-5:
			mv += "L"
		elif rel[0]>5:
			mv += "R"

		if rel[1]<-5:
			mv += "U"
		elif rel[1]>5:
			mv += "D"

		self.forgetMovement()
		for m in mv:
			self.movingDirection(m)

		self.move(mv, dt)

		self.placeHPBar()

	def takeHP(self, amt):
		self.currentHP -= amt
		if self.currentHP<=0:
			return True
		self.updateHPBar()
		return False

	def updateHPBar(self):
		x = self.HPBar.get_width()  - 2
		y = self.HPBar.get_height() - 2

		self.HPBar.subsurface(pg.Rect((1,1), (x,y))).fill(g.WHITE)

		portion = float(self.currentHP) / self.getStat('hp')
		
		x*=portion

		self.HPBar.subsurface((1,1), (x,y)).fill(g.RED)

	def placeHPBar(self):
		self.HPBarRect = pg.Rect((self.getRect().left, self.getRect().top - self.HPBar.get_height()), self.HPBar.get_size())