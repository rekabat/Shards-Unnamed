import pygame as pg

class Display:
	def __init__(self):
		pg.display.init()

		self.width = 640+32*11
		self.height = 480+32*2
		# self.width = 1366 #
		# self.height = 768 #
		self.isFull=False
		self.screen = None

		self.createDisplay()
	
	def get(self): return self.screen
	def getWH(self): return (self.width, self.height)
	
	def createDisplay(self):
		self.screen = pg.display.set_mode((self.width, self.height))
		# self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN|pygame.NOFRAME)
		
		self.screen.convert()
		
		pg.display.set_icon(pg.image.load('art/icon.png').convert())
		pg.display.set_caption('Shattered')

		splash = pg.image.load("art/shattered.png").convert_alpha()
		self.screen.blit(splash, ((self.width - splash.get_width())/2,(self.height - splash.get_height())/2))
		pg.display.flip()
	
	def toggleFull(self):
		if self.isFull:
			temp = pg.display.get_surface().convert()
			self.screen = pg.display.set_mode((self.width, self.height))
			self.screen.blit(temp, (0,0))
			# pygame.display.set_mode((self.width, self.height))
		else:
			
			temp = pg.display.get_surface().convert()
			self.screen = pg.display.set_mode((self.width, self.height), pg.FULLSCREEN)#|pygame.NOFRAME)
			self.screen.blit(temp, (0,0))
			# pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN|pygame.NOFRAME)
		
		self.isFull = not self.isFull