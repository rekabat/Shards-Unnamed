from src.general import Utils as g

class Tile:
    def __init__(self, img, blocked, pos_on_map, z):
        self.img = img
        self.Blocked = blocked
        self.rect = g.tile2rect(pos_on_map)
        self.z = z

    def getImg(self): return self.img

    def blocked(self): return self.Blocked

    def getRect(self): return self.rect

    def getZ(self): return self.z
