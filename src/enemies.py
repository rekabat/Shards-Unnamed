import pygame as pg

import general as g
import moveables

class Enemy(moveables.Moveable):
	def __init__(self, position, zs, size= (1,1), img='art/playersprite.png', pixStep = 75):
		moveables.Moveable.__init__(self, position, zs, size, img, pixStep)

		self.aggroRange = 7 #tiles (width)
		self.origin = self.rect.center

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
 
		# if rel[0]<-5:
		# 	mv += "L"
		# elif rel[0]>5:
		# 	mv += "R"

		# if rel[1]<-5:
		# 	mv += "U"
		# elif rel[1]>5:
		# 	mv += "D"

		self.forgetMovement()
		for m in mv:
			self.movingDirection(m)

		# rect, pos = self.ifMoved(mv, dt)

		# # 	self.move(rect, pos)
		# self.move(rect, [0], pos)
		self.move(mv, dt)