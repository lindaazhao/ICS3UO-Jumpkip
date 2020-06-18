# ICS3UO - Pygame Assignment
# Student: Linda Zhao

import pygame
import random

# Initialize game display
pygame.init()
screensize = screenwidth, screenheight = 640, 480
screen = pygame.display.set_mode(screensize)


# Function used to display text onto the game screen
# modified from the example on the following website: https://pythonprogramming.net/displaying-text-pygame-screen/
def write(text, size, colour, xpos, ypos):
    font = pygame.font.SysFont("consolas", size)
    texttoscreen = font.render(text, False, colour)
    screen.blit(texttoscreen, (xpos, ypos))


# Function to update the game screen - Includes all drawing except for obstacle drawing
def redrawGameScreen():
    screen.blit(background, (0, 0))  # draw in the background

    # display instructions to play, static character
    if introScreen:
        screen.blit(char, (int(x), int(y)))
        write("Welcome to Jumpkip!", 30, black, 160, 130)
        write("Press the space key or up arrow key to jump", 20, black, 80, 170)
        write("and the down arrow key to fall back down.", 20, black, 90, 195)

    # used to animate the mudkip when the game has started
    if gameStart:
        global animCount
        if animCount + 1 >= 20:
            animCount = 0
        screen.blit(mudkipAnim[animCount//5], (int(x), int(y)))
        animCount += 1

    # display game over instructions, static character
    if gameOver:
        screen.blit(char, (int(x), int(y)))
        write("Game Over!", 40, black, 200, 150)
        write("Jump to restart the game.", 20, black, 175, 200)

    # write score to the screen
    write("Score: " + str(int(scoreTracker)), 30, white, 50, 50)


# ---------- Game Elements & Variables ----------
ground = 300  # y value of the ground
scoreTracker = 0
running = True
gameStart = False
gameOver = False
isJump = False
cancelJump = False
introScreen = True
clock = pygame.time.Clock()
lastFrame = pygame.time.get_ticks()  # get time in milliseconds since pygame.init()
background = pygame.transform.scale(pygame.image.load('img/bg.png'), (700, 480))
# colours
white = (255, 255, 255)
black = (0, 0, 0)
# sound effects
jumpSound = pygame.mixer.Sound('sound/jumpSound.wav')
playJumpSound = True
deathSound = pygame.mixer.Sound('sound/deathSound.wav')


# ---------- Main Character ----------
x = 40  # starting x position
y = 250  # starting y position
width = 50
height = 50
animCount = 0  # used to animate the main character
yVel = 650  # initial y velocity of main character for jumping
mudkipAnim = [pygame.transform.scale(pygame.image.load('img/mudkip1.png'), (50, 50)),
              pygame.transform.scale(pygame.image.load('img/mudkip2.png'), (50, 50)),
              pygame.transform.scale(pygame.image.load('img/mudkip1.png'), (50, 50)),
              pygame.transform.scale(pygame.image.load('img/mudkip2.png'), (50, 50))]
char = pygame.transform.scale(pygame.image.load('img/mudkip1.png'), (50, 50))


# ---------- Obstacles ----------
# Obstacle class used to generate multiple instances of obstacles
# Used to set obstacle width, height, x and y positions, and also includes function to draw the obstacle
class Obstacle:
    def __init__(self, obsWidth, obsHeight, groundY):
        self.width = obsWidth
        self.height = obsHeight
        self.groundY = groundY
        self.x = 640

    def draw(self):
        if self.height == 23:
            obsType = obsGraphics[0]
        elif self.height == 14:
            obsType = obsGraphics[1]
        elif self.height == 27:
            obsType = obsGraphics[2]
        else:
            obsType = obsGraphics[3]
        screen.blit(obsType, (int(self.x), int(self.groundY - self.height)))


xVel = 200  # starting speed of obstacles
obstacle_list = []  # maintain a list of all obstacles that are currently on screen (active)
obsGraphics = [pygame.transform.scale(pygame.image.load('img/obs1.png'), (35, 23)),
               pygame.transform.scale(pygame.image.load('img/obs2.png'), (25, 14)),
               pygame.transform.scale(pygame.image.load('img/obs3.png'), (35, 27)),
               pygame.transform.scale(pygame.image.load('img/obs4.png'), (35, 35))]
obsWidths = [35, 25, 35, 35]
obsHeights = [23, 14, 27, 35]
# generates and creates first obstacle of the game
obsSize = random.randint(0, 3)
xDiff = random.randint(150, 500)
newObstacle = Obstacle(obsWidths[obsSize], obsHeights[obsSize], ground)
obstacle_list.append(newObstacle)


# ---------- Main Game Loop ----------
while running:
    clock.tick(20)  # sets the rate at which the loop runs; used for animating main character
    time = pygame.time.get_ticks()  # get time in milliseconds since pygame.init()
    deltaTime = (time - lastFrame)/1000.0
    lastFrame = time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_SPACE:  # make character jump
                if gameOver:
                    # reset all game variables to start a new game
                    yVel = 650
                    xVel = 200
                    scoreTracker = 0
                    obstacle_list = []
                    gameOver = False
                    isJump = True
                    gameStart = True
                    playJumpSound = True
                    # create new "first" obstacle
                    xDiff = random.randint(150, 500)
                    obsSize = random.randint(0, 3)
                    newObstacle = Obstacle(obsWidths[obsSize], obsHeights[obsSize], ground)
                    obstacle_list.append(newObstacle)
                    break
                isJump = True
                gameStart = True  # game starts once user jumps for the first time
            if event.key == pygame.K_DOWN:  # make character go back to ground
                yVel = 0
                cancelJump = True
                isJump = False

    # True if player presses up key
    # Adds downwards acceleration on yVel and changes y coord accordingly
    # Player can only jump when character is on the ground to prevent mid-air jumps
    if isJump:
        yVel += -1800 * deltaTime
        y -= yVel * deltaTime
        if y > ground-height:
            isJump = False
            yVel = 650
            y = 250
        if playJumpSound:
            jumpSound.play()
            playJumpSound = False

    # True if player presses down key
    # Adds faster acceleration downwards and changes y coord accordingly
    if cancelJump:
        yVel += -6000 * deltaTime
        y -= yVel * deltaTime
        if y > ground-height:
            cancelJump = False
            yVel = 650
            y = 250

    # True if player presses jump key on introScreen or gameOver screen
    if gameStart:
        playDeathSound = True
        introScreen = False
        # obstacles begin moving from right to left
        for obs in obstacle_list:
            obs.x -= xVel * deltaTime
            # collision detection: if player (x,y) overlaps with obstacle (x, y), game is ended
            for i in range(x, x+width):
                for j in range(int(y), int(y+height)):
                    if i in range(int(obs.x), int(obs.x+obs.width)) and j in range(obs.groundY-obs.height, obs.groundY):
                        gameOver = True
        # updates score
        scoreTracker += 30 * deltaTime
        # increase speed of obstacles by 2 for every 100 points
        if int(scoreTracker) >= 100 and (int(scoreTracker) % 100) == 0:
            xVel += 3
        # increase speed of obstacles by 30 for every 1000 points
        if int(scoreTracker) >= 1000 and (int(scoreTracker) % 1000) == 0:
            xVel += 30
            scoreTracker += 1  # prevents xVel from increase multiple times until scoreTracker increases
        # sound can only play if player is on ground (prevents sound from playing multiple times)
        if y == ground-height:
            playJumpSound = True

    # True if player hits an obstacle
    if gameOver:
        gameStart = False
        cancelJump = False
        isJump = False
        if playDeathSound:
            deathSound.play()
            playDeathSound = False
        yVel = 0
        xVel = 0

    # Call function to redraw all game elements
    redrawGameScreen()

    # Main loop for drawing obstacles
    for i in range(len(obstacle_list)):
        obs = obstacle_list[i]  # set current obstacle
        # Test if obs is last obstacle
        if i == len(obstacle_list)-1:
            obs.draw()
            # Test if current obstacle satisfies conditions for new obstacle generation
            # Condition: current obstacle must be xDiff away from edge of screen where a new obstacle is generated
            if obs.x < (640 - xDiff):
                # Generate a new obstacle and add it to the list of active obstacles
                obsSize = random.randint(0, 3)
                newObstacle = Obstacle(obsWidths[obsSize], obsHeights[obsSize], ground)
                obstacle_list.append(newObstacle)
                # Generate a random number for the distance between last obstacle and new obstacle to be generated
                xDiff = random.randint(150, 500)
        # If obstacle is off screen, remove it from the list of active obstacles
        if obs.x < 0-obs.width:
            obstacle_list.remove(obs)
            break
        else:
            obs.draw()

    # Update the display
    pygame.display.flip()

pygame.quit()
