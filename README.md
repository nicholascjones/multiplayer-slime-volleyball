A multiplayer implementation of the popular online game Slime Volleyball, using the PyGame and Twisted libraries

- Do not use the clock manager in Pygame:
- def gameloopiterate():
	ticks += 1
	# ... rest of game loop
	# use ticks to count instead of clock

lc = LoopingCall(gameloopiterate)
lc.start(1.0/60)
reactor.run()
lc.stop()



Sources:

- pygame.org -- used for general documentation knowledge surrounding library
- piskelapp.com -- used to create sprites
- CITE ORIGINAL SLIME VOLLEYBALL AS INSPIRATION
