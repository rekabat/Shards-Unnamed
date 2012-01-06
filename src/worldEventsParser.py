import pygame as pg
from pygame.locals import *

from mapParser import tileRect

TILE_RES = (32, 32)
TRANSPARENT = (199,200,201)

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

def parse(evtfile, EVENT_IDS):
    eventDict = {}
    file = [line.strip() for line in open(evtfile, 'r').readlines()]
    
    eventChains = []
    chain = []
    for line in file:
        if not line.startswith(">>>"):
            chain.append(line)
        else:
            eventChains.append(chain)
            chain = []

    event=[]
    chain=[]
    chainList=[]
    for listOfStringsOfChain in eventChains:
        for line in listOfStringsOfChain:
            if not line.startswith("}}}"):
                event.append(line)
            else:
                chain.append(event)
                event=[]
        chainList.append(chain)
        chain = []
    
    eventList = []
    for chain in chainList:
        j = 0
        for event in chain:
            pos = event.pop(0).split(" ")[1]
            pos = tuple([int(i) for i in pos.split(":")])
            
            ret = getDict(pos, event)
            eventObj = EVENT_IDS[ret['event_id']]
            
            if j == 0:
                eventList.append(eventObj(**ret))
            else:
                eventList[-1].setDeepest(eventObj(**ret))
            j+=1
    
    return eventList
