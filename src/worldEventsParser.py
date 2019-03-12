def getDict(evtList):
    rDict = {}
    for i, line in enumerate(evtList):
        if line.startswith("> "):
            rDict['extra'] = evtList[i:]
            break
        else:
            k, v = line.split(": ")
            rDict[k.lower()] = v

    # art as string, none if no art exists for event
    rDict['art'] = rDict['art'].replace("'", "")
    if len(rDict['art']) == 0:
        rDict['art'] = None

    # art tile as tile coords (tuple)
    rDict['art_tile'] = rDict['art_tile'].replace("'", "")
    if rDict['art_tile'] == "":
        rDict['art_tile'] = None
    else:
        rDict['art_tile'] = tuple([int(i) for i in rDict['art_tile'].split(":")])

    # on as a list of tuples
    rDict['on'] = tuple([int(i) for i in rDict['on'].split(':')])

    # z as int
    rDict['z'] = int(rDict['z'])

    # blocked as bool
    rDict['blocked'] = bool(int(rDict['blocked']))

    # enter as bool
    rDict['enter'] = bool(int(rDict['enter']))

    # one_time as bool
    rDict['one_time'] = bool(int(rDict['one_time']))

    # locked as bool
    rDict['locked'] = bool(int(rDict['locked']))

    # immediate as bool
    rDict['immediate'] = bool(int(rDict['immediate']))

    # # on as a list of tuples
    # rDict['on'] = rDict['on'].split(', ')
    # rDict['on'] = [tuple([int(i) for i in each.split(':')]) for each in rDict['on']]

    # ret = []
    # for each in rDict['on']:
    #     ret.append(dc(rDict))
    #     ret[-1]['on'] = each

    # return ret

    return rDict


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

    event = []
    chain = []
    chainList = []
    for listOfStringsOfChain in eventChains:
        for line in listOfStringsOfChain:
            if not line.startswith("}}}"):
                event.append(line)
            else:
                chain.append(event)
                event = []
        chainList.append(chain)
        chain = []

    eventList = []
    for chain in chainList:
        j = 0
        for event in chain:
            ret = getDict(event)

            # for r in ret:
            #     eventObj = EVENT_IDS[r['event_id']]

            #     if j == 0:
            #         eventList.append(eventObj(**r))
            #     else:
            #         eventList[-1].setDeepest(eventObj(**r))
            #     j+=1
            eventObj = EVENT_IDS[ret['event_id']]

            if j == 0:
                eventList.append(eventObj(**ret))
            else:
                eventList[-1].setDeepest(eventObj(**ret))
            j += 1

    return eventList
