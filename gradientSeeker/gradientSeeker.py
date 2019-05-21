import cv2
import numpy as np
import math
from statistics import mean
import sys

def retrieveDiagonals(matrix):

    topLeft = []
    topRight = []
    bottomLeft = []
    bottomRight = []

    height, width = len(pixelMatrix), len(pixelMatrix[0])

    # Iterate for top-left
    for y in range(0, height/2):
        for x in range(0, width/2):
            topLeft.append(pixelMatrix[y][x])

    # Iterate for bottom-left
    for y in range(height/2, height):
        for x in range(0, width/2):
            bottomLeft.append(pixelMatrix[y][x])
    
     # Iterate for top-right
    for y in range(0, height/2):
        for x in range(width/2, width):
            topRight.append(pixelMatrix[y][x])

    # Iterate for bottom-right
    for y in range(height/2, height):
        for x in range(width/2, width):
            bottomRight.append(pixelMatrix[y][x])

    return [topLeft, topRight, bottomLeft, bottomRight]

def linearRegressionGradient(diagonals):
    gradients = []
    for diagonal in diagonals:
        xs = np.array(range(0, len(diagonal)), dtype=np.float64)
        if len(diagonal) > 0:
            ys = np.array(diagonal, dtype=np.float64)
            gradient = abs((((mean(xs)*mean(ys)) - mean(xs*ys)) / ((mean(xs)**2) - mean(xs**2))))
            gradients.append(gradient)
    return gradients

def reshapedMatrixCoordinates(matrix, quadrantNumber):

    h = len(matrix)
    w = len(matrix[0])

    # Top left
    if quadrantNumber == 0:
        pixelMatrix = [[0 for x in range(0, w/2)] for x in range(0, h/2)]
        for indexHeight, i in enumerate(range(0, h/2)):
            for indexWidth, j in enumerate(range(0, w/2)):
                pixelMatrix[indexHeight][indexWidth] = matrix[i][j]

    # Bottom left
    if quadrantNumber == 1:
        pixelMatrix = [[0 for x in range(0, w/2)] for x in range(h/2, h)]
        for indexHeight, i in enumerate(range(h/2, h)):
            for indexWidth, j in enumerate(range(0, w/2)):
                pixelMatrix[indexHeight][indexWidth] = matrix[i][j]
    
    # Top right
    if quadrantNumber == 2:
        pixelMatrix = [[0 for x in range(w/2, w)] for x in range(0, h/2)]
        for indexHeight, i in enumerate(range(0, h/2)):
            for indexWidth, j in enumerate(range(w/2, w)):
                pixelMatrix[indexHeight][indexWidth] = matrix[i][j]

    # Bottom right
    if quadrantNumber == 3:
        pixelMatrix = [[0 for x in range(w/2, w)] for x in range(h/2, h)]        
        for indexHeight, i in enumerate(range(h/2, h)):
            for indexWidth, j in enumerate(range(w/2, w)):
                pixelMatrix[indexHeight][indexWidth] = matrix[i][j]

    return pixelMatrix
    
