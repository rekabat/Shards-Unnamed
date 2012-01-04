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
            eventDict[pos] = temp[:]
            temp = []

    return eventDict

def logEvent(id, text):
    return EVENT_IDS[id](parseText(text))

class WorldEvent:
    def __init__(self, img=[]):
        self.img = img

class TwoWayDialog(WorldEvent):
    def __init__(self, text):
        pass

# EVENT_IDS = { 1: TwoWayDialog,
#               2: PickUpItem,
#               3: DeathByBurning }
