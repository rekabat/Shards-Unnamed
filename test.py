import pygame
import random
from pygame.locals import *

pygame.init()

import source.display as display
import source.text as text
import source.mapParser as mapParser

screen = display.Display()
screen.createDisplay()



myMap = mapParser.Map('maps/demo.map')

screen.get().blit(myMap.get(), (0,0))

pygame.display.flip()

while 1:
	pygame.time.Clock().tick(1000)