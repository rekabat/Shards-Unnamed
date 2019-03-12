import pygame as pg

TILE_RES = (32, 32)  # the width and hight of tiles in pixels
class Utils:
    # important constant
    TILE_RES = (32, 32)  # the width and hight of tiles in pixels
    # PX_STEP = 200 #pixels/second
    FRAME_RATE = 60  # Frames per second
    PF_REFRESH_RATE = 30  # how oftenpaths are found

    # easy references
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)

    @staticmethod
    def makeOutlinedArt(img, color):
        newArt = img.copy()
        # sets top to color
        for i in range(TILE_RES[0]):
            for j in range(TILE_RES[1]):
                if tuple(newArt.get_at((i, j)))[3] != 0:
                    newArt.set_at((i, j), color)
                    break
        # sets bottom to color
        for i in range(TILE_RES[0]):
            for j in range(TILE_RES[1])[::-1]:
                if tuple(newArt.get_at((i, j)))[3] != 0:
                    newArt.set_at((i, j), color)
                    break
        # sets left to color
        for j in range(TILE_RES[0]):
            for i in range(TILE_RES[1]):
                if tuple(newArt.get_at((i, j)))[3] != 0:
                    newArt.set_at((i, j), color)
                    break
        # sets right to color
        for j in range(TILE_RES[0]):
            for i in range(TILE_RES[1])[::-1]:
                if tuple(newArt.get_at((i, j)))[3] != 0:
                    newArt.set_at((i, j), color)
                    break
        return newArt

    @staticmethod
    def giveBorder(img, color, pixels: int):
        from itertools import chain
        for x in range(img.get_width()):
            for y in range(img.get_height()):
                if x in chain(range(pixels), range(img.get_width())[-pixels:]) or \
                        y in chain(range(pixels), range(img.get_height())[-pixels:]):
                    img.set_at((x, y), color)

    # useful functions

    # gets the rect given tile coordinates

    @staticmethod
    def tile2rect(x_y):
        return pg.Rect((x_y[0] * TILE_RES[0], x_y[1] * TILE_RES[1]), TILE_RES)

    @staticmethod
    def pix2tile(x_y):
        return int(x_y[0] / TILE_RES[0]), int(x_y[1] / TILE_RES[1])

    @staticmethod
    def tile2pix(x_y, center=True):  # center pixel
        if center:
            return int((x_y[0] + .5) * TILE_RES[0]), int((x_y[1] + .5) * TILE_RES[1])
        else:
            return int(x_y[0] * TILE_RES[0]), int(x_y[1] * TILE_RES[1])

    @staticmethod
    def pix2tile2rect(x_y):
        return Utils.tile2rect(Utils.pix2tile(x_y))

    @staticmethod
    def distance(point1, point2):
        return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** .5
