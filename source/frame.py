import pygame as pg

class Frame:
	def __init__(self, surface, pixel, screen):
		self.surface = surface
		self.pixel = pixel
		self.screen = screen
		
		self.updateFrame(self.pixel)
	
	def updateFrame(self, pixel):
		wh = self.screen.getWH()
		placing=pg.Rect(pixel[0]-wh[0]*.5, pixel[1]-wh[1]*.5, wh[0], wh[1])
		# print pixel[0]+wh[0]*.5, pixel[1]+wh[1]*.5
		print self.surface.get_rect(), placing, self.surface.get_rect().contains(placing)
		if self.surface.get_rect().contains(placing):
			self.screen.get().blit(self.surface.subsurface(placing), (0,0))
			pg.display.flip()
			return True
		return False