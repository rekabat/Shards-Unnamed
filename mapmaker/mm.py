import pygame as pg
from pygame.locals import *

import multiprocessing as mp

def runGame():
	# print "in rungame", GI
	# GI = src.gameinterface.GameInterface('play')

	send_pipe, recv_pipe = mp.Pipe()

	d = mp.Process(target = dispatching, args = (recv_pipe,))
	r = mp.Process(target = rendering, args = (recv_pipe,))



	d.start()
	r.start()
	send_pipe.send([GI])
	# d.join()

	# r.send([GI])
	# r.join()

def dispatching(pipe):
	# print "in dispatching", GI
	GI = pipe.recv()

	clock = pg.time.Clock()
	
	froze = False

	while 1:
		dt = clock.tick(g.FRAME_RATE)
		if froze:
			dt = 1./g.FRAME_RATE

		events = pg.event.get()

		trash0, froze = GI.dispatch(events, dt/1000.)


def rendering(pipe):
	# print "in rendering", GI
	GI = pipe.recv()

	clock = pg.time.Clock()

	while 1:
		dt = clock.tick(g.FRAME_RATE)
		GI.renderView()


# def dispatching():
#     clock = pg.time.Clock()
#     while 1:
#         dt = clock.tick(.55)
#         print "hi"

# def rendering():
#     clock = pg.time.Clock()
#     while 1:
#         dt = clock.tick(.6)
#         print "hello"

pg.init()
pg.display.init()

def runGame():
	ts = pg.display.set_mode((32,32))
	mp = pg.display.set_mode((32,32))

	clock = pg.time.Clock()

	while True:
		clock.tick(30)

		for evt in pg.event.get():
			if evt.type == pg.KEYDOWN:
				key = evt.dict['key']

				if key == pg.K_RETURN:
					pass

				elif key == pg.K_TAB:
					pass
				
				elif key == pg.K_ESCAPE:
					pass

if __name__ == '__main__': runGame()