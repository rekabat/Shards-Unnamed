import pygame
import random
from pygame.locals import *

pygame.init()

import source.display as display
import source.text as text

screen = display.Display()
screen.createDisplay()



#################################################################
#################################################################
#################################################################
#################################################################

print text.Text("Play Game", 50, text.GREEN).place(screen.get(), (screen.get().get_rect().centerx, int(screen.get().get_rect().centery*(2./3))))
print text.Text("Load Game", 50, text.RED).place(screen.get(), (screen.get().get_rect().centerx, int(screen.get().get_rect().centery*(4./3))))
pygame.display.flip()

flag = False
running = True
while running:
	for event in pygame.event.get():
		if (event.type == pygame.QUIT):
			running = False
			break
		# elif (event.type == pygame.KEYDOWN):
		elif (event.type == pygame.MOUSEMOTION):
			wh= screen.getWH()
			for i in range(int(wh[0]*wh[1]*.00013)): #Change this number to increase pixel populating rate
				a = random.randint(0,255)
				b = random.randint(0,255)
				c = random.randint(0,255)
				# screen.get().fill((a,b,c))
				x = random.randint(0,wh[0])
				y = random.randint(0,wh[1])
				screen.get().set_at((x,y),(a,b,c))
				# print a,b,c
				# screen.get().fill((100,100,200))
				pygame.display.flip()
		elif (event.type == pygame.KEYDOWN):
			if event.dict['unicode'] == "t":
				screen.toggleFull()
			'''			
			if flag:
				screen.get().fill((0,0,0))
				pygame.display.flip()
			else:
				a = random.randint(0,255)
				b = random.randint(0,255)
				c = random.randint(0,255)
				# screen.get().fill((a,b,c))
				x = random.randint(0,screen.getWH()[0])
				y = random.randint(0,screen.getWH()[1])
				screen.get().set_at((x,y),(a,b,c))
				print a,b,c
				# screen.get().fill((100,100,200))
				pygame.display.flip()
			
			flag= not flag
			'''
		
		print event
	
	pygame.time.Clock().tick(20)

#################################################################
#################################################################
#################################################################
#################################################################

# player = pygame.image.load('art/player.png').convert()
# background = pygame.image.load('art/floors.png').convert()
# screen.blit(background, (0,0))
# cddrive = pygame.cdrom.CD(0)
# cddrive.init()
# cddrive.eject()
# pygame.time.delay(3000)

# class GameObject:
	# def __init__(self, image, height, speed):
		# self.speed = speed
		# self.image = image
		# self.pos = image.get_rect().move(0, height)
	# def move(self):
		# self.pos = self.pos.move(0, self.speed)
		# if self.pos.right > 600:
			# self.pos.left = 0



			
# objects = []
# for x in range(10): 		#create 10 objects
	# o = GameObject(player, x*40, x)
	# objects.append(o)
# while 1:
	# for event in pygame.event.get():
		# if event.type in (QUIT, KEYDOWN):
			# sys.exit()
	# for o in objects:
		# screen.blit(background, o.pos, o.pos)
		# for o in objects:
			# o.move()
			# screen.draw(o.image, o.pos)
		# pygame.display.update()
		# pygame.time.delay(100)


