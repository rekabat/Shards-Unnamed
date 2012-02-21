import pygame as pg
import general as g

class Text:
	def __init__(self, str, size, fontsize, chars):
		self.str = str.upper()
		self.size = int(size)
		self.height = int(size)
		self.width = int(size/2)
		self.fontsize = fontsize

		self.chars = {}
		for key in chars.keys():
			self.chars[key] = pg.transform.scale(chars[key], (self.width, self.height))

		self.img = pg.Surface((self.width*len(str), self.height), pg.SRCALPHA, 32).convert_alpha()
		x=0
		for a in self.str:
			if a in self.chars.keys():
				self.img.blit(self.chars[a], (x,0))
			elif a == " ":
				pass
			else:
				self.img.blit(self.chars["Z"], (x,0))

			x+=self.width
	
	def get(self): return self.img
	def getSize(self): return self.size
	def getStr(self): return self.str
	def getLength(self): return self.get().get_rect().width
	
	# def getColor(self):
	# 	return self.color
	
	# def getAA(self):
	# 	return self.antialiasing

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
		
		return Text(newStr, self.getSize(), self.fontsize, self.chars)

class Font:
	def __init__(self):
		self.fontsize = (32, 64) # width/height in pixels
		self.chars = {}

		fontkey = open("art/font/fontkey.txt", "r").readlines()
		fontkey = [each[:-1] for each in fontkey] #remove newlines
		for key in fontkey:
			image, letters = key.split(" - ")
			image = pg.image.load("art/font/"+image).convert_alpha()
			x = 0
			for l in letters:
				self.chars[l] = image.subsurface(pg.Rect((x,0),self.fontsize)).copy()
				x+=self.fontsize[0]

	def text(self, str, size):
		return Text(str, size, self.fontsize, self.chars)