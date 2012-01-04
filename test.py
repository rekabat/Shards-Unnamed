import pygame
import random
from pygame.locals import *

pygame.init()

import source.display as display
import source.text as text
import source.mapParser as mapParser

screen = display.Display()
screen.createDisplay()

myMap = mapParser.Map('maps/large_map.map')

screen.get().blit(myMap.get(), (0,0))

pygame.display.flip()

running = True
while running:
		for event in pygame.event.get():
				if event.type == pygame.QUIT:
						running = False
						break
		
		pygame.time.Clock().tick(20)
