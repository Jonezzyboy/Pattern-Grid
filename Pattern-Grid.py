#-------------------------------------------------------------------------------
# INTPROG COURSEWORK
# Alan Jones
# 762633
#-------------------------------------------------------------------------------
from graphics import *
import math

def main():
    gridSize, colourList = getInputs()
    patternPatch, numOfPatterns, patchList, objectList, window = (
                                            drawPatchGrid(gridSize, colourList))
    swapPatches(window, patternPatch, objectList, numOfPatterns, patchList)
    
def getInputs():
    gridError = True
    validColours = ["blue", "red", "green", "orange", "magenta", "cyan"]
    sizes = ["5", "7", "9"]
    colourList = []
    while gridError == True:
        gridInput = input("Enter the size of grid (5, 7, 9): ")
        if gridInput in sizes:
            gridError = False
            gridSize = eval(gridInput)
        else:
            print("Please try again")
    for place in ["first", "second", "third"]:
        colour = input("Enter the {0} colour: ".format(place)).lower()
        while colour not in validColours or colour in colourList:
            print("Please try again")
            colour = input("Enter the {0} colour: ".format(place)).lower()
        colourList.append(colour)
    return gridSize, colourList

def drawPatchGrid(gridSize, colourList):
    window = GraphWin("Patch", gridSize * 100, gridSize * 100)
    x, y, count = 0, 0, 0
    patchList, patternPatch, objectList = [], [], []
    numOfPatterns = gridSize ** 2
    while count != numOfPatterns:
        for colour in colourList:
            count = count + 1
            xyIndex = str(x + 100) + str(y + 100)
            if count > gridSize and x >= 200:
                objectList = drawPatch2(window, x, y, colour, objectList)
                #lists for extension task
                patternPatch.append(xyIndex)
                patternPatch.append(objectList)
                x = x + 100
            else:
                objectList = drawPatch1(window, x, y, colour, objectList)
                #lists for extension task
                patternPatch.append(xyIndex)
                patternPatch.append(objectList)
                x = x + 100
            if count % gridSize == 0:
                y = y + 100
                x = 0
            if count == numOfPatterns:
                break

    return patternPatch, numOfPatterns, patchList, objectList, window
    
#Extension Task
def swapPatches(window, patternPatch, objectList, numOfPatterns, patchList):
    patchList.append(patternPatch)
    while True:
        mouseClick1 = window.getMouse()
        mouseClick2 = window.getMouse()
        mouseX1, mouseY1 = mouseClick1.getX(), mouseClick1.getY()
        mouseX2, mouseY2 = mouseClick2.getX(), mouseClick2.getY()
        mouseCheck1, mouseCheck2 = False, False
        #While loop to allow for swapping of lower numbered items in list
        if mouseX1 != mouseX2 and mouseY1 != mouseY2:
            while mouseCheck2 == False:
                for item in range(0, numOfPatterns * 2, 2):
                    x1 = int(patchList[0][item][0:3])
                    y1 = int(patchList[0][item][3:6])
                    x2, y2 = x1 - 100, y1 - 100
                    #Checks which patch the first click is within
                    if mouseX1 <= x1 and mouseX1 >= x2 and mouseY1 <= y1 and(
                       mouseY1 >= y2 and mouseCheck1 == False):
                            tempItem = item
                            tempX, tempY = x2, y2
                            mouseCheck1 = True
                    #Checks which patch the second click is within
                    elif mouseX2 <= x1 and mouseX2 >= x2 and mouseY2 <= y1 and(
                         mouseY2 >= y2 and mouseCheck1 == True):
                            #Moves patches by the distance they are from each other
                            length1 = len(patchList[0][item + 1])
                            length2 = len(patchList[0][tempItem + 1])
                            distanceX, distanceY = distanceWayBetweenPoints(x2, y2, tempX, tempY)
                            for i in range (length1):
                                patchList[0][item + 1][i].move(distanceX, distanceY)
                            for i in range(length2):
                                patchList[0][tempItem + 1][i].move(-distanceX, -distanceY)
                            #Switches list places
                            patchList[0][tempItem], patchList[0][item] = (
                                     patchList[0][item], patchList[0][tempItem])
                            mouseCheck1, mouseCheck2 = False, True
                            break
                        
def distanceWayBetweenPoints(x2, y2, tempX, tempY):
    distanceX = tempX - x2
    distanceY = tempY - y2
    return distanceX, distanceY        
                        
#Draws the curved line illusion pattern
def drawPatch1(win, x, y, colour, objectList):
    objectList = []
    for i in range(1, 101, 10):
        line = Line(Point(i + x, 0 + y), Point(100 + x, i + y))
        line.setFill(colour.lower())
        line.draw(win)
        objectList.append(line)
        line = Line(Point(0 + x, i + y), Point(i + x, 100 + y))
        line.setFill(colour.lower())
        line.draw(win)
        objectList.append(line)
    return objectList
        
#Draws the 9x9 larger combination of the red and white circles
def drawPatch2(win, x, y, colour, objectList):
    objectList = []
    x = x + 5
    y = y - 4
    radius = 5
    #Works out spacing between each circles using current radius
    distanceBetweenCircles = radius * 7
    temp = x
    for i in range(1, 10):
        objectList = drawCirclePattern(win, x, y, colour, radius, objectList)
        x = x + distanceBetweenCircles
        #Checks if a new row should be created
        if i % 3 == 0:
            y = y + distanceBetweenCircles
            x = temp
    return objectList
            
# Draws the initial 9x9 smaller red and white circle pattern
def drawCirclePattern(win, x, y, colour, radius, objectList):
    centre = Point(x, y)
    for i in range(9):
        if i == 4 :
            currentColour = "white"
        else:
            currentColour = colour
        #Checks if a new row should be created
        if i % 3 == 0:
            centre = Point(x, centre.getY() + radius * 2)
        objectList = drawCircle(win, centre, radius, currentColour, objectList)
        centre = Point(centre.getX() + radius * 2, centre.getY())
    return objectList

def drawCircle(win, centre, radius, colour, objectList):
    circle = Circle(centre, radius)
    circle.setFill(colour)
    circle.draw(win)
    objectList.append(circle)
    return objectList
    
main()