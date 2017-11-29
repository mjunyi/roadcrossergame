#Project done by Min Junyi and Kellen Dorchen

import pygame, sys, time, random, math
from pygame.locals import*

pygame.init()

'''Defining my Classes'''

#Super class for most objects
class Super(object):
    def __init__(self, image, surface):
        self.image = image
        self.surface = surface
    
    def getWidth(self):
        return self.width
     
    def getHeight(self):
        return self.height
    
    def getPosition(self):
        return self.xy
        
    def setPosition(self, x, y):
        x = max(0, min(self.surface.get_width(),x))
        y = max(0, min(self.surface.get_height(),y))
        self.xy=[x,y]

    def draw(self):
        self.surface.blit(self.image, (self.xy[0], self.xy[1]))

    def getSpeed(self):
        return self.speed

    def setSpeed(self, speed):
        self.speed = speed

#Super Class for vehicles: cars, bikes, ambulances
class Vehicle(Super):
    def __init__(self, image, surface):
        super().__init__(image, surface)
        
    def move(self, xy):
    #When the car reaches the bottom of the screen, reset position back to top of screen.
        xy = self.getPosition()
        xy[1] += self.getSpeed()
        if xy[1] >= 800:
            xy[1] = 0

    def collisionTest(self, xyTarget, targetWth, targetHgt):
    #When car touches the target, for example Jay, then it returns the boolean True.
        xy=self.getPosition()
        for i in range (targetWth+1):
            for j in range (targetHgt+1):
                if xy[0]<=xyTarget[0]+i<=xy[0]+self.getWidth() and xy[1]<=xyTarget[1]+j<=xy[1]+self.getHeight():
                    return True

class Car(Vehicle):
    def __init__(self, image, surface):
        self.width = 41
        self.height = 78
        self.setSpeed(4)
        super().__init__(image, surface)
                    
class Bike(Vehicle):
    def __init__(self, image, surface):
        self.width = 30
        self.height = 43
        self.setSpeed(7)
        super().__init__(image, surface)

class Ambulance(Vehicle):
    def __init__(self, image, surface):
        self.width = 55
        self.height = 69
        self.setSpeed(4)
        super().__init__(image, surface)

#Invisible objects that has methods that don't do anything important.
class Invisible(object):
    def __init__(self, surface):
        self.surface = surface
    
    def setPosition(self,x, y):
        self.nothing = 0
    
    def draw(self):
        self.nothing = 0
    
    def move(self, xy):
        self.nothing = 0
    
    def getPosition(self):
        return [0,0]
    
    def collisionTest(self, xyTarget, targetWth, targetHgt):
        self.nothing =0
        
#The Jaywalker's class
class Jay(Super):
    def __init__(self, image, surface):
        self.width = 63
        self.height = 40
        self.setSpeed(30)
        super().__init__(image, surface)
    
    def setWidth(self, width):
        self.width = width
    
    def setHeight(self, height):
        self.height = height

    def move(self, key):
        xy = self.getPosition()
        
        if key == "w":
            xy[1]-= self.getSpeed()
        elif key == "a":
            xy[0]-= self.getSpeed()
        elif key == "s":
            xy[1]+= self.getSpeed()
        elif key == "d":
            xy[0]+= self.getSpeed()
            
        #Teleporting code, helps in testing. Also helps in cheating. :)
        #Jumps to left grass patch
        elif key== "e":
            xy[0] = 1250
            xy[1] = 400
        #Jumps to right grass patch
        elif key == "q":
            xy[0] = 100
            xy[1] = 400
        #Jumps to middle - safe zone 
        elif key == "m":
            xy[0] = 718
            xy[1] = 400
        
        self.setPosition(xy[0], xy[1])
        
FPS=32
fpsClock = pygame.time.Clock()

