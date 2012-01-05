import pygame as pg
import time

import text

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
	if retDict['art_tile'] == "''":
		retDict['art_tile'] = None
	else:
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
			

			ret = getDict(pos,temp)
			eventObj = EVENT_IDS[ret['event_id']]
			eventDict[pos].append(eventObj(**ret))
			
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

	def imageInfo(self):
		return self.art, self.art_tile
		

class TwoWayDialog(WorldEvent):
	def __init__(self, **kwargs):
		WorldEvent.__init__(self, **kwargs)
	
	def execute(self, GI):
		print 'success', self
		new = text.Text("SUCCESS", 50)
		new.place(pg.display.get_surface(), (0,0), center=False)
		# pg.display.flip()
		time.sleep(1)
		GI.map.setup[self.on].removeEvent()


EVENT_IDS = { 1: TwoWayDialog } #,
	  # 2: PickUpItem,
	  # 3: DeathByBurning }
