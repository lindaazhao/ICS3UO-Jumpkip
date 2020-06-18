import pygame
import random

# Things I still need to add:
# display scoretracker that starts counting once you start
# increase in xvel as the score gets higher (every 1000 or something)
# call it jumpkip lmfao
# obstacle collision (end game when main character hits an obstacle)


# initialize display
pygame.init()
screensize = screenwidth, screenheight = 640, 480
screen = pygame.display.set_mode(screensize)

# main character
x = 40
y = 300
width = 40
height = 50
yvel = 750 # initial y velocity of main character for jumping

ground = 350 # y value of the ground

# obstacles
xvel = 150 # starting speed of obstacles
obstacle_list = [] # maintain a list of all obstacles that are currently on screen (active)
xdiff = random.randint(120, 400)


class Obstacle:
    def __init__(self, size, groundheight):
        self.size = size
        self.groundheight = groundheight
        self.x = 640

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), [int(self.x), int(self.groundheight-self.size), self.size, self.size])

    def updatePos(self, deltaTime, velocity):
        self.x -= (velocity*deltaTime)


newObstacle = Obstacle(25, 350)
obstacle_list.append(newObstacle)

running = True
gameStart = False

isJump = False
cancelJump = False
lastFrame = pygame.time.get_ticks() # get time in milliseconds since pygame.init()

while running:
    time = pygame.time.get_ticks()  # get time in milliseconds since pygame.init()
    deltaTime = (time - lastFrame)/1000.0
    lastFrame = time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_SPACE: # make character jump
                isJump = True
                gameStart = True # game starts once user jumps for the first time
            if event.key == pygame.K_DOWN: # make character go back to ground
                yvel = 0
                cancelJump = True
                isJump = False

    if isJump:
        yvel += -1800 * deltaTime
        y -= yvel * deltaTime
        if y > ground-height:
            isJump = False
            yvel = 750
            y = 300

    if cancelJump:
        yvel += -4500 * deltaTime
        y -= yvel * deltaTime
        if y > ground-height:
            cancelJump = False
            yvel = 750
            y = 300

    if gameStart:  # obstacles start rolling
        for obs in obstacle_list:
            obs.x -= xvel * deltaTime

    # temporary - fill the screen with black & draw the main character (currently a blue rectangle)
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (0, 100, 255), (x, int(y), width, height))

    # main loop for drawing obstacles
    for i in range(len(obstacle_list)):
        obs = obstacle_list[i] # set current obstacle
        if i == len(obstacle_list)-1:
            obs.draw(screen)
            if len(obstacle_list) == i+1: # test if obs is last obstacle
                print(xdiff)
                if obs.x < (640 - xdiff): # if current obstacle is xdiff away from the edge of the screen (satisfies xdiff for new obstacle generation)
                    print(obs.x)
                    newObstacle = Obstacle(25, 350) # generate a new obstacle
                    obstacle_list.append(newObstacle)
                    xdiff = random.randint(100, 500) # generate a random number for the distance between last obstacle and new obstacle to be generated
        else:
            obs.draw(screen)

    pygame.display.flip()

pygame.quit()
