Names: Min Junyi and Kellen Dorchen

Point of Project:  To make a 2-D game of a Jaywalker trying to cross roads. Like the “Frogger” arcade game

Class hierarchy:

Super Class: Has common methods that most classes will have to use. It has init method that provides image and surface. Also contains getWidth, getHeight, getPosition, setPosition, draw, getSpeed and setSpeed methods.
	Vehicle Class: Contains the methods that allow the classes below to move and check for collisions with Jay. All vehicles will move from the top of the screen to the bottom, once reaching the bottom, it will reposition back at the top.
		Car Class: When car CRASHES into Jay, Jay dies. (looks like a car in-game)
		Bike Class: When bike CRASHES into Jay for the first time, Jay loses some legs. When it crashes into Jay again, Jay loses all legs. The third collision causes the death of Jay. (looks like turtle in-game)
		Ambulance Class: If Jay is injured, the ambulance CRASHING into Jay heals him, and Jay regains back his legs. If Jay is not injured and gets hit by the ambulance, nothing happens. (looks like a muppet in-game)
	Jay Class:Jay moves up, left, down and right with W-A-S-D keys respectively. (looks like a cat in-game)

Invisible Class:This is interesting. Its methods are essentially gibberish. You can still call methods through it like "Invisible.draw", "Invisible.move", "Invisible.getPosition", but nothing important happens. It functions as an empty replacement object. When we don't want an object(maybe an ambulance or a bike) anymore, but still need to call its methods, we replace that object with the Invisible class object.

How to Use Your Program, Including Major Features:
Have fun, try to cross the roads with W-A-S-D without getting killed. 
Every time Jay crosses the street (all the lanes), and enters the green pavement on the opposite side of the street, the score counter increases by one. The user can then keep crossing the roads, to try to get a high score.
Every time Jay crosses the street, he looks at the other direction, hinting to the user to keep crossing the street (the grass is always greener on the other side).
If you get hit by a bike, you can get hit by an ambulance and recover. 
When you get hit by a bike once, you lose speed (limping), when you get hit again, you lose more speed(crawling/wiggling). Speed is also regained by colliding into an ambulance.
You can press "r" to restart the game. 
Most lanes' vehicles are spawning at random times, and are moving at random speeds.
It includes an extremely helpful tutorial poem on the top right of the play screen.

Which Features do NOT Work:
N/A to us

Which Aspects of Your Project were Most Challenging:
1) Trying to space out the vehicles in each lane, so that they don't start clumped up together. We used time delay to separate the vehicles. The first vehicle goes off at time(t) = 0, the others go off at respective t times.

2) Coming up with the Invisible Class. While trying to make the vehicles disappear, and then spawn, we came up with the idea of having an Invisible Class. When the vehicles touch the bottom of the screen, an Invisible class object (we called it 'ghost') replaces the vehicle objects, so that the main while loop can still run without barfing out errors. The while loop will still call for methods in the ghost object, but nothing happens.

3) Trying to make the vehicles spawn at random times. When a vehicle touches the bottom of the screen, a variable for that specific vehicle, mainly called StartTime, records the time that that happens, and a random delay time is added to the StartTime. When the in-game time is equal to the StartTime of the vehicle, then the ghost is replaced by the corresponding vehicle, and the vehicle starts moving down from the top of the screen again.

4) Recording how many times the bike has hit Jay. At first, we gave Jay a period of invulnerability after he got hit by a bike. However, if two bikes were to hit Jay consecutively, the program will not record 2 hits but just 1. It was decided that this was not the way to go, because getting run over by 2 bikes definitely hurts more than getting run over by 1. We counted the number of "collisions" by counting the number of times the bike is within the x-y coordinates of Jay. But due to the firing of the while loops, the collision test constantly detects "collisions" while the bike travels through Jay.  Through experimentation, it was found that when 1 entire bike passes through Jay, the collision count was consistently shown to be 12. Therefore, we proposed that when the collision count is >0 but <=12, it injures Jay once, and when the collision count is >12 and <=24, it injures Jay the second time. When the collision count is >24, Jay dies.
We understand that if we briefly touch the bike (don't let the entire bike pass through Jay), it may not injure Jay. But that makes sense realistically, because it can be seen as being grazed by a bike, and not entirely getting hit by it.

5) How to change the direction that Jay is facing when he reaches the other side of the street. It was solved by using a list of the states the Jay can be in (healthy, injured, badly injured). The states are just Jay objects with different pictures. We then replaced the objects in the list with objects that have pictures of Jay looking at the left. Now, even when an injured Jay crosses successfully to the other side, he turns around, and is still injured. It maintains the state that Jay was in before Jay arrives to the end of the street.

6) How to record the score. At first we thought that just by having Jay's x-coordinates equal the x-coordinates of the safe pavement, it increases the score. However, due to the while loop constantly repeating, the score keeps increasing whenever Jay is in that safe pavement. Then we came up with the idea of having a variable destinationCat = "right". So only when Jay is traveling to the right (destination == right), and Jay has reached the street on the right, will the score increase by 1, then we change the destination of Jay, destinationCat = "left", so that it stops the score increment. And Jay can then proceed to the street on the left to score more points. 

7) How to restart the game. We came up with the idea of having 3 while loops:
while True:
	a = True
	b = True
	while a:
	while b: 
with 2 while loops (while a, while b) nested within the first while loop. The first while loop just sets up all the objects and makes the game ready to run. The second while loop runs the game. (most things are happening within this while loop, this is like the in-game while loop) The third while loop shows the message that Jay has died and hints to the user to press R. 

When the user has died, we will change a to a = False. It breaks the second while loop and goes into the third while loop. Then in the third while loop when the user presses r, it changes b to b = False, ending the third while loop, and looping back into the first while loop. The first while loop resets the game's elements and resets a and b to be True, thus going back into the second while loop again, keeping the game running.
Furthermore, if the user presses "r" while Jay is not dead, it restarts the game, by making a = False, b = False, and going to the first while loop that resets all the elements of the game.

8) Condensing the code down for efficiency. We had 1000 lines of code at first, and condensed it to around 600 lines of code. The problem is that, each lane of vehicles are doing something very different from the other lanes. For example, the first lane of cars does not set a random speed or time delay when it reaches the bottom of the screen. But other lanes do that. And the lanes get harder in difficulty, for example the time delay is shorter and the random speeds are faster. Therefore, each lane of cars/bikes have their own unique properties and cannot be condensed easily.

What we would add/future game-changing improvements:
Constant movements when a movement key is held down. 
Make diagonal movements when 2 movement keys (that don't cancel out) are pressed together.
Vehicles going in different directions (up and down the screen).
We would improve the efficiency of the code.
Add a high score indicator that remembers the name of the players and the highest 3 scores. 
Different character options for Jay (different image) and a character selection screen.
Possibly power ups, like invincibility or super speed.
Natural disasters occurring in-game (earthquakes splitting up lanes, tsunamis just flooding certain parts of the lanes, typhoons hurling cars to different lanes)
We can add different levels of difficulties, and have a menu page to select the difficulty along with all the options above.