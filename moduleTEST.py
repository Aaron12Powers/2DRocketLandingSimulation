import random
import math
from pygame.locals import *
import pygame

rocket_img = pygame.image.load('Assets/rocket.png')
rocket_thrusting_img = pygame.image.load('Assets/rocketThrusting.png')
rocket_success_img = pygame.image.load('Assets/rocketSuccess.png')
rocket_fail_img = pygame.image.load('Assets/rocketFail.png')
rocket_flipped = pygame.transform.flip(rocket_img, False, False)


WHITE = (255, 255, 255)
LIGHT_GREY = (155, 155, 155)
GREY = (128, 128, 128)
BLACK = (0, 0, 0)
RED = (255,0,0)
GREEN = (0,128,0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (135,206,250)

TERMINAL_VELOCITY = 100

class thruster(object):
    def __init__(self, isEnabled, flameColor, boosterColor):
        self.isEnabled = False
        self.flameColor = flameColor
        self.boosterColor = boosterColor

class rocket(object):
    def __init__(self, column, row, rotation):
        #centerpoints
        self.column = column
        self.row = row

        #radians
        self.rotation = rotation
        self.color = WHITE
        self.rocketThruster = thruster(True, RED, LIGHT_GREY)
        self.velocity = 0
        self.timeFalling = 0
        self.timeThrusting = 0
        self.rightThrust = False
        self.leftThrust = False
        print('test')

def DrawBackground(pygame, screen, columns, rows):
    screen.fill(LIGHT_BLUE)
    pygame.draw.rect(screen, GREEN, [0, rows, columns, -rows/8])
    pygame.draw.rect(screen, GREY, [(columns / 2) - (columns / 8), rows - (rows/8 - rows/64), columns/4, -rows/64])

def DrawRocket(pygame, screen, columns, rows, rocket):
    width = columns / 30
    height = rows / 8

    #maximum size rocket can be. only area needed to calculate for
    squareSize = math.sqrt((width * width) + (height * height))
    (corners, thrusterCorners) = getCorners(screen,rocket, width, height)
    slopes = []
    intercepts = []

    

    

    # getSlopeIntercepts(corners, slopes, intercepts)
    # DrawRocketMain(screen, rocket, squareSize, corners, slopes, intercepts, rocket.color)
    


    print(rocket.velocity)

    if rocket.rocketThruster.isEnabled:
        intercepts = []
        getSlopeIntercepts(thrusterCorners, slopes, intercepts)
        screen.blit(pygame.transform.rotate(rocket_thrusting_img, rocket.rotation * -57.2958), (rocket.column - width/2, rocket.row - height / 2))
    

                            
    if rocket.rocketThruster.isEnabled and rocket.row + height <= rows - rows/16:
        if rocket.velocity > 0:
            rocket.row += rocket.velocity / 5

        else:
            rocket.column += math.sin(rocket.rotation + math.pi) * rocket.velocity / 5
            rocket.row -= math.cos(rocket.rotation + math.pi) * rocket.velocity / 5
    
        if rocket.velocity >= -1 * TERMINAL_VELOCITY: 
            rocket.velocity -= 1
            rocket.timeFalling = 0
        
    elif not rocket.rocketThruster.isEnabled and rocket.row + height <= rows - rows/16:
        print(rocket.velocity)
        screen.blit(pygame.transform.rotate(rocket_img, rocket.rotation * -57.2958), (rocket.column - width/2, rocket.row - height / 2))
        if rocket.velocity <= TERMINAL_VELOCITY: 
            rocket.velocity += 1
        
        if rocket.velocity > 0:
            print('NUM1')
            rocket.column -= abs(math.sin(rocket.rotation + math.pi)) * rocket.velocity / 10
            # fall should be more or less constant fo gravity
            rocket.row += rocket.velocity / 5
        
        else:
            print('NUM2')
            rocket.column += math.sin(rocket.rotation + math.pi) * rocket.velocity / 10
            # fall should be more or less constant fo gravity
            rocket.row -= math.cos(rocket.rotation + math.pi) * rocket.velocity / 10


    elif rocket.row + height >= rows - rows/8 and rocket.column >= columns / 4 and rocket.column <= columns - columns * 3 / 8 and rocket.velocity <= 25 and (rocket.rotation < math.pi / 16 or rocket.rotation > (2 * math.pi) - (math.pi / 16)):
        rocket.color = GREEN
        rocket.rocketThruster.isEnabled = False
        screen.blit(pygame.transform.rotate(rocket_success_img, rocket.rotation * -57.2958), (rocket.column - width/2, rocket.row - height / 2))
        print(rocket.velocity)
        print('Velocity at Land: ', rocket.velocity)
        print('Target column: ', columns / 4)
        print('Actual column: ', rocket.column)
        print('You Survived')


    else:
        rocket.color = RED
        rocket.rocketThruster.isEnabled = False
        screen.blit(pygame.transform.rotate(rocket_fail_img, rocket.rotation * -57.2958), (rocket.column - width/2, rocket.row - height / 2))
        if rocket.velocity > 25:
            print('Velocity at Land: ', rocket.velocity)
            print('Came in too hot')
        if rocket.column < columns / 4 or rocket.column > columns - columns / 4:
            print('Aim for the Pad!')
        print('Failed')

def getCorners(screen,rocket, width, height):

    corners = []
    thrusterCorners = []

    #corner1
    tempX = rocket.column - (width / 2) - rocket.column
    tempY = rocket.row - (height / 2) - rocket.row
    rotatedX = tempX*math.cos(rocket.rotation) - tempY*math.sin(rocket.rotation)
    rotatedY = tempX*math.sin(rocket.rotation) + tempY*math.cos(rocket.rotation)
    corners.extend([(rotatedX + rocket.column, rotatedY + rocket.row)])
    # screen.set_at((int(rotatedX + rocket.column), int(rotatedY + rocket.row)), GREEN)
    
    #corner 2
    tempX = rocket.column + (width / 2) - rocket.column
    tempY = rocket.row - (height / 2) - rocket.row
    rotatedX = tempX*math.cos(rocket.rotation) - tempY*math.sin(rocket.rotation)
    rotatedY = tempX*math.sin(rocket.rotation) + tempY*math.cos(rocket.rotation)
    corners.extend([(rotatedX + rocket.column, rotatedY + rocket.row)])
    # screen.set_at((int(rotatedX + rocket.column), int(rotatedY + rocket.row)), GREEN)

    #corner 3
    tempX = rocket.column - (width / 2) - rocket.column
    tempY = rocket.row + (height / 2) - rocket.row
    rotatedX = tempX*math.cos(rocket.rotation) - tempY*math.sin(rocket.rotation)
    rotatedY = tempX*math.sin(rocket.rotation) + tempY*math.cos(rocket.rotation)
    corners.extend([(rotatedX + rocket.column, rotatedY + rocket.row)])
    # screen.set_at((int(rotatedX + rocket.column), int(rotatedY + rocket.row)), RED)

    #corner 4
    tempX = rocket.column + (width / 2) - rocket.column
    tempY = rocket.row + (height / 2) - rocket.row
    rotatedX = tempX*math.cos(rocket.rotation) - tempY*math.sin(rocket.rotation)
    rotatedY = tempX*math.sin(rocket.rotation) + tempY*math.cos(rocket.rotation)
    corners.extend([(rotatedX + rocket.column, rotatedY + rocket.row)])
    # screen.set_at((int(rotatedX + rocket.column), int(rotatedY + rocket.row)), RED)

    #additional Thruster Corners

    thrusterCorners.append((corners[2][0], corners[2][1]))
    thrusterCorners.append((corners[3][0], corners[3][1]))

    tempX = rocket.column - (width / 2) - rocket.column
    tempY = rocket.row + ((40 + height) / 2) - rocket.row
    rotatedX = tempX*math.cos(rocket.rotation) - tempY*math.sin(rocket.rotation)
    rotatedY = tempX*math.sin(rocket.rotation) + tempY*math.cos(rocket.rotation)
    thrusterCorners.extend([(rotatedX + rocket.column, rotatedY + rocket.row)])

    tempX = rocket.column + (width / 2) - rocket.column
    tempY = rocket.row + ((40 + height) / 2) - rocket.row
    rotatedX = tempX*math.cos(rocket.rotation) - tempY*math.sin(rocket.rotation)
    rotatedY = tempX*math.sin(rocket.rotation) + tempY*math.cos(rocket.rotation)
    thrusterCorners.extend([(rotatedX + rocket.column, rotatedY + rocket.row)])



    return (corners, thrusterCorners)

def getSlopeIntercepts(corners, slopes, intercepts):
    try:
        slopes.extend([(corners[0][1] - corners[1][1]) / (corners[0][0] - corners[1][0])])
    except:
        slopes.extend([99999])
    intercepts.extend([-1 * ((slopes[0] * corners[0][0]) - corners[0][1])])

    try:
        slopes.extend([(corners[1][1] - corners[3][1]) / (corners[1][0] - corners[3][0])])
    except:
        slopes.extend([-99999])
    intercepts.extend([-1 * ((slopes[1] * corners[1][0]) - corners[1][1])])

    try:
        slopes.extend([(corners[3][1] - corners[2][1]) / (corners[3][0] - corners[2][0])])
    except:
        slopes.extend([2147483647])
    intercepts.extend([-1 * ((slopes[2] * corners[2][0]) - corners[2][1])])

    try:
        slopes.extend([(corners[2][1] - corners[0][1]) / (corners[2][0] - corners[0][0])])
    except:
        slopes.extend([-2147483647])
    intercepts.extend([-1 * ((slopes[3] * corners[0][0]) - corners[0][1])])

def DrawRocketMain(screen, rocket, squareSize, corners, slopes, intercepts, color):
    for i in range(int(rocket.column - (squareSize/2)), int(rocket.column + (squareSize/2))):
        for j in range(int(rocket.row - (squareSize/2)), int(rocket.row + (squareSize/2))):
            if rocket.rotation <= math.pi / 2 and rocket.rotation >= 0:
                temp = slopes[0] * i + intercepts[0]
                if temp < j:
                    temp = slopes[1] * i + intercepts[1]
                    if temp > j:
                        temp = slopes[2] * i + intercepts[2]
                        if temp > j:
                            temp = slopes[3] * i + intercepts[3]
                            if temp < j:
                                screen.set_at((int(i), int(j)), color)
                                

            elif rocket.rotation <= math.pi and rocket.rotation >= 0:
                temp = slopes[0] * i + intercepts[0]
                if temp > j:
                    temp = slopes[1] * i + intercepts[1]
                    if temp > j:
                        temp = slopes[2] * i + intercepts[2]
                        if temp < j:
                            temp = slopes[3] * i + intercepts[3]
                            if temp < j:
                                screen.set_at((int(i), int(j)), color)
                                
            elif rocket.rotation <= math.pi + (math.pi / 2) and rocket.rotation >= 0:
                temp = slopes[0] * i + intercepts[0]
                if temp > j:
                    temp = slopes[1] * i + intercepts[1]
                    if temp < j:
                        temp = slopes[2] * i + intercepts[2]
                        if temp < j:
                            temp = slopes[3] * i + intercepts[3]
                            if temp > j:
                                screen.set_at((int(i), int(j)), color)                              
                                

            else:
                temp = slopes[0] * i + intercepts[0]
                if temp < j:
                    temp = slopes[1] * i + intercepts[1]
                    if temp < j:
                        temp = slopes[2] * i + intercepts[2]
                        if temp > j:
                            temp = slopes[3] * i + intercepts[3]
                            if temp > j:
                                screen.set_at((int(i), int(j)), color) 
                                
