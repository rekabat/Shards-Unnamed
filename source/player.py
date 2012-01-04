import pygame as pg
import mapParser

class Player:
	def __init__(self, map, position):
		self.name = "GenericFantasyHero"
		self.map = map
		self.position = position
		
		self.avatar = pg.image.load('art/player.png')
		
		self.place(self.map, self.position)
		
	def place(self, map, position):
		self.position = position
		
		self.m
		self