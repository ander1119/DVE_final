import cv2
import numpy as np 

def boundedPoint(selectedPoints):
    selectedPoints = np.array(selectedPoints)
    lineVecs = selectedPoints[1:] - selectedPoints[:-1]
    lineLengths = (lineVecs[:, 0]**2 + lineVecs[:, 1]**2) ** (1/2)
    newPoints = []
    for p, v, l in zip(selectedPoints[:-1], lineVecs, lineLengths):
        tmp = np.array([i for i in range(int(l))] / l) * np.array(v) + np.array(p)
        print(tmp)
        newPoints += [i for i in range(int(l))] / l * v + p
    newPoints += [selectedPoints[-1]]
    return newPoints 

def blend(selectedPoints, srcImg, dstImg):
    selectedPoints = boundedPoint(selectedPoints)
    polygonMask = cv2.fillPoly(np.zeros_like(srcImg), selectedPoints, (255, 255, 255))
    r, c = np.where(polygonMask == (255, 255, 255))

    roiMat = polygonMask[(r, c)] # N x 1 matrix
    boundMat = np.array(selectedPoints) # M x 1 matrix
    MVC = np.zeros((len(r), len(selectedPoints)), dtype=float)

    vecMat = roiMat - boundMat[np.newaxis:]

if __name__ == "__main__":
    selectedPoints = [[187, 738], [91, 533], [90, 224], [143, 104], [317, 4], [521, 93], [592, 303], [553, 544], [407, 771], [271, 770], [187, 738]]
    srcImg = cv2.imread("./image/style1.png")
    dstImg = cv2.imread("./image/style2.png")
    blend(selectedPoints, srcImg, dstImg)
    




        