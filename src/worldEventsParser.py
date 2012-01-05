import pygame as pg
from pygame.locals import *

from worldEvents import EVENT_IDS

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
