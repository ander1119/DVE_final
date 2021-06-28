import cv2
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import Notebook
from PIL import Image, ImageTk
from mvc import * 

class popUpWindow(tk.Toplevel):
    def __init__(self, parent, srcFileName, targetFileName, selectedPoints):
        super().__init__(parent)
        self.title("drag the object to where you want")
        self.sourceImage = cv2.imread(srcFileName)
        self.targetImage = cv2.imread(targetFileName)
        self.selectedPoints = np.array(selectedPoints[:-1])
        
        self.displayImage = self.targetImage
        self.canvasImage = ImageTk.PhotoImage(image=Image.fromarray(self.displayImage[:,:,::-1]))
        self.canvas = tk.Canvas(self, height=self.canvasImage.height(), width=self.canvasImage.width())
        self.canvas.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        self.canvas.create_image(0,0, anchor='nw', image=self.canvasImage)

        self.saveButton = tk.Button(self, text='save edited image', command=self.saveImage)
        self.saveButton.grid(row=1, column=0)

        # print(self.selectedPoints)
        self.m = triangulate(self.selectedPoints)
        self.points = self.m.p.astype(int)
        self.triangles = self.m.t.transpose()
        print(f'There are {self.m.p.shape[1]} verticies')
        print(f'There are {self.m.t.shape[1]} tringular')
        print(self.sourceImage.shape)
        print(self.targetImage.shape)
        self.row, self.col = self.points[1], self.points[0]
        self.roiPosMat = np.column_stack((self.row, self.col)) # K x 1 matrix
        self.boundMat = np.array(self.selectedPoints)

        self.MVC = mvcCompute(self.roiPosMat, self.boundMat)

        self.srcCenter = np.array([int(self.selectedPoints[:,1].mean()), int(self.selectedPoints[:,0].mean())])
        self.dstCenter = np.array([self.targetImage.shape[0] // 2, self.targetImage.shape[1] // 2])
        self.offset = self.dstCenter - self.srcCenter
        self.dstSelectedPoints = self.selectedPoints + self.offset[::-1]
        if not self.outOfImage(self.dstSelectedPoints, self.targetImage):
            self.displayImage = blendOptimized(self.boundMat ,self.selectedPoints, self.offset, self.sourceImage, self.targetImage, self.points, self.triangles, self.MVC)
            self.updateCanvas()
        else:
            
            messagebox.showinfo("Warning !!", "selected region out of image")

        self.canvas.bind("<ButtonPress-1>", self.Click)
        self.canvas.bind("<ButtonRelease-1>", self.Release) 
        self.x = None
        self.y = None

    def Click(self, event):
        self.x = event.x
        self.y = event.y
        print("clicked at ", self.x, self.y)

    def Release(self, event):
        dstCenter = self.dstCenter + np.array([event.y - self.y, event.x - self.x])
        # print(self.dstCenter)
        offset = dstCenter - self.srcCenter
        dstSelectedPoints = self.selectedPoints + offset[::-1]
        if not self.outOfImage(dstSelectedPoints, self.targetImage):
            self.dstCenter = dstCenter
            self.offset = offset
            self.dstSelectedPoints = dstSelectedPoints
            self.displayImage = blendOptimized(self.boundMat ,self.selectedPoints, self.offset, self.sourceImage, self.targetImage, self.points, self.triangles, self.MVC)
            self.updateCanvas()
        else:
            messagebox.showinfo("Warning !!", "selected region out of image")
        self.x = None
        self.y = None

    def saveImage(self):
        saveFile = filedialog.asksaveasfilename(filetypes=[('Portable Network Graphics', '*.png')])
        cv2.imwrite(saveFile, self.displayImage)

    def outOfImage(self, dstSelectedPoints, targetImage):
        print("dstSelectedPoint", dstSelectedPoints)
        for px, py in dstSelectedPoints:
            if px < 0 or px >= targetImage.shape[1] or py < 0 or py >= targetImage.shape[0]:
                return True 
        return False

    def updateCanvas(self):
        self.canvasImage = ImageTk.PhotoImage(image=Image.fromarray(self.displayImage[:,:,::-1]))
        self.canvas = tk.Canvas(self, height=self.canvasImage.height(), width=self.canvasImage.width())
        self.canvas.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        self.canvas.create_image(0,0, anchor='nw', image=self.canvasImage)
        self.canvas.bind("<ButtonPress-1>", self.Click)
        self.canvas.bind("<ButtonRelease-1>", self.Release) 