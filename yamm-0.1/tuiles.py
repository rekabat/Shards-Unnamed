# -*- coding: utf-8 -*-

from pygame.locals import *
import pygame.rect


class active_tiles (pygame.sprite.Sprite):
  """the tiles to be drowned on the map"""
  def __init__(self,config,mapping,start=1):
    self.config=config
    self.mapping=mapping
    if start==1:
      self.tuile=self.config.config['tile_image'].subsurface(self.config.config['active_tile_tiles_x'],self.config.config['active_tile_tiles_y'],self.config.config['size_tile_x'],self.config.config['size_tile_y'])
      self.rect=self.tuile.get_rect()
      self.rect.topleft=[self.config.config['margin'],self.config.config['margin']]

  def affiche(self,screen):
    """blit the choosen tile on the screen"""
    screen.blit(self.tuile,self.rect)
    pygame.display.update(self.rect)

  def pose(self,screen,x,y,update=1):
    """draw on the map the choosen tile"""
    self.rect.topleft=[x*self.config.config['size_tile_x']+self.config.config['map_pos_x'],y*self.config.config['size_tile_y']+self.config.config['map_pos_y']]
    screen.blit(self.tuile,self.rect)
    if update==1:
      pygame.display.update(self.rect)
      self.mapping['-'.join([str(x),str(y)])]=','.join([str(self.config.config['active_tile_x']),str(self.config.config['active_tile_y'])])

  def couvre(self,screen):
    """cover the all map we drawn with the tile in use"""
    for i in range (0, self.config.config['size_map_x']):
      for j in range (0, self.config.config['size_map_y']):
	self.rect.topleft=[i*self.config.config['size_tile_x']+self.config.config['map_pos_x'],j*self.config.config['size_tile_y']+self.config.config['map_pos_y']]
	screen.blit(self.tuile,self.rect)
	self.mapping['-'.join([str(i),str(j)])]=','.join([str(self.config.config['active_tile_x']),str(self.config.config['active_tile_y'])])
    pygame.display.update(self.config.get_map_rect())

  def reload_save_map(self,screen):
    """reloading the saved map"""
    static_tile=''
    tiles=self.mapping.items()
    tiles.sort(key=lambda x: x[1])
    for tile in tiles:
      mp=tile[0].split("-")
      tn=tile[1].split(",")
      if tile[1]!=static_tile:
	static_tile=tile[1]
	self.config.set_active_tile(int(tn[0]),int(tn[1]))
	self.tuile=self.config.config['tile_image'].subsurface(int(self.config.config['active_tile_tiles_x']),int(self.config.config['active_tile_tiles_y']),int(self.config.config['size_tile_x']),int(self.config.config['size_tile_y']))
	self.rect=self.tuile.get_rect()
      self.pose(screen,int(mp[0]),int(mp[1]),0)
      pygame.display.update(self.config.get_map_rect())

    


class tuiles(pygame.sprite.Sprite):
  """ the tile set we are using """
  def __init__(self,config):
    pygame.sprite.Sprite.__init__(self)
    self.config=config
    self.config.config['tile_image'] = pygame.image.load(self.config.config['tiles_file'].encode('utf-8'))
    self.rect=self.config.config['tile_image'].get_rect()
    self.rect.topleft=[self.config.config['margin'],2*self.config.config['margin']+self.config.config['size_tile_y']]
    self.config.config['tiles_file_size_x']=self.config.config['tile_image'].get_size()[0]
    self.config.config['tiles_file_size_y']=self.config.config['tile_image'].get_size()[1]
    self.pos_x=self.config.config['margin']
    self.pos_y=2*self.config.config['margin']+self.config.config['size_tile_y']



  def get_click(self,x,y,screen):
    """did we click on the tileset, return tne 'name' of the tile, for exemple 0,0 for the first one"""

    if self.rect.collidepoint(x,y):
      nbr_x= int((x-self.pos_x)/self.config.config['size_tile_x'])
      nbr_y= int((y-self.pos_y)/self.config.config['size_tile_y'])
      self.config.set_active_tile(nbr_x,nbr_y)
      return True

  def grid(self,image):
    """ draw a grid on the tileset to easy see the differents tiles"""
    x=0
    y=0
    while (x <= self.config.config['tiles_file_size_x']):
      pygame.draw.line(image,(255,255,255),(x,0),(x,self.config.config['tiles_file_size_y']),1)
      x+=self.config.config['size_tile_x']
    while (y <= self.config.config['tiles_file_size_y']):
      pygame.draw.line(image,(255,255,255),(0,y),(self.config.config['tiles_file_size_x'],y),1)
      y+=self.config.config['size_tile_y']

  def affiche(self,screen):
    """blit the tileset on the screen"""
    if self.config.config['tile_image'] != None:
      self.grid(self.config.config['tile_image'])
      screen.blit(self.config.config['tile_image'],self.rect)

  



class map_draw(pygame.sprite.Sprite):
  """ the map we are drawing on the screen """

  def __init__(self,config,tuiles):
    pygame.sprite.Sprite.__init__(self)
    self.config=config

    self.config.config['map_size_x']=self.config.config['size_map_x']*self.config.config['size_tile_x']
    self.config.config['map_size_y']=self.config.config['size_map_y']*self.config.config['size_tile_y']
    self.config.config['map_pos_x']=(2*self.config.config['margin'])+self.config.config['tiles_file_size_x']
    self.config.config['map_pos_y']=2*self.config.config['margin']+self.config.config['size_tile_y']

    self.image = pygame.Surface([self.config.config['map_size_x'],self.config.config['map_size_y']])
    self.rect=self.image.get_rect()
    self.rect.topleft=[self.config.config['map_pos_x'],self.config.config['map_pos_y']]

  def get_click(self,x,y,screen):
    """did we click on the map we are drawing, return tne 'position', for exemple 0,0 for the first position top_left"""
    if self.rect.collidepoint(x,y):
      nbr_x= int((x-self.config.config['map_pos_x'])/self.config.config['size_tile_x'])
      nbr_y= int((y-self.config.config['map_pos_y'])/self.config.config['size_tile_y'])
      return(nbr_x,nbr_y)

  def grid(self,screen):
    """ draw a grid on the map we draw to easy see the different positions"""
    x=0
    y=0
    while (x <= self.config.config['map_size_x']):
      pygame.draw.line(screen,(255,255,255),(x,0),(x,self.config.config['map_size_y']),1)
      x+=self.config.config['size_tile_x']
    while (y <= self.config.config['map_size_y']):
      pygame.draw.line(screen,(255,255,255),(0,y),(self.config.config['map_size_x'],y),1)
      y+=self.config.config['size_tile_y']

  def affiche(self,screen):
    """ draw on the map the tile in use at its choosen position"""
    self.grid(self.image)
    screen.blit(self.image,self.rect)
