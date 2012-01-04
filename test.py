import pygame
import random
from pygame.locals import *
import time

pygame.init()

import source.display as display
import source.text as text
import source.mapParser as mapParser
import source.frame as frame
import source.moveables as moveables

screen = display.Display()
screen.createDisplay()

myMap = mapParser.Map('maps/mapgen_map.map')


currentPix = myMap.tile2pix((12,10))
player = moveables.Moveable(myMap, (24,0), (1,1), 'art/player.png')

frm = frame.Frame(myMap.get(), currentPix, screen)

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
	if up:
		newPix = (currentPix[0], currentPix[1]-1)
		if frm.updateFrame(newPix):
			currentPix=newPix
	if down:
		newPix = (currentPix[0], currentPix[1]+1)
		if frm.updateFrame(newPix):
			currentPix=newPix
	if left:
		newPix = (currentPix[0]-1, currentPix[1])
		if frm.updateFrame(newPix):
			currentPix=newPix
		frm.updateFrame(currentPix)
		player.move("L")
	if right:
		newPix = (currentPix[0]+1, currentPix[1])
		if frm.updateFrame(newPix):
			currentPix=newPix
		frm.updateFrame(currentPix)
		player.move("R")
	pygame.time.Clock().tick(1000)

