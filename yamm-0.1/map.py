#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# map.py
#
# File created by herve couvelard - herve@viva-vous.net
# 05 2010
# license : gplv3
#
#
import sys, os, pygame

from pygame.locals import *
import pygame.rect
from Tkinter import *
import tkFileDialog

from interaction import *
from tuiles import *
from load_save import *


class config():

  def __init__(self):
    self.config={'size_tile_x':32,'size_tile_y':32,'size_map_x':25,'size_map_y':15,'margin':10,
		'tiles_file':'','tiles_file_size_x':'','tiles_file_size_y':'',
		  'map_pos_x':'','map_pos_y':'','map_size_x':'','map_size_y':'','tile_image':'',
		  'active_tile_x':'','active_tile_y':'','active_tile_tiles_x':'','active_tile_tiles_y':''}

  def set_active_tile(self,x,y):
      self.config['active_tile_tiles_x']=x*self.config['size_tile_x']
      self.config['active_tile_x']=x
      self.config['active_tile_y']=y
      self.config['active_tile_tiles_y']=y*self.config['size_tile_y']

  def get_window_size(self):
      self.window_size_x=3*self.config['margin']+self.config['tiles_file_size_x']+self.config['map_size_x']
      self.window_size_y=3*self.config['margin']+self.config['tiles_file_size_y']+self.config['size_tile_y']
      return(self.window_size_x,self.window_size_y)

  def get_map_rect(self):
      return (	[self.config['map_pos_x'],
		self.config['map_pos_y'],
		self.config['map_pos_x']+self.config['size_map_x']*self.config['size_tile_x'],
		self.config['map_pos_y']+self.config['size_map_y']*self.config['size_tile_y'] ])
		

class map():

  def __init__(self):
    pygame.init()
    self.window = pygame.display.set_mode((600,200), RESIZABLE)
    pygame.display.set_caption('Yamm - V 0.01 press F1 for help')
    self.config=config()
    self.screen = pygame.display.get_surface()
    self.mon_aide= aide()
    self.mapping={}
    self.interaction=interaction()
    self.load_save=load_save()
    self.game()



  def prepare_map(self):
    	self.tuiles=tuiles(self.config)
	self.mymap=map_draw(self.config,self.tuiles)
	self.window = pygame.display.set_mode(self.config.get_window_size(), RESIZABLE)
	self.tuiles.affiche(self.screen)
	self.mymap.affiche(self.screen)
	pygame.display.update()


  def open_file(self):
    tk_root = Tk()
    tk_root.withdraw()
    filetype=[('supported', ('*.hmp', '*.png', '*.jpg', '*.bmp')), ('map files', '*.hmp'), ('tilesets', ('*.png', '*.jpg', '*.bmp'))]
    fichier=tkFileDialog.askopenfilename( title = 'File Select',filetypes=filetype)
    if fichier:
      if fichier.endswith(".bmp") or fichier.endswith(".png") or fichier.endswith(".jpg"):
	self.config.config['tiles_file']=fichier	
	self.prepare_map()
      elif fichier.endswith(".hmp"):
	self.load_save.load(self.config,self.mapping,fichier)
	self.prepare_map()
	self.active_tuile=active_tiles (self.config,self.mapping,start=0)
	self.active_tuile.reload_save_map(self.screen)


  def input(self, events):
    for event in events:
      if event.type == KEYUP and event.key == K_ESCAPE or event.type == QUIT:
	sys.exit(0)
      if event.type == MOUSEBUTTONDOWN:
	left, top = pygame.mouse.get_pos()
	
	try :
	  x=self.tuiles.get_click(left,top,self.screen) ### click on tile set
	  if x:
	    self.active_tuile=active_tiles(self.config,self.mapping)
	    self.active_tuile.affiche(self.screen)
	except :
	  pass
	
	try:
	  x,y=self.mymap.get_click(left,top,self.screen) # click on map draw
	  if event.button == 1:
	    self.active_tuile.pose(self.screen,x,y)
	  if event.button == 3:
	    self.active_tuile.couvre(self.screen)	  
	except :
	  pass

      if event.type==KEYUP and event.key == K_F1:
	self.mon_aide.general()
      if event.type==KEYUP and event.key == K_F2:
	self.interaction.taille(self.config)

      if event.type==KEYUP and (event.key == K_F7 or (event.key==K_s and pygame.key.get_mods()==4160)):#left ctrl
	self.load_save.save(self.config,self.mapping)
      if event.type==KEYUP and (event.key == K_F8 or (event.key==K_o and pygame.key.get_mods()==4160)):#left ctrl
	fichier=self.open_file()

  def game(self):
    while True:
      self.input(pygame.event.get())
      pygame.time.wait(100)
      
		
if __name__ == '__main__':
	map()

