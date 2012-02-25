import pygame as pg
from pygame.locals import *

import general as g

def getDict(evtList):
    retDict = {}
    for i, line in enumerate(evtList):
        if line.startswith("> "):
            retDict['extra'] = evtList[i:]
            break
        else:
            k, v = line.split(": ")
            retDict[k.lower()] = v

    # art as string, none if no art exists for event
    retDict['art'] = retDict['art'].replace("'", "")
    if len(retDict['art']) == 0:
        retDict['art'] = None
    
    # art tile as tile coords (tuple)
    retDict['art_tile'] = retDict['art_tile'].replace("'", "")
    if retDict['art_tile'] == "":
        retDict['art_tile'] = None
    else:
        retDict['art_tile'] = tuple([int(i) for i in retDict['art_tile'].split(":")])
    
    # on as tuple
    retDict['on'] = tuple([int(i) for i in retDict['on'].split(':')])

    # z as int
    retDict['z'] = int(retDict['z'])

    # blocked as bool
    retDict['blocked'] = bool(int(retDict['blocked']))

    # enter as bool
    retDict['enter'] = bool(int(retDict['enter']))

    # one_time as bool
    retDict['one_time'] = bool(int(retDict['one_time']))

    # locked as bool
    retDict['locked'] = bool(int(retDict['locked']))

    # immediate as bool
    retDict['immediate'] = bool(int(retDict['immediate']))

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
            ret = getDict(event)
            eventObj = EVENT_IDS[ret['event_id']]
            
            if j == 0:
                eventList.append(eventObj(**ret))
            else:
                eventList[-1].setDeepest(eventObj(**ret))
            j+=1
    
    return eventList
