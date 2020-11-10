#Space_Invader Game

# main.py

import pygame
import random
import math

from pygame import mixer

# Intialize the pygame
pygame.init()

#create the screen
screen = pygame.display.set_mode((800,600)) #Width,Height

# Background
background = pygame.image.load("background.png")

# Background Music
mixer.music.load("background.wav")
mixer.music.play(-1)

# Title 
pygame.display.set_caption("Space Invaders")

# Icon (source : https://www.flaticon.com/)
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("battleship.png")
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("alien.png"))
    enemyX.append(random.randint(0,736))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# missile

'''
Ready -> You cant see the missile on screen
Fire -> The missile is currently moving/Launch
'''

missileImg = pygame.image.load("missile.png")
missileX = 0
missileY = 480
missileX_change = 0
missileY_change = 10
missile_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)

textX = 10
testY = 10

# GAME OVER TEXT
over_font = pygame.font.Font('freesansbold.ttf',64)

def game_over_text():
    over_text = over_font.render("GAME-OVER",True, (255,255,255))
    screen.blit(over_text, (200,250))

def show_score(x,y):
    score = font.render("Score : " + str(score_value),True, (255,255,255))
    screen.blit(score, (x,y))

def player(x,y):
    screen.blit(playerImg,(x,y))

def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))

def fire_missile(x,y):
    global missile_state
    missile_state = "fire"
    screen.blit(missileImg,(x + 16, y + 10))

def isCollision(enemyX, enemyY, missilex, missileY):
    """
    Pythagorean theorem as d=√((x_2-x_1)²+(y_2-y_1)²)
    to find the distance between any two points.
    """
    distance = math.sqrt((math.pow(enemyX-missileX,2)) + (math.pow(enemyY-missileY,2)))

    if distance < 27:
        return True
    else:
        return False
    
running = True
#Infinite GAME Loop
while running:
    
    # RGB - Red, Green, Blue
    screen.fill((0,0,0))

    # Background Image
    screen.blit(background,(0,0))

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # IF keystroke pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            #print("a keystoke is pressed.")
            if event.key == pygame.K_LEFT:
                #print("Left arrow is pressed")
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                #print("Right arrow is pressed")
                playerX_change = 5
            if  event.key == pygame.K_SPACE:
                if missile_state is "ready":
                    
                    missile_sound = mixer.Sound("laser.wav")
                    missile_sound.play()
                    
                    missileX = playerX
                    fire_missile(playerX,missileY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                #print("Keystoke has been released")
                playerX_change = 0


    # Checking Boundries of spaceship
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736: #800 - 64(spaceship pixals)
        playerX = 736


    for i in range(num_of_enemies):

        # Game OVER
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        
        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736: #800 - 64(spaceship imagepixals)
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i],enemyY[i],missileX,missileY)

        if collision:
            explosion_Sound = mixer.Sound("explosion.wav")
            explosion_Sound.play()
            missileY = 480
            missile_state = "ready"
            score_value += 1
            #print("Score : {}".format(score))
            enemyX[i] = random.randint(0,736)
            enemyY[i] = random.randint(50,150)

        enemy(enemyX[i],enemyY[i], i)


    # Missile movement
    if missileY <= 0:
        missileY = 480
        missile_state = "ready"
    
    if  missile_state is "fire":
        fire_missile(missileX,missileY)
        missileY -= missileY_change
    
    player(playerX,playerY)

    show_score(textX,testY)
    
    pygame.display.update()
