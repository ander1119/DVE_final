import cv2
import numpy as np 
    

def MVC(boundPoints, polygonMask, srcImg):
    col_arr = np.arange(srcImg.shape[0])
    col_arr = np.transpose(np.tile(col_arr, (srcImg.shape[1], 1)))
    row_arr = np.arange(srcImg.shape[1]).reshape(1, -1)
    row_arr = np.tile(row_arr, (srcImg.shape[0], 1))
    pos = np.stack([col_arr, row_arr], )
    

def boundedPoint(selectedPoints):
    lineVecs = selectedPoints[1:] - selectedPoints[:-2]
    lineLengths = (lineVecs[:, 0]**2 + lineVecs[:, 1]**2) ** (1/2)
    newPoints = []
    for p, v, l in zip(selectedPoints[:-2], lineVecs, lineLengths):
        newPoints += [i in range(int(l))] / l * v + p
    newPoints += [selectedPoints[-1]]
    return newPoints 




        