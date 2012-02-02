import random as rand

# def itemParser(filename):
# 	lines = open(filename, "r").readlines()
# 	lines = [l[:-1] for l in lines] #removes newline chars

# 	print lines



def genRandItem(type, level):
	if type == "Weapon":
		return genRandWeapon(level)
	else:
		print "no gen method for "+type+"type item."

class Item:
	def __init__(self, name, type, value):
		self.name = name
		self.type = type
		self.value = value
	
	def getType(self):
		return self.type


def genRandWeapon(self):
	power = rand.random()*level
	speed = rand.random()*level
	value = rand.random()*level
	return Weapon(power, speed, "random", "weapon", rand.random()*level)

class Weapon(Item):
	def __init__(self, power, speed, **kwargs):
		Item.__init__(self, **kwargs)

		self.subtype = ""
		self.power = 0
		self.speed = 0
