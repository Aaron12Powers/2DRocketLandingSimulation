from pygame.locals import *
import numpy as np
from random import randint
import pygame
import math
import module


randomize = False


#Define Window Size in px
COLUMNS = 700
ROWS = COLUMNS
#Define Rocket Start and Angle. 0 = straight up
startRow = 100
startColumn = 150


#Define Colors
WHITE = (255, 255, 255)
LIGHT_GREY = (155, 155, 155)
GREY = (128, 128, 128)
BLACK = (0, 0, 0)
RED = (255,0,0)
GREEN = (0,128,0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (135,206,250)





screen = pygame.display.set_mode((COLUMNS, ROWS))

pygame.display.set_caption('RocketSim')

if randomize:
    print('randomizing')


grid = []
for row in range(6):
    grid.append([])
    for column in range(8):
        grid[row].append(0)



running = True


clock = pygame.time.Clock()

tick_count = 0

step = 0

pause = True
complete = False

rocket = module.rocket(startColumn, startRow)

currentCoords = []

screen.fill(LIGHT_BLUE)
module.DrawBackground(pygame, screen, COLUMNS, ROWS)  
module.DrawRocket(pygame, screen, COLUMNS, ROWS, rocket)
 
#Main pygame loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  
            running = False  # Exit loop/ close pygame when x is clicked
        key=pygame.key.get_pressed()  #checking pressed keys
        if key[pygame.K_RETURN]:
            if pause:
                pygame.display.set_caption('RocketSim')
                pause = False
            else:
                pygame.display.set_caption('RocketSim - PAUSED')
                rocket = module.rocket(startColumn, startRow)
                pause = True 

        elif key[pygame.K_SPACE]:
            if rocket.rocketThruster.isEnabled:
                rocket.rocketThruster.isEnabled = False
                print('Thruster OFF')
            else:
                rocket.rocketThruster.isEnabled = True
                print('Thruster ON')

        elif key[pygame.K_RIGHT]:
            rocket.rotation += .05
            if rocket.rotation >= math.pi * 2:
                rocket.rotation = rocket.rotation - (math.pi * 2)
            print('Rotation: ' , rocket.rotation)
            rocket.rightThrust = True

        elif key[pygame.K_LEFT]:
            rocket.rotation -= .05
            if rocket.rotation < 0:
                rocket.rotation = (2 * math.pi) - rocket.rotation            
                print(rocket.rotation)
            rocket.leftThrust = True



        elif event.type == pygame.MOUSEBUTTONDOWN and pause:
            # If Left Click Make wall
            if event.button == 1:
                pos = pygame.mouse.get_pos()

            # If Right click make End
            elif event.button == 2:
                pos = pygame.mouse.get_pos()

            # If Center Click Set Start
            elif event.button == 3:
                pos = pygame.mouse.get_pos()

        elif event.type == pygame.MOUSEBUTTONDOWN and complete:
            if event.button == 1:
                pos = pygame.mouse.get_pos()


    
    # Run Board
    if tick_count % 2 == 0 and not pause:
        # rocket.row = rocket.row + 1
        module.DrawBackground(pygame, screen, COLUMNS, ROWS)  
        module.DrawRocket(pygame, screen, COLUMNS, ROWS, rocket)

  


    tick_count += 1
    clock.tick(60)
   
    pygame.display.flip()