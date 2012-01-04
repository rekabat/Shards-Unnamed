import pygame
import random
from pygame.locals import *
import time

pygame.init()

import source.display as display
import source.text as text
import source.mapParser as mapParser
import source.moveables as moveables

screen = display.Display()
screen.createDisplay()

myMap = mapParser.Map('maps/mapgen_map.map')


currentPix = myMap.tile2pix((12,10))
player = moveables.Player(myMap, (12,10), screen)

# frm = frame.Frame(myMap.get(), currentPix, screen)

up = False
down = False
left = False
right = False

running = True
while running:
	for event in pygame.event.get():
		if (event.type == pygame.QUIT):
			running = False
			break
		elif (event.type == pygame.KEYDOWN):
			# print "down", event.dict
			if event.dict['key'] == 119:
				up = True
			if event.dict['key'] == 115:
				down = True
			if event.dict['key'] == 97:
				left = True
			if event.dict['key'] == 100:
				right = True
			
		elif (event.type == pygame.KEYUP):
			# print "up", event.dict
			if event.dict['key'] == 119:
				up = False
			if event.dict['key'] == 115:
				down = False
			if event.dict['key'] == 97:
				left = False
			if event.dict['key'] == 100:
				right = False
	
	mv = ""
	if up or down or left or right:
		if up:
			mv += "U"
		if down:
			mv += "D"
		if left:
			mv += "L"
		if right:
			mv += "R"
		player.move(mv)
		
	pygame.time.Clock().tick()
	

