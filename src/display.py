import pygame

class Display:
	def __init__(self):
		self.width = 640
		self.height = 480
		self.isFull=False
		self.screen = None

		self.createDisplay()
		
	def createDisplay(self):
		self.screen = pygame.display.set_mode((self.width, self.height))
		# self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN|pygame.NOFRAME)
		
		self.screen.convert()
		
		pygame.display.set_icon(pygame.image.load('art/icon.png').convert())
		pygame.display.set_caption('Shards')
	
	def get(self):
		return self.screen
		
	def getWH(self):
		return (self.width, self.height)
	
	def toggleFull(self):
		if self.isFull:
			temp = pygame.display.get_surface().convert()
			self.screen = pygame.display.set_mode((self.width, self.height))
			self.screen.blit(temp, (0,0))
			# pygame.display.set_mode((self.width, self.height))
		else:
			
			temp = pygame.display.get_surface().convert()
			self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN|pygame.NOFRAME)
			self.screen.blit(temp, (0,0))
			# pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN|pygame.NOFRAME)
		
		self.isFull = not self.isFull