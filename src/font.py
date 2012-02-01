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
	
	def get(self):
		return self.img
	
	def getSize(self):
		return self.size
	
	def getStr(self):
		return self.str
	
	# def getColor(self):
	# 	return self.color
	
	# def getAA(self):
	# 	return self.antialiasing
	
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
		
		return Text(newStr, self.getSize(), self.fontsize, self.chars)

class Font:
	def __init__(self):
		self.fontsize = (32, 64) # width/height in pixels
		self.chars = {}
		fontkey = open("art/font/fontkey.txt", "r")
		fontkey = fontkey.readlines()
		fontkey = [each[:-1] for each in fontkey] #remove newlines
		print fontkey

		for key in fontkey:
			image, letters = key.split(" - ")
			image = pg.image.load("art/font/"+image).convert_alpha()
			x = 0
			for l in letters:
				self.chars[l] = image.subsurface(pg.Rect((x,0),self.fontsize)).copy()
				x+=self.fontsize[0]
		
		# print self.chars


		# letters = pg.image.load("art/font/letters.png").convert_alpha()
		# letters = [letters.subsurface(pg.Rect((i,0),self.fontsize)).copy() for i in range(0,831,32)]
		# self.chars.update({	"A": letters[0],  "B": letters[1],  "C": letters[2],  "D": letters[3],  \
		# 					"E": letters[4],  "F": letters[5],  "G": letters[6],  "H": letters[7],  \
		# 					"I": letters[8],  "J": letters[9],  "K": letters[10], "L": letters[11], \
		# 					"M": letters[12], "N": letters[13], "O": letters[14], "P": letters[15], \
		# 					"Q": letters[16], "R": letters[17], "S": letters[18], "T": letters[19], \
		# 					"U": letters[20], "V": letters[21], "W": letters[22], "X": letters[23], \
		# 					"Y": letters[24], "Z": letters[25]})

		# numbers = pg.image.load("art/font/numbers.png").convert_alpha()
		# numbers = [numbers.subsurface(pg.Rect((i,0),self.fontsize)).copy() for i in range(0,319,32)]
		# self.chars.update({	"1": numbers[0], "2": numbers[1], "3": numbers[2], "4": numbers[3], \
		# 					"5": numbers[4], "6": numbers[5], "7": numbers[6], "8": numbers[7], \
		# 					"9": numbers[8], "0": numbers[9]})

		# symbols = pg.image.load("art/font/symbols.png").convert_alpha()
		# symbols = [symbols.subsurface(pg.Rect((i,0),self.fontsize)).copy() for i in range(0,959,32)]
		# self.chars.update({	"!": symbols[0],  "@": symbols[1],  "#": symbols[2],  "$": symbols[3], \
		# 					"%": symbols[4],  "^": symbols[5],  "&": symbols[6],  "*": symbols[7], \
		# 					"(": symbols[8],  ")": symbols[9],  "_": symbols[10], "-": symbols[11], \
		# 					"+": symbols[12], "=": symbols[13], "[": symbols[14], "]": symbols[15], \
		# 					"{": symbols[16], "}": symbols[17], "|": symbols[18], "\\": symbols[19], \
		# 					'"': symbols[20], "'": symbols[21], ":": symbols[22], ";": symbols[23], \
		# 					"<": symbols[24], ">": symbols[25], ",": symbols[26], ".": symbols[27], \
		# 					"?": symbols[28], "/": symbols[29]})

	def text(self, str, size):
		return Text(str, size, self.fontsize, self.chars)