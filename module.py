import random
import math

WHITE = (255, 255, 255)
LIGHT_GREY = (155, 155, 155)
GREY = (128, 128, 128)
BLACK = (0, 0, 0)
RED = (255,0,0)
GREEN = (0,128,0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (135,206,250)

class thruster(object):
    def __init__(self, isEnabled, flameColor, boosterColor):
        self.isEnabled = False
        self.flameColor = flameColor
        self.boosterColor = boosterColor

class rocket(object):
    def __init__(self, column, row):
        #centerpoints
        self.column = column
        self.row = row

        #radians
        self.rotation = 0
        self.color = WHITE
        self.rocketThruster = thruster(True, RED, LIGHT_GREY)
        self.velocity = 0
        self.timeFalling = 0
        self.timeThrusting = 0
        self.rightThrust = False
        self.leftThrust = False
        print('test')

def DrawBackground(pygame, screen, columns, rows):
    # for i in range(columns):
    #     for j in range(rows):
    #         if j <= rows - (rows / 10):
    screen.fill(LIGHT_BLUE)
    pygame.draw.rect(screen, GREEN, [0, rows, columns, -rows/8])
    pygame.draw.rect(screen, GREY, [(columns / 2) - (columns / 8), rows - (rows/8 - rows/64), columns/4, -rows/64])

def DrawRocket(pygame, screen, columns, rows, rocket):
    width = columns / 30
    height = rows / 8

    #maximum size rocket can be. only area needed to calculate for
    squareSize = math.sqrt((width * width) + (height * height))
    #replace with rotatable rectangle code
    # pygame.draw.rect(screen, rocket.color, [rocket.column - width/2, rocket.row-height/2, width, height])
    
    # pygame.draw.rect(screen, rocket.color, [rocket.column - (squareSize / 2), (rocket.row - (squareSize / 2)), squareSize, squareSize])
    
    corners = getCorners(screen,rocket, width, height)
    slopes = []
    intercepts = []


    getSlopeIntercepts(corners, slopes, intercepts)

    DrawRocketMain(screen, rocket, squareSize, corners, slopes, intercepts)

    
                                



    #replace with rotatable thruster
    #pygame.draw.rect(screen, rocket.rocketThruster.boosterColor, [rocket.column +  width/4, rocket.row + height - height/4 + 1, width/2, height/4])
    if rocket.rocketThruster.isEnabled and rocket.row + height <= rows - rows/8:
        rocket.row = rocket.row + rocket.timeThrusting / 5
        pygame.draw.rect(screen, rocket.rocketThruster.flameColor, [rocket.column - width/2, (rocket.row + rows/8) - height/2, columns/30, rows/32])

        rocket.row = rocket.row + rocket.velocity / 5

        # if rocket.velocity > 0:
        #     columnChange = rocket.rotation
        #     rowChange = rocket.rotation
        #     rocket.column = rocket.column + (columnChange * (rocket.velocity / 5))
        #     rocket.row = rocket.row + (rowChange * (rocket.velocity / 5))
        
        if abs(rocket.velocity) <= 100: 
            rocket.velocity -= 1
            rocket.timeFalling = 0
        
    elif not rocket.rocketThruster.isEnabled and rocket.row + height <= rows - rows/8:
        rocket.row = rocket.row + rocket.velocity / 5
        if abs(rocket.velocity) <= 100: 
            rocket.velocity += 1
            rocket.timeThrusting = 0
        

    elif rocket.row + height >= rows - rows/8 and rocket.column >= columns / 4 and rocket.column <= columns - columns / 4 and rocket.velocity <= 25:
        rocket.color = GREEN
        # print(rocket.velocity)
        # print('Velocity at Land: ', rocket.velocity)
        # print('Target column: ', columns / 4)
        # print('Actual column: ', rocket.column)
        # print('Pogu You survived')


    else:
        rocket.color = RED
        # if rocket.velocity > 25:
        #     print('Velocity at Land: ', rocket.velocity)
        #     print('Came in too hot')
        # if rocket.column < columns / 4 or rocket.column > columns - columns / 4:
        #     print('Aim for the Pad!')
        # print('yerdeadmate')


def getCorners(screen,rocket, width, height):

    corners = []

    #corner1
    tempX = rocket.column - (width / 2) - rocket.column
    tempY = rocket.row - (height / 2) - rocket.row
    rotatedX = tempX*math.cos(rocket.rotation) - tempY*math.sin(rocket.rotation)
    rotatedY = tempX*math.sin(rocket.rotation) + tempY*math.cos(rocket.rotation)
    corners.extend([(rotatedX + rocket.column, rotatedY + rocket.row)])
    screen.set_at((int(rotatedX + rocket.column), int(rotatedY + rocket.row)), RED)
    
    #corner 2
    tempX = rocket.column + (width / 2) - rocket.column
    tempY = rocket.row - (height / 2) - rocket.row
    rotatedX = tempX*math.cos(rocket.rotation) - tempY*math.sin(rocket.rotation)
    rotatedY = tempX*math.sin(rocket.rotation) + tempY*math.cos(rocket.rotation)
    corners.extend([(rotatedX + rocket.column, rotatedY + rocket.row)])
    screen.set_at((int(rotatedX + rocket.column), int(rotatedY + rocket.row)), RED)

    #corner 3
    tempX = rocket.column - (width / 2) - rocket.column
    tempY = rocket.row + (height / 2) - rocket.row
    rotatedX = tempX*math.cos(rocket.rotation) - tempY*math.sin(rocket.rotation)
    rotatedY = tempX*math.sin(rocket.rotation) + tempY*math.cos(rocket.rotation)
    corners.extend([(rotatedX + rocket.column, rotatedY + rocket.row)])
    screen.set_at((int(rotatedX + rocket.column), int(rotatedY + rocket.row)), RED)

    #corner 4
    tempX = rocket.column + (width / 2) - rocket.column
    tempY = rocket.row + (height / 2) - rocket.row
    rotatedX = tempX*math.cos(rocket.rotation) - tempY*math.sin(rocket.rotation)
    rotatedY = tempX*math.sin(rocket.rotation) + tempY*math.cos(rocket.rotation)
    corners.extend([(rotatedX + rocket.column, rotatedY + rocket.row)])
    screen.set_at((int(rotatedX + rocket.column), int(rotatedY + rocket.row)), RED)

    return corners

def getSlopeIntercepts(corners, slopes, intercepts):
    try:
        slopes.extend([(corners[0][1] - corners[1][1]) / (corners[0][0] - corners[1][0])])
    except:
        slopes.extend([2147483647])
    intercepts.extend([-1 * ((slopes[0] * corners[0][0]) - corners[0][1])])

    try:
        slopes.extend([(corners[1][1] - corners[3][1]) / (corners[1][0] - corners[3][0])])
    except:
        slopes.extend([-2147483647])
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

def DrawRocketMain(screen, rocket, squareSize, corners, slopes, intercepts):
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
                                screen.set_at((int(i), int(j)), rocket.color) 

            elif rocket.rotation <= math.pi:
                temp = slopes[0] * i + intercepts[0]
                if temp > j:
                    temp = slopes[1] * i + intercepts[1]
                    if temp > j:
                        temp = slopes[2] * i + intercepts[2]
                        if temp < j:
                            temp = slopes[3] * i + intercepts[3]
                            if temp < j:
                                screen.set_at((int(i), int(j)), rocket.color)

            elif rocket.rotation <= math.pi + (math.pi / 2):
                temp = slopes[0] * i + intercepts[0]
                if temp > j:
                    temp = slopes[1] * i + intercepts[1]
                    if temp < j:
                        temp = slopes[2] * i + intercepts[2]
                        if temp < j:
                            temp = slopes[3] * i + intercepts[3]
                            if temp > j:
                                screen.set_at((int(i), int(j)), rocket.color)                              

            else:
                temp = slopes[0] * i + intercepts[0]
                if temp < j:
                    temp = slopes[1] * i + intercepts[1]
                    if temp < j:
                        temp = slopes[2] * i + intercepts[2]
                        if temp > j:
                            temp = slopes[3] * i + intercepts[3]
                            if temp > j:
                                screen.set_at((int(i), int(j)), rocket.color)    