def showBestQuadrant(greyImage, lowestGradientIndex, boundaryCoordinates):
    newBoundaryCoordinates = {}

    # Top left
    if lowestGradientIndex == 0:
        startCoord = boundaryCoordinates['leftTopCorner']
        endCoord = boundaryCoordinates['rightBottomCorner']
        cv2.rectangle(greyImage, (startCoord[0], startCoord[1]), (endCoord[0], endCoord[1]), (0,0,255),2)
        newBoundaryCoordinates = generateNewBoundaryCoordinates(boundaryCoordinates, 0)
        
    # Bottom left
    elif lowestGradientIndex == 1:
        startCoord = boundaryCoordinates['leftBottomCorner']
        endCoord = [boundaryCoordinates['leftBottomCorner'][0] + (boundaryCoordinates['rightBottomCorner'][0] - boundaryCoordinates['leftBottomCorner'][0]), boundaryCoordinates['leftBottomCorner'][1] + (boundaryCoordinates['rightBottomCorner'][1] - boundaryCoordinates['leftTopCorner'][1])]
        cv2.rectangle(greyImage, (startCoord[0], startCoord[1]), (endCoord[0], endCoord[1]), (0,0,255),2)
        newBoundaryCoordinates = generateNewBoundaryCoordinates(boundaryCoordinates, 1)

    # Top right
    elif lowestGradientIndex == 2:
        startCoord = boundaryCoordinates['rightTopCorner']
        endCoord = [boundaryCoordinates['rightTopCorner'][0] + (boundaryCoordinates['rightTopCorner'][0] - boundaryCoordinates['leftTopCorner'][0]),  boundaryCoordinates['rightTopCorner'][1] + (boundaryCoordinates['rightBottomCorner'][1] - boundaryCoordinates['rightTopCorner'][1])]
        cv2.rectangle(greyImage, (startCoord[0], startCoord[1]), (endCoord[0], endCoord[1]), (0,0,255),2)
        newBoundaryCoordinates = generateNewBoundaryCoordinates(boundaryCoordinates, 2)

    # Bottom right
    elif lowestGradientIndex == 3:
        startCoord = (boundaryCoordinates['rightBottomCorner'])
        endCoord = [boundaryCoordinates['rightTopCorner'][0] * 2, boundaryCoordinates['rightBottomCorner'][1] + (boundaryCoordinates['rightBottomCorner'][1] - boundaryCoordinates['rightTopCorner'][1])]
        cv2.rectangle(greyImage, (startCoord[0], startCoord[1]), (endCoord[0], endCoord[1]), (0,0,255),2)
        newBoundaryCoordinates = generateNewBoundaryCoordinates(boundaryCoordinates, 3)

    print("OLD_CORDS:")
    print(boundaryCoordinates)
    print("QUAD: " + str(lowestGradientIndex) + " NEW_CORDS:")
    print(newBoundaryCoordinates)
    print("********************")

    return [greyImage, newBoundaryCoordinates]

def generateNewBoundaryCoordinates(oldBoundaryCoordinates, quadrantNumber):

    data = {}
    quad = ""

    # Top left
    if quadrantNumber == 0:
        data['leftTopCorner'] = [oldBoundaryCoordinates["leftTopCorner"][0], oldBoundaryCoordinates["leftTopCorner"][1]]
        data['leftBottomCorner'] = [oldBoundaryCoordinates["leftTopCorner"][0], (oldBoundaryCoordinates["leftTopCorner"][1] + ((oldBoundaryCoordinates["leftBottomCorner"][1] - oldBoundaryCoordinates["leftTopCorner"][1])/2))]
        data['rightTopCorner'] = [oldBoundaryCoordinates["leftTopCorner"][0] + ((oldBoundaryCoordinates["rightTopCorner"][0] - oldBoundaryCoordinates["leftTopCorner"][0])/2), oldBoundaryCoordinates["leftTopCorner"][1]]
        data['rightBottomCorner'] = [oldBoundaryCoordinates["leftTopCorner"][0] + ((oldBoundaryCoordinates["rightTopCorner"][0] - oldBoundaryCoordinates["leftTopCorner"][0])/2), (oldBoundaryCoordinates["leftTopCorner"][1] + ((oldBoundaryCoordinates["leftBottomCorner"][1] - oldBoundaryCoordinates["leftTopCorner"][1])/2))]
        return data

    # Bottom left
    if quadrantNumber == 1:
        data['leftTopCorner'] = [oldBoundaryCoordinates["leftBottomCorner"][0], oldBoundaryCoordinates["leftBottomCorner"][1]]
        data['leftBottomCorner'] = [oldBoundaryCoordinates["leftBottomCorner"][0], oldBoundaryCoordinates["leftBottomCorner"][1] + (oldBoundaryCoordinates["leftBottomCorner"][1] - oldBoundaryCoordinates["leftTopCorner"][1])/2]
        data['rightTopCorner'] = [oldBoundaryCoordinates["leftBottomCorner"][0] + (oldBoundaryCoordinates["rightBottomCorner"][0] - oldBoundaryCoordinates["leftBottomCorner"][0])/2, oldBoundaryCoordinates["leftBottomCorner"][1]]
        data["rightBottomCorner"] = [oldBoundaryCoordinates["leftBottomCorner"][0] + (oldBoundaryCoordinates["rightBottomCorner"][0] - oldBoundaryCoordinates["leftBottomCorner"][0])/2, oldBoundaryCoordinates["leftBottomCorner"][1] + (oldBoundaryCoordinates["leftBottomCorner"][1] - oldBoundaryCoordinates["leftTopCorner"][1])/2]
        return data
 

    # Top right
    if quadrantNumber == 2:
        data['leftTopCorner'] = [oldBoundaryCoordinates["rightTopCorner"][0], oldBoundaryCoordinates["rightTopCorner"][1]]
        data['leftBottomCorner'] = [oldBoundaryCoordinates["rightTopCorner"][0], oldBoundaryCoordinates["rightTopCorner"][1] + ((oldBoundaryCoordinates["rightBottomCorner"][1] - oldBoundaryCoordinates["rightTopCorner"][1])/2)]
        data["rightTopCorner"] = [oldBoundaryCoordinates["rightTopCorner"][0] + ((oldBoundaryCoordinates["rightTopCorner"][0] - oldBoundaryCoordinates["leftTopCorner"][0])/2), oldBoundaryCoordinates["rightTopCorner"][1]]
        data["rightBottomCorner"] = [oldBoundaryCoordinates["rightTopCorner"][0] + ((oldBoundaryCoordinates["rightTopCorner"][0] - oldBoundaryCoordinates["leftTopCorner"][0])/2), oldBoundaryCoordinates["rightTopCorner"][1] + ((oldBoundaryCoordinates["rightBottomCorner"][1] - oldBoundaryCoordinates["rightTopCorner"][1])/2)]
        return data

    # Bottom right
    elif quadrantNumber == 3:
        data['leftTopCorner'] = [oldBoundaryCoordinates["rightBottomCorner"][0], oldBoundaryCoordinates["rightBottomCorner"][1]]
        data['leftBottomCorner'] = [oldBoundaryCoordinates["rightBottomCorner"][0], oldBoundaryCoordinates["rightBottomCorner"][1] + (oldBoundaryCoordinates["rightBottomCorner"][1] - oldBoundaryCoordinates["rightTopCorner"][1])/2]
        data['rightTopCorner'] = [oldBoundaryCoordinates["rightBottomCorner"][0] + (oldBoundaryCoordinates["rightBottomCorner"][0]/2), oldBoundaryCoordinates["rightBottomCorner"][1]]
        data['rightBottomCorner'] = [oldBoundaryCoordinates["rightBottomCorner"][0] + (oldBoundaryCoordinates["rightBottomCorner"][0]/2), oldBoundaryCoordinates["rightBottomCorner"][1] + (oldBoundaryCoordinates["rightBottomCorner"][1] - oldBoundaryCoordinates["rightTopCorner"][1])/2]
        return data


