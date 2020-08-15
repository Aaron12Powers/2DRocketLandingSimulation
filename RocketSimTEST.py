from pygame.locals import *
import numpy as np
import random
import pygame
import math
import moduleTEST as module


randomize = False

#Define Window Size in px
COLUMNS = 750
ROWS = 1000
#Define Rocket Start and Angle. 0 = straight up
startRow = 100
startColumn = 375





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

if randomize:
    print('randomizing')
    rocket = module.rocket(random.randint(0, COLUMNS), 100, random.uniform(0, math.pi * 2))
else:
    rocket = module.rocket(startColumn, startRow, 0)

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
                if not randomize:
                    pygame.display.set_caption('RocketSim - PAUSED')
                    rocket = module.rocket(startColumn, startRow, 0)
                    pause = True 
                else:
                    rocket = module.rocket(random.randint(0, COLUMNS), 100, random.uniform(0, math.pi * 2))

        elif key[pygame.K_SPACE]:
            if rocket.rocketThruster.isEnabled:
                rocket.rocketThruster.isEnabled = False
                print('Thruster OFF')
            else:
                rocket.rocketThruster.isEnabled = True
                print('Thruster ON')

    if key[pygame.K_RIGHT]:
        rocket.rotation += .02
        if rocket.rotation >= math.pi * 2:
            rocket.rotation = rocket.rotation - (math.pi * 2)
        rocket.rightThrust = True

    if key[pygame.K_LEFT]:
        rocket.rotation -= .02
        if rocket.rotation < 0:
            rocket.rotation = (2 * math.pi) + rocket.rotation            
        rocket.leftThrust = True



        if event.type == pygame.MOUSEBUTTONDOWN and pause:
            # If Left Click Make wall
            if event.button == 1:
                pos = pygame.mouse.get_pos()

            # If Right click make End
            elif event.button == 2:
                pos = pygame.mouse.get_pos()

            # If Center Click Set St
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