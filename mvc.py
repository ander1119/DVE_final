import cv2
import numpy as np 

def boundedPoint(selectedPoints):
    lineVecs = selectedPoints[1:] - selectedPoints[:-2]
    lineLengths = (lineVecs[:, 0]**2 + lineVecs[:, 1]**2) ** (1/2)
    newPoints = []
    for p, v, l in zip(selectedPoints[:-2], lineVecs, lineLengths):
        newPoints += [i in range(int(l))] / l * v + p
    newPoints += [selectedPoints[-1]]
    return newPoints 

def blend(selectedPoints, srcImg, dstImg):
    selectedPoints = boundedPoint(selectedPoints)
    polygonMask = cv2.fillPoly(np.zeros_like(srcImg), selectedPoints, (255, 255, 255))
    r, c = np.where(polygonMask == (255, 255, 255))

    roiMat = polygonMask[(r, c)] # N x 1 matrix
    boundMat = np.array(selectedPoints) # M x 1 matrix
    MVC = np.zeros((len(r), len(selectedPoints)), dtype=float)

    




        