import pygame as pg
import time

def getDict(pos, evtList):
	retDict = {'on': pos}
	for i, line in enumerate(evtList):
		if line.startswith("> "):
			retDict['extra'] = evtList[i:]
			break
		else:
			k, v = line.split(": ")
			retDict[k.lower()] = v
	
	# blocked as bool
	retDict['blocked'] = bool(int(retDict['blocked']))

	# event_id as int
	retDict['event_id'] = int(retDict['event_id'])

	# one_time as bool
	retDict['one_time'] = bool(int(retDict['one_time']))

	# art as string, none if no art exists for event
	retDict['art'] = retDict['art'].replace("'", "")
	if len(retDict['art']) == 0:
		retDict['art'] = None
	
	# art tile as tile coords (tuple)
	retDict['art_tile'] = tuple([int(i) for i in retDict['art_tile'].split(":")])

	return retDict

def parse(evtfile):
	eventDict = {}
	file = [line.strip() for line in open(evtfile, 'r').readlines()]

	temp = []
	for line in file:
		if not line.startswith(">>>"):
			temp.append(line)
		else:
			pos = temp.pop(0).split(" ")[1]
			pos = tuple([int(i) for i in pos.split(":")])
			
			if pos not in eventDict.keys():
				eventDict[pos] = []
			eventDict[pos].append(WorldEvent(**getDict(pos, temp)))
			
			temp = []
	
	return eventDict

class WorldEvent:
	def __init__(self, on, blocked, event_id, one_time, art, art_tile, extra):
		self.on = on
		self.blocked = blocked
		self.event_id = event_id
		self.one_time = one_time
		self.art = art
		self.art_tile = art_tile
		self.extra = extra

	def execute(self):
		return EVENT_IDS[self.event_id](self.extra)
	
	def imageInfo(self):
		return self.art, self.art_tile


import text
def twoWayDialog(extra):
	print 'success'
	new = text.Text("SUCCESS", 50)
	new.place(pg.display.get_surface(), (0,0), center=False)
	pg.display.flip()
	time.sleep(1)
	

EVENT_IDS = { 1: twoWayDialog } #,
	  # 2: PickUpItem,
	  # 3: DeathByBurning }