while True:
    #Some colours we might use
    black = (0,0,0)
    white=(255,255,255)
    red = (255,0,0)
    green = (34,139,34)
    blue = (0,0,255)
    grey = (205,201,201)

    #Drawing Surface
    surface = pygame.display.set_mode((1400,800))
    pygame.display.set_caption('Jaywalker')

    #Words/Phrases/Sentences we might want to Print on Screen
    lossfont = pygame.font.Font(None,200)
    scorefont = pygame.font.Font(None, 50)
    helperfont = pygame.font.Font(None, 30)
    smallhelperfont =pygame.font.Font(None, 20)
    lossMsg = lossfont.render("YOU LOSE, PRESS R", True, red)
    scoreNumber = 0
    helperMsg = helperfont.render("Press R to restart", True, grey)
    helperMsg0 = smallhelperfont.render("Keep CAPSLOCK off", True, grey)
    helperMsg1 = helperfont.render("W-A-S-D to move", True, grey)
    helperMsg2 = helperfont.render("Cars kill,", True, grey)
    helperMsg3 = helperfont.render("Muppets heal,", True, grey)
    helperMsg4 = helperfont.render("and Turtles", True, grey)
    helperMsg5 = helperfont.render("make you squeal", True, red)
    
    '''Assigning Images to Characters'''
    carImage = pygame.image.load('car.png')
    jayImage = pygame.image.load('cat.png')
    jayLeftImage = pygame.image.load('leftcat.png')
    bikeImage = pygame.image.load('bike.png')
    jayInjuredImage = pygame.image.load('catinjured.png')
    jayLeftInjuredImage = pygame.image.load('leftcatinjured.png')
    jayInjuredBadlyImage = pygame.image.load('mouse.png')
    jayLeftInjuredBadlyImage = pygame.image.load('leftmouse.png')
    ambulanceImage = pygame.image.load('animal2.png')
    
    '''Making Objects - Jay states'''
    jayHealthy = Jay(jayImage, surface)
    jayHealthy.setPosition(50, 400)
    jayInjured1 = Jay(jayInjuredImage, surface)
    jayInjured2 = Jay(jayInjuredBadlyImage, surface)
    jayLeftHealthy = Jay(jayLeftImage,surface)
    jayLeftInjured1 = Jay(jayLeftInjuredImage, surface)
    jayLeftInjured2 = Jay(jayLeftInjuredBadlyImage, surface)
    
    jayStateList = [jayHealthy,jayInjured1,jayInjured2]
    jayList =[jayStateList[0]]
    
    '''Making Objects - Ambulance'''
    ambulanceStartList = [8,8,8,8,8]
    ambulanceList = []
    for i in range (5):
        ambulanceList+=[Ambulance(ambulanceImage, surface)]
    for i in range(5):
        ambulanceList[i].setPosition(300+200*i+25,0)
    
    '''Making Objects - Invisible'''
    ghost = Invisible(surface)
    
    '''Making Objects - Cars'''
    road1CarList=[]
    road2CarList=[]
    road3CarList=[]
    road4CarList=[]
    road5CarList=[]
    roadCarList = [road1CarList, road2CarList, road3CarList, road4CarList, road5CarList]
    
    #Road 1,2,3 Cars (has 4 cars in their lanes)
    for i in range(3):
        for j in range(4):
            roadCarList[i]+=[Car(carImage, surface)]
            roadCarList[i][j].setPosition(225+200*i,0)
            if i == 2:
                roadCarList[i][j].setSpeed(random.randint(1,8))
    road1CarList[3].setSpeed(7)
    
    road2CarStartList = [5,5,5,5]
    road3CarStartList = [5,5,5,5]
    
    #Road 4,5 (has 5 Cars in their lanes)
    for i in range(3,5):
        for j in range(5):
            roadCarList[i]+=[Car(carImage, surface)]
            roadCarList[i][j].setPosition(225+200*i,0)
            if i == 4:
                roadCarList[i][j].setSpeed(random.randint(2,9))
            else:
                roadCarList[i][j].setSpeed(random.randint(3,10))
                
    road4CarStartList = [5,5,5,5,5]
    road5CarStartList = [5,5,5,5,5]
    roadCarStartList = [0,road2CarStartList,road3CarStartList,road4CarStartList,road5CarStartList]
    
    '''Making Objects - Bikes'''
    
    #Road 1 Bikes
    
    road1BikeList=[]
    road2BikeList=[]
    road4BikeList=[]
    road5BikeList=[]
    #All bikes come forth
    bikeList = [road1BikeList, road2BikeList, road4BikeList, road5BikeList]
    for i in range (3):
        road1BikeList+=[Bike(bikeImage, surface)]
        road1BikeList[i].setPosition(336,0)
    road1BikeStartList = [5,5,5]
    
    #Road 2 Bikes
    for i in range(4):
        road2BikeList+=[Bike(bikeImage,surface)]
        road2BikeList[i].setPosition(536,0)
        
    #Road 4,5 Bikes - Road 3 for bikes is a safe zone without bikes
    for i in range(2,4):
        for j in range(4):
            bikeList[i]+=[Bike(bikeImage, surface)]
            bikeList[i][j].setPosition(536+i*200,0)

    road2BikeStartList = [5,5,5,5]
    road4BikeStartList = [5,5,5,5]
    road5BikeStartList = [5,5,5,5]
    bikeStartList = [road1BikeStartList, road2BikeStartList, road4BikeStartList, road5BikeStartList]   
    
    #Bike Collision Tracker
    bikeHit = 0
    
    '''Other Misc Variables'''
    destinationCat = "right"
    
    starttime = time.clock()

    breakLoop1 = True
    breakLoop2 = True
    
    
    #Loop that runs when the game starts, this is the main loop that is running. Most things happening in-game are coded in this while loop.
    while breakLoop1:
        newtime = time.clock()
        '''DRAWING BEGINS - background car/bike lanes'''
        surface.fill(green)
        #Left Safezone
        pygame.draw.line(surface,red,(200,0),(200,800),2)
        #Right Safezone
        pygame.draw.line(surface,red,(1200,0),(1200,800),2)

        #Car Lanes
        #Road 1 Rightzone and White Stripes
        pygame.draw.rect(surface,black,(202,0,98,800))
        for i in range(0, 800, 100):
            pygame.draw.rect(surface,white, (240,i,23,80))
        
        #Road 2,3,4,5 Rightzone and White Stripes
        for i in range(400,1200,200):
            pygame.draw.rect(surface,black,(i,0,100,800))
            for j in range(0,800,100):
                pygame.draw.rect(surface,white,(i+40,j,23,80))

        #Bike Lanes 
        for i in range(300,1200,200):
            pygame.draw.rect(surface,grey,(i,0,100,800))
            for j in range(0,800,100):
                pygame.draw.rect(surface,white,(i+45,j,13,80))

        '''Useful Drawing Functions'''
        
        #moves and draws the given object
        def moveDraw(drawWhat):
            drawWhat.move(drawWhat.getPosition())
            drawWhat.draw()
            
        #ghostDelay moves the given object in 'what', and when the object reaches the bottom of the screen, the given object is changed to
        #(continued) a Invisible Class object named 'ghost'. Then the time at which the object is supposed to spawn again
        #(continued) is recorded. This time will be used to determine when the object spawns and moves once again from the top.
        #(continued) When the time to spawn has reached, the ve
        def ghostDelay(newObject, howmany, what, whatTime, randStart,randEnd, xPos, speedS, speedF):
            for i in range(howmany):
                if what[i].getPosition()[1]<795:
                    moveDraw(what[i])
                if what[i].getPosition()[1]>=795:
                    what[i]=ghost
                    whatTime[i] = time.clock()+random.randint(randStart,randEnd)
            for i in range(howmany):
                if whatTime[i]+0.1>=time.clock()>= whatTime[i]:
                    what[i] = newObject
                    what[i].setPosition(xPos, 0)
                    what[i].setSpeed(random.randint(speedS,speedF))
        
        '''Drawing and moving - Cars'''
        #Road1Cars    
        #r1c1
        moveDraw(roadCarList[0][0])
        #r1c2
        if newtime - starttime >= 1.5:
            moveDraw(roadCarList[0][1])
        #r1c3
        if newtime - starttime>= 3:
            moveDraw(roadCarList[0][2])
        #r1c4
        if newtime - starttime>= 5:
            moveDraw(roadCarList[0][3])
    
        #Road 2, 3, 4, 5 Cars
        
        if newtime - starttime<5:            
            #r2c1, r3c1, r4c1, r5c1
            for i in range(1,5):
                moveDraw(roadCarList[i][0])
            
            #r2c2, r3c2, r4c2, r5c2
            if newtime - starttime >= 1:
                for i in range(1,5):
                    moveDraw(roadCarList[i][1])
            
            #r2c3, r3c3, r4c3, r5c3
            if newtime - starttime>= 2:
                for i in range(1,5):
                    moveDraw(roadCarList[i][2])                
                
            #r2c4, r3c4, r4c4, r5c4
            if newtime - starttime>= 3:
                for i in range(1,5):
                    moveDraw(roadCarList[i][3])
                    
            #r4c5, r5c5
            if newtime - starttime>= 4:
                for i in range(3,5):
                    moveDraw(roadCarList[i][4])
        else: 
            #Road 2
            ghostDelay(Car(carImage, surface),4, roadCarList[1], roadCarStartList[1], 1,8, 425, 4, 4)
            #Road 3
            ghostDelay(Car(carImage, surface),4, roadCarList[2], roadCarStartList[2], 1,5, 625, 1, 7)
            #Road 4
            ghostDelay(Car(carImage, surface),5, roadCarList[3], roadCarStartList[3], 1, 5, 825, 2, 9)
            #Road 5
            ghostDelay(Car(carImage, surface),5, roadCarList[4], roadCarStartList[4], 1, 5, 1025, 3, 10)
    
        '''Drawing and Moving - BIKES'''
        #r1b1
        moveDraw(bikeList[0][0])
        
        #r1b2
        if newtime - starttime>= 1:
            moveDraw(bikeList[0][1])
        
        #r1b3
        if newtime - starttime>=2:
            moveDraw(bikeList[0][2])
            
        #Road 2,4,5 Bike
        if newtime - starttime<5:
            for i in range(1,4):
                moveDraw(bikeList[i][0])
            if newtime - starttime >= 1:
                for i in range(1,4):
                    moveDraw(bikeList[i][1])
            if newtime - starttime>= 2:
                for i in range(1,4):
                    moveDraw(bikeList[i][2])
            if newtime - starttime>= 3:
                for i in range(1,4):
                    moveDraw(bikeList[i][3])
                    
        else:            
            #Road 2 Bikes
            ghostDelay(Bike(bikeImage, surface),4, bikeList[1], bikeStartList[1], 1, 5, 536, 4, 9)
            #Road 4 Bikes
            ghostDelay(Bike(bikeImage, surface),4, bikeList[2], bikeStartList[2], 1, 5, 936, 5, 9)
            #Road 5 Bikes
            ghostDelay(Bike(bikeImage, surface),4, bikeList[3], bikeStartList[3], 1, 5, 1136, 6, 11)

        '''Drawing and Moving - AMBULANCES'''
        #All Ambulances
        for i in range (5):
            if ambulanceList[i].getPosition()[1]<790:
                ambulanceList[i].move(ambulanceList[i].getPosition())
                ambulanceList[i].draw()
            if ambulanceList[i].getPosition()[1]>=790:
                ambulanceList[i] = ghost
                ambulanceStartList[i] = time.clock() + random.randint(3,8)
        for i in range(5):
            if ambulanceStartList[i]+0.1>=time.clock()>= ambulanceStartList[i]:
                ambulanceList[i] = Ambulance(ambulanceImage, surface)
                ambulanceList[i].setPosition(325+i*200,0)
  
        key = None
    
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                key = event.unicode
                
        '''Drawing and Moving - JAY'''
        jayList[0].move(key)
        jayList[0].draw() 
        
        
        '''COLLISION TESTS'''
        #Collision Test for Cars
        for j in range(5):
            for i in range(4):
                if roadCarList[j][i].collisionTest(jayList[0].getPosition(), jayList[0].getWidth(), jayList[0].getHeight()):
                    breakLoop1=False

        #Collision Test for Bikes
        #For Road 1 Bikes
        if bikeHit < 12:
            for i in range(3):
                if road1BikeList[i].collisionTest(jayList[0].getPosition(), jayList[0].getWidth(), jayList[0].getHeight()):
                    tempxy = jayList[0].getPosition()
                    jayList[0]= jayStateList[1]
                    jayList[0].setPosition(tempxy[0],tempxy[1])
                    jayList[0].setSpeed(20)
                    bikeHit += 1
        elif bikeHit<24:
            for i in range(3):
                if road1BikeList[i].collisionTest(jayList[0].getPosition(), jayList[0].getWidth(), jayList[0].getHeight()):
                    tempxy = jayList[0].getPosition()
                    jayList[0]= jayStateList[2]
                    jayList[0].setPosition(tempxy[0],tempxy[1])
                    jayList[0].setSpeed(10)
                    bikeHit += 1
        else:
            for i in range(3):
                if road1BikeList[i].collisionTest(jayList[0].getPosition(), jayList[0].getWidth(), jayList[0].getHeight()):
                    breakLoop1=False
                    
        #For Road 2,4,5 Bikes (can't condense with the top because the top one the lane has 3 bikes, these lanes have 4 bikes.)
        
        if bikeHit < 12:
            for i in range(4):
                if road2BikeList[i].collisionTest(jayList[0].getPosition(), jayList[0].getWidth(), jayList[0].getHeight()) or road4BikeList[i].collisionTest(jayList[0].getPosition(), jayList[0].getWidth(), jayList[0].getHeight()) or road5BikeList[i].collisionTest(jayList[0].getPosition(), jayList[0].getWidth(), jayList[0].getHeight()):
                    tempxy = jayList[0].getPosition()
                    jayList[0]= jayStateList[1]
                    jayList[0].setPosition(tempxy[0],tempxy[1])
                    jayList[0].setSpeed(20)
                    bikeHit += 1
        elif bikeHit<24:
            for i in range(4):
                if road2BikeList[i].collisionTest(jayList[0].getPosition(), jayList[0].getWidth(), jayList[0].getHeight()) or road4BikeList[i].collisionTest(jayList[0].getPosition(), jayList[0].getWidth(), jayList[0].getHeight()) or road5BikeList[i].collisionTest(jayList[0].getPosition(), jayList[0].getWidth(), jayList[0].getHeight()):
                    tempxy = jayList[0].getPosition()
                    jayList[0]= jayStateList[2]
                    jayList[0].setPosition(tempxy[0],tempxy[1])
                    jayList[0].setSpeed(10)
                    bikeHit += 1
        else:
            for i in range(4):
                if road2BikeList[i].collisionTest(jayList[0].getPosition(), jayList[0].getWidth(), jayList[0].getHeight()) or road4BikeList[i].collisionTest(jayList[0].getPosition(), jayList[0].getWidth(), jayList[0].getHeight()) or road5BikeList[i].collisionTest(jayList[0].getPosition(), jayList[0].getWidth(), jayList[0].getHeight()):
                    breakLoop1=False
        
        
        #Collision Test for Ambulances
        
        for i in range(5):
            if ambulanceList[i].collisionTest(jayList[0].getPosition(),jayList[0].getWidth(),jayList[0].getHeight()):
                tempxy = jayList[0].getPosition()
                jayList[0] = jayStateList[0]
                jayList[0].setPosition(tempxy[0],tempxy[1])
                jayList[0].setSpeed(30)
                bikeHit = 0

        '''Changing the Direction of the Cat'''
        def switchHelper(state, speed):
            jayList[0] = state
            jayList[0].setPosition(tempxy[0],tempxy[1])
            jayList[0].setSpeed(speed)
            
        #When Cat moves to the right
        if jayList[0].getPosition()[0]>=1200:
            if destinationCat == "right":
                scoreNumber+=1
                destinationCat = 'left'
            tempxy = jayList[0].getPosition()
            jayStateList[0] = jayLeftHealthy
            jayStateList[1] = jayLeftInjured1
            jayStateList[2] = jayLeftInjured2
            if jayList[0] == jayHealthy:
                switchHelper(jayLeftHealthy, 30)
            if jayList[0] == jayInjured1:
                switchHelper(jayLeftInjured1, 20)
            if jayList[0] == jayInjured2:
                switchHelper(jayLeftInjured2, 10)
            
        #When Cat moves to the left
        if jayList[0].getPosition()[0]<=200:
            if destinationCat == "left":
                scoreNumber+=1
                destinationCat = 'right'
            tempxy = jayList[0].getPosition()
            jayStateList[0] = jayHealthy
            jayStateList[1] = jayInjured1
            jayStateList[2] = jayInjured2
            if jayList[0] == jayLeftHealthy:
                switchHelper(jayHealthy, 30)
            if jayList[0] == jayLeftInjured1:
                switchHelper(jayInjured1, 20)
            if jayList[0] == jayLeftInjured2:
                switchHelper(jayInjured2, 10)
        
        '''Other Misc Prints'''        
        #Blits and prints Helper Messages and Scores
        highScore = scorefont.render("SCORE:"+str(scoreNumber),True,black)
        highScorePos = highScore.get_rect()
        surface.blit(highScore, (20,750))
        surface.blit(helperMsg, (15,0))
        surface.blit(helperMsg1, (17, 25))
        surface.blit(helperMsg0, (36,50))
        surface.blit(helperMsg2, (1210, 0))
        surface.blit(helperMsg3, (1210, 25))
        surface.blit(helperMsg4, (1210, 50))
        surface.blit(helperMsg5, (1210, 75))
        
        '''Restart Key'''
        #Pressing R will reset the game, it breaks this loop and skips the next while loop and goes back to the first while loop, resetting the elements of the game.
        if key == "r":
            breakLoop1= False
            breakLoop2= False
        
        pygame.display.update()
        fpsClock.tick(FPS)
    
    
    while breakLoop2:
        #This while loop is initiated when Jay dies, and it prints a "you lose" message
        surface.blit(lossMsg, (0,300))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                key = event.unicode
        #Pressing R restarts the game, breaks this loop and goes to the 1st while loop that resets all the elements of the game.
        if key == "r":
            breakLoop2 = False
