import pygame

WHITE=(255,255,255)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
BLACK=(0,0,0)

class Text:
	def __init__(self, str, size, color=WHITE, antialiasing=True):
		self.str = str
		self.color = color
		self.size = size
		self.antialiasing = antialiasing
	
	def get(self):
		return pygame.font.Font(None, self.size).render(self.str, self.antialiasing, self.color)
	
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
		