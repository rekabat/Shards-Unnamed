# currently, while pathfinding, enemies are ignored and then collisions are handled as they happen
# it seems to run too slowly if I detect collisions while pathfinding.
# I may want to change it back wants I can do multiprocessing so it's more robust


import pygame as pg

from .general import Utils as g
from .moveables import Moveable
from .attacks import fireball


class Enemy(Moveable):
    def __init__(self, GI, position, z, size=(1, 1), img='art/playersprite.png', pixStep=.075):
        Moveable.__init__(self, position, z, size, img, pixStep)

        self.GI = GI
        self.targetTile = None
        self.currentTile = None
        self.currentPath = None
        self.player_changedTiles = 0

        self.aggroRange = 7  # tiles (width)
        self.aggro = False
        self.origin = self.rect.topleft

        self.alignment = 1
        self.spells = [fireball(alignment=self.alignment, user=self, GI=GI)]
        self.atkRate = 1500  # how many ms between attacks
        self.secondSinceAtk = 0

        self.stats = {'lvl': 0,
                      'hp': 5,
                      'def': 1,
                      'mag': 1,
                      'atk': 1}  # stats

        self.currentHP = 5

        # hp bar with a black border
        self.HPBar = pg.Surface((g.TILE_RES[0], int(g.TILE_RES[1] / 4.)))
        for x in range(g.TILE_RES[0]):
            for y in range(int(g.TILE_RES[1] / 4.)):
                if (x == 0) or (y == 0) or (x == g.TILE_RES[0] - 1) or (y == int(g.TILE_RES[1] / 4.) - 1):
                    self.HPBar.set_at((x, y), g.BLACK)
        self.updateHPBar()
        self.HPBarRect = None
        self.placeHPBar()

    def getAggro(self):
        return self.aggro

    def getAlignment(self):
        return self.alignment

    def getStat(self, stat):
        return self.stats[stat]

    def getCurrentHP(self):
        return self.currentHP

    def getHPBar(self):
        return self.HPBar

    def getHPBarRect(self):
        return self.HPBarRect

    def useShards(self, amt):
        return True

    def tick(self, dt):
        # deal with spells
        for each in self.spells:
            each.tick(dt)

        self.currentTile = g.pix2tile(self.getRect().center)

        # if player is in aggro range, target player
        if g.distance(self.GI.player.getRect().center, self.getRect().center) < self.aggroRange * g.TILE_RES[0]:
            self.targetTile = g.pix2tile(self.GI.player.getRect().center)
            self.aggro = True
            toOrigin = False
        # if player is out of aggro, target origin
        else:
            self.targetTile = g.pix2tile(self.origin)
            self.aggro = False
            toOrigin = True

        # if the target has been reached, end movement
        if self.currentTile == self.targetTile:
            self.currentPath = None
            return False

        # if you're still targeting the same tile as before (what you found the path for), and a path is found...
        if (self.currentPath != None):
            # if self.currentPath[0] == self.currentTile:
            # 	del(self.currentPath[0])
            # 	if len(self.currentPath) == 0:
            # 		self.currentPath = None
            # 		return False
            try:
                i = self.currentPath.index(self.currentTile)
                del (self.currentPath[:i + 1])
                if len(self.currentPath) == 0:
                    self.currentPath = None
                    return False
            except:
                pass

            # the coords you're heading to this tick
            xp, yp = g.tile2pix(self.currentPath[0], center=True)
            # the coords you're on now
            xs, ys = self.getRect().center

            # #the coords you're heading to this tick
            # xp, yp = self.currentPath[0]
            # #the coords you're on now
            # xs, ys = self.currentTile

            mv = ""

            if xp - xs < 0:
                mv += "L"
            elif xp - xs > 0:
                mv += "R"

            if yp - ys < 0:
                mv += "U"
            elif yp - ys > 0:
                mv += "D"

            self.forgetMovement()
            for m in mv:
                self.movingDirection(m)

            if len(mv) == 2:
                mv = [mv, mv[0], mv[1]]
            else:
                mv = [mv]
            for each in mv:
                self.move(each, dt, forceTurn=g.tile2pix(self.targetTile))

                # Check if the movement is valid by making a smaller rectangle and seeing
                smallerRect = pg.Rect((0, 0), (self.getRect().width * .87, self.getRect().height * .87))
                smallerRect.center = self.getRect().center

                if self.GI.collisionWithBlockedRect(smallerRect, self.getZ(), player=True, ignoreEnemy=self):
                    self.undoMove()
                else:
                    break

            # self.currentPath[0] = g.pix2tile(self.getRect().center)

            self.placeHPBar()

        if (self.currentPath == None) or (self.targetTile != self.currentPath[-1]):
            if toOrigin:
                t0 = None
            else:
                t0 = 1.5 * self.aggroRange

            path = self.GI.findPath_from_to(self, (self.currentTile[0], self.currentTile[1], self.z),
                                            (self.targetTile[0], self.targetTile[1], self.z), limit=t0)

            if path:
                self.currentPath = path

                # it could be that pathfinding took long enough that the enemy has left the tile he initially requested the path from
                if not (self.currentTile in self.currentPath):
                    # assume only one tile has passed
                    self.currentPath = self.currentPath[1:]

        # touching the player
        # only casts the first spell on the enemy's list!!!!!!!!
        # the coords you're heading to this tick
        xp, yp = g.pix2tile(self.GI.player.getRect().center)
        # the coords you're on now
        xs, ys = self.currentTile
        x = abs(xp - xs)
        y = abs(yp - ys)
        if (self.aggro) and (x == 0 or y == 0) and (x < self.spells[0].distance or y < self.spells[0].distance):
            return self.spells[0].cast(self.getRect(), self.facing)
        else:
            return False

    # return False

    def takeHP(self, amt):
        self.currentHP -= amt
        if self.currentHP <= 0:
            return True
        self.updateHPBar()
        return False

    def updateHPBar(self):
        x = self.HPBar.get_width() - 2
        y = self.HPBar.get_height() - 2

        self.HPBar.subsurface(pg.Rect((1, 1), (x, y))).fill(g.WHITE)

        portion = float(self.currentHP) / self.getStat('hp')

        x *= portion

        self.HPBar.subsurface((1, 1), (x, y)).fill(g.RED)

    def placeHPBar(self):
        self.HPBarRect = pg.Rect((self.getRect().left, self.getRect().top - self.HPBar.get_height()),
                                 self.HPBar.get_size())
