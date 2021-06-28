import cv2
import numpy as np 
import matplotlib.pyplot as plt
from tqdm import tqdm

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
    row, col = np.where(np.all(polygonMask == (255, 255, 255), axis=-1))

    roiValueMat = srcImg[(row, col)]
    roiPosMat = np.column_stack((row, col)) # N x 1 matrix
    boundMat = np.array(selectedPoints) # M x 1 matrix
    M = len(boundMat)
    N = len(roiPosMat)
    print(f'M={M}, N={N}')

    # M = np.expand_dims(roiPosMat, axis=1) - boundMat[:,:]

    # MVC.shape = (N, M-1)
    MVC = np.zeros((roiPosMat.shape[0], boundMat.shape[0]-1))
    for i, pos in enumerate(tqdm(roiPosMat)):
        vec = boundMat - pos
        v1, v2 = vec[:-1], vec[1:]
        cosAng = (v1[:,0] * v2[:,0] + v1[:,1] * v2[:,1]) / (v1[:,0]**2+v1[:,1]**2)**(1/2) / (v2[:,0]**2+v2[:,1]**2)**(1/2)
        ang = np.nan_to_num(np.arccos(cosAng))
        tanHalfAng = np.tan(ang/2)
        tanHalfAng = np.append(tanHalfAng, [tanHalfAng[-1]])

        w_numerator = tanHalfAng[1:] + tanHalfAng[:-1]
        w_denominator = (v1[:,0]**2 + v1[:,1]**2) ** (1/2)

        MVC[i] = np.nan_to_num(w_numerator / w_denominator)
        MVC[i] = MVC[i] / MVC[i].sum()

    offset = np.array([(dstImg.shape[0] - srcImg.shape[0]) // 2, (dstImg.shape[1] - srcImg.shape[1]) // 2])
    print(f'offset: {offset}')

    # diff.shape = (M, 3)
    diff = dstImg[boundMat[:-1,1] + offset[0],boundMat[:-1,0] + offset[1]].astype(np.float32) - srcImg[boundMat[:-1,1],boundMat[:-1,0]].astype(np.float32)

    r = MVC @ diff
    
    dstImg[row+offset[0], col+offset[1]] = np.minimum(np.maximum(roiValueMat + r, 0), 255)
    return dstImg

if __name__ == "__main__":
    selectedPoints = [[187, 738], [91, 533], [90, 224], [143, 104], [317, 4], [521, 93], [592, 303], [553, 544], [407, 771], [271, 770], [187, 738]]
    srcImg = cv2.imread("./image/style1.png")
    dstImg = cv2.imread("./image/style2.png")
    print('src:', srcImg.shape, 'dst:', dstImg.shape)
    ret = blend(selectedPoints, srcImg, dstImg)
    cv2.imwrite("image/result.png", ret)
    # plt.imshow(ret)
    # plt.show()
        