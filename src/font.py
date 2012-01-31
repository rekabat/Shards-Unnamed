import pygame as pg
import general as g

class Text:
	def __init__(self, str, size, color=g.WHITE, antialiasing=True):
		self.str = str
		self.color = color
		self.size = size
		self.antialiasing = antialiasing

		self.img = pg.font.Font(None, self.size).render(self.str, self.antialiasing, self.color)
	
	def get(self):
		return self.img
	
	def getSize(self):
		return self.size
	
	def getStr(self):
		return self.str
	
	def getColor(self):
		return self.color
	
	def getAA(self):
		return self.antialiasing
	
	def getLength(self):
		return self.get().get_rect().width

	def place(self, surface, position, center=True):
		strSurface = self.get()
		if center:
			rect = strSurface.get_rect()
			rect.centerx = position[0]
			rect.centery = position[1]
			surface.blit(strSurface, rect)
			
			return rect
		else:
			surface.blit(strSurface, position)
			
			return 0
	
	def concatenate(self, texts):
		newStr = self.getStr()
		for each in texts:
			if each.getSize() != self.getSize():
				print "Error, text blocks different size, can not concatenate."
				return False
			else:
				newStr+=each.getStr()
		
		return Text(newStr, self.getSize(), self.getColor(), self.getAA())

class Font:
	def __init__(self):
		self.fontsize = (32, 64) # width/height in pixels

		letters = pg.image.load("art/font/letters.png").convert_alpha()
		letters = [letters.subsurface(pg.Rect((i,0),fontsize)).copy() for i in range(0,831,32)]
		
		self.chars = {"A": letters[0], "B": letters[1], \
				"C": letters[2], "D": letters[3], \
				"E": letters[4], "F": letters[5], \
				"G": letters[6], "H": letters[7], \
				"I": letters[8], "J": letters[9], \
				"K": letters[10], "L": letters[11], \
				"M": letters[12], "N": letters[13], \
				"O": letters[14], "P": letters[15], \
				"Q": letters[16], "R": letters[17], \
				"S": letters[18], "T": letters[19], \
				"U": letters[20], "V": letters[21], \
				"W": letters[22], "X": letters[23], \
				"Y": letters[24], "Z": letters[25]}