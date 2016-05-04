A multiplayer implementation of the popular online game Slime Volleyball, using the PyGame and Twisted libraries. The title indicates what type of game our project is: a goofy volleyball simulator with slimes instead of people. The concept mimics actual volleyball, with each player attempting to score a set number of points by hitting the ball into their opponent's ground, while preventing the ball from hitting the ground on their own side. The files included in this directory are:

	- ball.png
	- ceiling.png
	- greenslime.png
	- net.png
	- redslime.png
	- client.py
	- game.py
	- README.md (this file)
	- server.py

The game can be played one of two ways. To play a local game against a static opponent to better your skills, enter python game.py and use the arrow keys to control your red slime, with right arrow to move right, left arrow to move left, and up arrow to move up. Or, put your skills to the test, and play online mode! Run python server.py first, followed by two versions of python client.py. Online mode controls utilize 'a' for left, 'd' for right, and 'space' for jump. Simply follow any additional commands that are displayed on the screen, and have fun!

As for other features of the game, the physics and mechanics of our game are somewhat realistic, but slightly modified from reality to increase the quality of gameplay. Players can move sideways in the air mid-jump, and the walls and sides of the net add "bounce" to the ball, both of which are fun game changes. For all of the volleyball and tennis purists playing the game, however, grazing the ball off the top of the net will provide the perfect drop shot that you desire!

Upon finishing a game, players will have the option to either quit or play a second round of Slime Volleyball in CHALLENGE MODE! This mode includes a lowered ceiling, lower ball drop heights, and a higher net than the standard gameplay. This mode provides an exciting new arena (both literally and figuratively) for players to practice their volleyball precision.

A few disclaimers and tips for players are as follows:

	- As much fun as it can be to play in front of the net, inelastic collisions with 	the ball, net, and walls can cause the ball to behave eratically. Additionally,	  we have had issues with the ball going through the net, due to the sheer        	power of the slimes. As such, we recommend keeping hits singular.
	- The best way to generate power comes by using the walls and applying "spin",	  	which happens when one hits the ball while moving in a direction.
	- The development team highly recommends practicing first on the local game.py 	  	file against a static green enemy. He may not be able to move, but this makes 	  him surprisingly skilled. Additionally, this version of the game runs very well.
	- When playing across the network, lag sometimes prevents bounces from occurring  	properly. We promise that this comes from network latency, not our code :)

Testing was done on several computers, including Fitz77, both personal computers (Brian running an Ubuntu Virtual Machine on an HP Notebook and Nick using a MacBook), and using ssh over student03 between Brian and Nick's computers. We would not recommend playing over ssh, as it can tend to have a fair amount of lag.

Final side note: game.py is sparcely commented as this is not truly intended to be a part of our project submission (though it is fun to play). Primary comments are in server.py and client.py.

Sources:

- pygame.org -- used for general documentation knowledge surrounding library
- piskelapp.com -- used to create sprites
- https://cdn.rawgit.com/marler8997/SlimeJavascript/master/SlimeVolleyballLegacy.html 	-- an online iteration used as a rough sketch of our final project
- twistedmatrix.com -- used for general Twisted documentation and knowledge
- http://gamedev.stackexchange.com/questions/15708/how-can-i-implement-gravity
  -- some early help for ideas pertaining to our gravity and acceleration
- http://www.pygame.org/docs/ref/font.html
  -- learning to implement and display text within our game

