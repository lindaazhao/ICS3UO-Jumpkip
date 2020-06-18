import pygame
import random

# Things I still need to add:
# call it jumpkip lmfao
# instructions on how to play the game
# game over end screen & way to restart game
# allll the graphics

# --- Stuff that's DONE! ---
# obstacle collision (end game when main character hits an obstacle)
# display scoretracker that starts counting once you start
# increase in xVel as the score gets higher (every 1000 or something)


# initialize display
pygame.init()
screensize = screenwidth, screenheight = 640, 480
screen = pygame.display.set_mode(screensize)

# ----- Game Elements -----
ground = 350  # y value of the ground
scoreTracker = 0
running = True
gameStart = False
gameOver = False
isJump = False
cancelJump = False
lastFrame = pygame.time.get_ticks()  # get time in milliseconds since pygame.init()
white = (255, 255, 255)


# function used to display text onto game screen
def write(text, size, colour, xpos, ypos):
    font = pygame.font.SysFont("consolas", size)
    texttoscreen = font.render(text, False, colour)
    screen.blit(texttoscreen, (xpos, ypos))


# ----- Main Character -----
x = 40
y = 300
width = 40
height = 50
yVel = 750  # initial y velocity of main character for jumping

# ----- Obstacles -----
xVel = 150  # starting speed of obstacles
obstacle_list = []  # maintain a list of all obstacles that are currently on screen (active)
xDiff = random.randint(120, 400)


class Obstacle:
    def __init__(self, size, groundY):
        self.size = size
        self.groundY = groundY
        self.x = 640

    def draw(self, display):
        pygame.draw.rect(display, (255, 0, 0), [int(self.x), int(self.groundY-self.size), self.size, self.size])


newObstacle = Obstacle(25, ground)
obstacle_list.append(newObstacle)


# ----- Main Game Loop -----
while running:
    time = pygame.time.get_ticks()  # get time in milliseconds since pygame.init()
    deltaTime = (time - lastFrame)/1000.0
    lastFrame = time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_SPACE:  # make character jump
                isJump = True
                gameStart = True  # game starts once user jumps for the first time
            if event.key == pygame.K_DOWN:  # make character go back to ground
                yVel = 0
                cancelJump = True
                isJump = False

    if isJump:
        yVel += -1800 * deltaTime
        y -= yVel * deltaTime
        if y > ground-height:
            isJump = False
            yVel = 750
            y = 300

    if cancelJump:
        yVel += -6000 * deltaTime
        y -= yVel * deltaTime
        if y > ground-height:
            cancelJump = False
            yVel = 750
            y = 300

    if gameStart:  # obstacles start rolling
        for obs in obstacle_list:
            obs.x -= xVel * deltaTime
            for i in range(x, x+width):
                for j in range(int(y), int(y+height)):
                    if i in range(int(obs.x), int(obs.x+obs.size)) and j in range(obs.groundY-obs.size, obs.groundY):
                        gameOver = True
        scoreTracker += 30 * deltaTime
        print(int(scoreTracker))
        # increase speed of obstacles by 2 for every 100 points
        if int(scoreTracker) >= 100 and (int(scoreTracker) % 100) == 0:
            xVel += 2
        # increase speed of obstacles by 30 for every 1000 points
        if int(scoreTracker) >= 1000 and (int(scoreTracker) % 1000) == 0:
            xVel += 30
            scoreTracker += 1  # prevents xVel from increase multiple times until scoreTracker increases



    # ----- Drawing to the Screen -----
    # temporary - fill the screen with black & draw the main character (currently a blue rectangle)
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (0, 100, 255), (x, int(y), width, height))

    # main loop for drawing obstacles
    for i in range(len(obstacle_list)):
        obs = obstacle_list[i]  # set current obstacle
        # Test if obs is last obstacle
        if i == len(obstacle_list)-1:
            obs.draw(screen)
            # print(xDiff) TEST
            # Test if current obstacle satisfies conditions for new obstacle generation
            # Condition: current obstacle must be xDiff away from edge of screen where a new obstacle is generated
            if obs.x < (640 - xDiff):
                # print(obs.x) TEST
                # Generate a new obstacle and add it to the list of active obstacles
                newObstacle = Obstacle(25, ground)
                obstacle_list.append(newObstacle)
                # Generate a random number for the distance between last obstacle and new obstacle to be generated
                xDiff = random.randint(150, 500)
        # If obstacle is off screen, remove it from the list of active obstacles
        if obs.x < 0-obs.size:
            obstacle_list.remove(obs)
            break
        else:
            obs.draw(screen)

    if gameOver:  # if main character hits an obstacle
        gameStart = False
        isJump = False
        cancelJump = False
        yVel = 0
        xVel = 0
        write("Game Over!", 50, white, 175, 200)

    write("Score: " + str(int(scoreTracker)), 30, white, 50, 50)

    # Update the display
    pygame.display.flip()

pygame.quit()
