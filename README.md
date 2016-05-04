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

Testing was done on several computers, including Fitz77, both personal computers, and using ssh over student03 between Brian and Nick's computers. I would not recommend playing over ssh, as it can tend to have a fair amount of lag.

Final side note: game.py is sparcely commented as all major commenting was put into server.py and client.py.

Sources:

- pygame.org -- used for general documentation knowledge surrounding library
- piskelapp.com -- used to create sprites
- CITE ORIGINAL SLIME VOLLEYBALL AS INSPIRATION
- Twisted documentation

