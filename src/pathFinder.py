from copy import deepcopy as dc

class nodule:
	def __init__(self, tile, g, h, parent, cameFrom):
		self.tile = tile
		
		self.cost = g+h
		self.movementcost = g
		# self.heuristiccost = h

		self.parent = parent
		self.cameFrom = cameFrom
		if self.parent is None:
			self.tilesOnPath = 1
		else:
			self.tilesOnPath = self.parent.tilesOnPath + 1

class PathFinder:
	def __init__(self):
		self.z_pos_tileblocked = None
		self.mapSize_tiles = None
		self.z_closed = None

	def loadMap(self, (z_pos_tileblocked, mapSize_tiles)):
		self.z_pos_tileblocked = z_pos_tileblocked
		self.mapSize_tiles = mapSize_tiles
		self.z_closed = {}
		for z in z_pos_tileblocked:
			self.z_closed[z] = []
			for x in range(self.mapSize_tiles[0]):
				for y in range(self.mapSize_tiles[1]):
					if (x,y) in self.z_pos_tileblocked[z]:
						if self.z_pos_tileblocked[z][(x,y)]:
							self.z_closed[z].append((x,y))
					else:
						self.z_closed[z].append((x,y))


	def findPath_from_to(self, (currentTile, targetTile, limit)):
		#currentTile-> xyz
		#targetTile -> xyz
		#limit		-> the farthest it will go to find a path

		if currentTile[2] != targetTile[2]: #cannot find a path to a tile on a different z yet
			return

		z = currentTile[2]
		currentTile = (currentTile[0], currentTile[1])
		targetTile = (targetTile[0], targetTile[1])

		current = nodule(currentTile, 0, 10*(abs(currentTile[0]-targetTile[0])+abs(currentTile[1]-targetTile[1])), None, (0,0))
			
		open = {current.tile: current}
		openByCost = {current.cost: [current]}
		closed = dc(self.z_closed[z])

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
						g = mincost.movementcost + cost
						h = 10*(abs(new[0]-targetTile[0])+abs(new[1]-targetTile[1]))

						cost = g+h
						
						if new in open: #already tested on another route
							oldcost = open[new].cost
							if cost < oldcost: #it's a better route than the last one found to get here
								#remove from openByCost
								openByCost[oldcost].remove(open[new])
								if len(openByCost[oldcost]) == 0:
									del(openByCost[oldcost])
								#replace in open
								open[new].cost = cost
								open[new].movementcost = g
								# open[new].heuristiccost = h
								open[new].parent = mincost
								open[new].cameFrom = (x,y)
								#put in openByCost
								if cost not in openByCost.keys():
									openByCost[cost] = []
								openByCost[cost].append(open[new])

						else: #not tested yet
							
							# if self.GI.collisionWithBlockedRect(g.tile2rect(new), self.getZs(), player = False, ignoreEnemy=self):
							
							#off of the map
							if new[0]<0 or new[1]<0 or new[0]>=self.mapSize_tiles[0] or new[1]>=self.mapSize_tiles[1]:
									return False

							#blocked
							# if self.GI.collisionWithBlockedTile(new, self.getZs(), player = False, ignoreEnemy=self):
							# if self.GI.collisionWithBlockedTile(new, self.getZ(), player = False, enemies = False):
							#  	closed.append(new)
							#  	return False
							
							#add to open
							nod = nodule(new, g, h, mincost, (x,y))
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

		#get a list of tiles to move along
		ret = []
		while mincost != None:
			ret.append(mincost.tile)
			mincost = mincost.parent
		ret.reverse()

		return ret