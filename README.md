# InfiniteBounce
A simple game in python where you clear obstacles for the main ball to bounce off the walls infinitely.

# What is this game?!
There is a red ball and a blue ball in the game. The red ball is only one in number and automatcally moves and bounces off the boundary walls. The blue balls are randomly generated and placed on screen. 
The objective of the player is to move the blue balls on the screen to make way for the red ball.
If the red ball collides with the blue ball, the game is over.

# Power-Ups
There are two power-ups in the game. The cooldown time for both the power-ups is 20 seconds.
  1) SlowMo:      This power-up slows down the red ball for 10 seconds.
  2) The Merger:  This power-up pairs up all the blue balls present on screen. This also increases the size of the blue balls.
  
# Running the game
Download all files and place it in the same folder. Run using any python IDE. You must have pygame installed on your system on top of python 3.6 or higher.

# Bugs
1) I've never actually went that far into the game to encounter this bug. When you use the merger power-up for a number of times, the blue balls grow bigger and bigger resulting in a collision between the red ball and the player can't do anything to prevent that. Also, it hits the wall which results in a game over.

2) Sometimes, the game instantiates both the red and blue balls on the same spot resulting in a game over right off the bat.
