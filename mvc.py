import cv2
import numpy as np 
import matplotlib.pyplot as plt

def boundedPoint(selectedPoints):
    lineVecs = selectedPoints[1:] - selectedPoints[:-1]
    lineLengths = (lineVecs[:, 0]**2 + lineVecs[:, 1]**2) ** (1/2)
    newPoints = []
    for p, v, l in zip(selectedPoints[:-1], lineVecs, lineLengths):
        tmp = [list(np.array(i / l * v + p, int)) for i in range(int(l))]
        # print(tmp)
        newPoints += tmp
    newPoints += [list(selectedPoints[-1])]
    # print(newPoints)
    return np.array(newPoints) 

def blend(selectedPoints, srcImg, dstImg):
    selectedPoints = np.array(selectedPoints)
    selectedPoints = boundedPoint(selectedPoints)
    polygonMask = np.zeros_like(srcImg)
    cv2.fillPoly(polygonMask, [selectedPoints], (255, 255, 255))
    r, c = np.where(np.all(polygonMask == (255, 255, 255), axis=-1))

    roiValueMat = srcImg[(r, c)] 
    roiPosMat = np.column_stack((r, c)) # N x 1 matrix
    boundMat = np.array(selectedPoints) # M x 1 matrix

    vec1 = boundMat[:-1, np.newaxis,:] - roiPosMat[np.newaxis,:,:]
    vec2 = boundMat[1:, np.newaxis,:] - roiPosMat[np.newaxis,:,:]

    print(vec1.shape)

    offset = np.array([(dstImg.shape[0] - srcImg.shape[0]) // 2, (dstImg.shape[1] - srcImg.shape[1]) // 2])

    # difference between target image and source image
    # diff.shape = (M, 3)
    diff = dstImg[boundMat[:,0] + offset[0],boundMat[:,1] + offset[1],:] - srcImg[boundMat[:,0],boundMat[:,1],:]

    transferedSelectedPoints = boundedPoint(selectedPoints + offset)
    polygonMask = np.zeros_like(dstImg)
    cv2.fillPoly(polygonMask, [transferedSelectedPoints], (255, 255, 255))

    r = np.zeros_like(dstImg)
    for i in range(len(boundMat)):
        r += diff[i] * MVC[i]

    return dstImg * (1 - polygonMask) + polygonMask * (srcImg + r)

if __name__ == "__main__":
    selectedPoints = [[187, 738], [91, 533], [90, 224], [143, 104], [317, 4], [521, 93], [592, 303], [553, 544], [407, 771], [271, 770], [187, 738]]
    srcImg = cv2.imread("./image/style1.png")
    dstImg = cv2.imread("./image/style2.png")
    print('src:', srcImg.shape, 'dst:', dstImg.shape)
    blend(selectedPoints, srcImg, dstImg)
    




        