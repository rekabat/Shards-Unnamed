import pygame as pg

class Display:
	def __init__(self):
		pg.display.init()

		self.width = 640+32*0
		self.height = 480+32*0
		# self.width = 1366 #
		# self.height = 768 #
		self.isFull=False
		self.screen = None

		self.createDisplay()
		
	def createDisplay(self):
		self.screen = pg.display.set_mode((self.width, self.height))
		# self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN|pygame.NOFRAME)
		
		self.screen.convert()
		
		pg.display.set_icon(pg.image.load('art/icon.png').convert())
		pg.display.set_caption('Shards')
	
	def get(self):
		return self.screen
		
	def getWH(self):
		return (self.width, self.height)
	
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