''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''                                                  '''
'''                      START                       '''
'''                                                  '''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''
imageName = str(sys.argv[1])

# Receive image the convert to greyscale
originalImage = cv2.imread(imageName)
greyscaleImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
greyscaleBoxImage = cv2.cvtColor(greyscaleImage,cv2.COLOR_GRAY2RGB)

# Create a 2d array that's mapped to each pixel value from the image. 
columnCount = greyscaleBoxImage.shape[1]
rowCount = greyscaleBoxImage.shape[0]
pixelMatrix = [[0 for x in range(columnCount)] for x in range(rowCount)]
for i in range(len(pixelMatrix)):
    for j in range(len(pixelMatrix[i])):
        pixelMatrix[i][j] = greyscaleBoxImage[i][j][0]

# Find the width, height and area of the matrix
width, height = len(pixelMatrix[0]), len(pixelMatrix)

# Centre new square in matrix
boundaryCoordinates = {}
boundaryCoordinates['leftTopCorner'] = [0, 0]
boundaryCoordinates['leftBottomCorner'] = [0, height/2]
boundaryCoordinates['rightTopCorner'] = [width/2, 0]
boundaryCoordinates['rightBottomCorner'] = [width/2, height/2]

for x in xrange(5):
    diagonals = retrieveDiagonals(pixelMatrix)
    gradients = linearRegressionGradient(diagonals)
    lowestGradientIndex = gradients.index(min(gradients))
    imageResult = showBestQuadrant(greyscaleBoxImage, lowestGradientIndex, boundaryCoordinates)
    pixelMatrix = reshapedMatrixCoordinates(pixelMatrix, lowestGradientIndex)
    boundaryCoordinates = imageResult[1]


# Present image
cv2.imshow('Landing zone', imageResult[0])
cv2.waitKey(0)
cv2.destroyAllWindows()

