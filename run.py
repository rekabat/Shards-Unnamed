# Import pygame, locals, and initialize
import pygame as pg
from pygame.locals import *
import pygame._view #purely for py2exe

from multiprocessing import freeze_support #purely for py2exe

pg.init()

import src.general as g
import src.gameinterface



def runGame():
    clock = pg.time.Clock()

    GI = src.gameinterface.GameInterface('play')
    
    froze = False

    while True:
        dt = clock.tick(g.FRAME_RATE)
        if froze:
            dt = 1./g.FRAME_RATE

        events = pg.event.get()

        trash0, froze = GI.dispatch(events, dt)
        GI.renderView()


# import multiprocessing as mp

# GI = src.gameinterface.GameInterface('play')
# # print "outside", GI

# def runGame():
#     # print "in rungame", GI
#     # GI = src.gameinterface.GameInterface('play')

#     send_pipe, recv_pipe = mp.Pipe()

#     d = mp.Process(target = dispatching, args = (recv_pipe,))
#     r = mp.Process(target = rendering, args = (recv_pipe,))



#     d.start()
#     r.start()
#     send_pipe.send([GI])
#     # d.join()

#     # r.send([GI])
#     # r.join()

# def dispatching(pipe):
#     # print "in dispatching", GI
#     GI = pipe.recv()

#     clock = pg.time.Clock()
    
#     froze = False

#     while 1:
#         dt = clock.tick(g.FRAME_RATE)
#         if froze:
#             dt = 1./g.FRAME_RATE

#         events = pg.event.get()

#         trash0, froze = GI.dispatch(events, dt/1000.)


# def rendering(pipe):
#     # print "in rendering", GI
#     GI = pipe.recv()

#     clock = pg.time.Clock()

#     while 1:
#         dt = clock.tick(g.FRAME_RATE)
#         GI.renderView()


# # def dispatching():
# #     clock = pg.time.Clock()
# #     while 1:
# #         dt = clock.tick(.55)
# #         print "hi"

# # def rendering():
# #     clock = pg.time.Clock()
# #     while 1:
# #         dt = clock.tick(.6)
# #         print "hello"

if __name__ == '__main__':
    freeze_support() #purely for py2exe
    runGame()