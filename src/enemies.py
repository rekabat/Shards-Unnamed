import pygame as pg

import general as g
import moveables
import attacks

class Enemy(moveables.Moveable):
	def __init__(self, position, zs, size= (1,1), img='art/playersprite.png', pixStep = 75):
		moveables.Moveable.__init__(self, position, zs, size, img, pixStep)

		self.aggroRange = 7 #tiles (width)
		self.origin = self.rect.center

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

	def getAlignment(self): return self.alignment
	def getStat(self, stat): return self.stats[stat]
	def getCurrentHP(self): return self.currentHP
	def getHPBar(self): return self.HPBar
	def getHPBarRect(self): return self.HPBarRect

	def tick(self, dt, player):
		if g.distance(player.getRect().center, self.getRect().center)>= self.aggroRange*g.TILE_RES[0]:
			if g.distance(self.origin, self.getRect().center) > 5: #tolerance of 5 pixels from the origin
				xp, yp = self.origin
			else:
				return
		else:
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


	def tick0(self, dt, player):
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