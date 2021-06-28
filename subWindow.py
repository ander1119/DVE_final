import cv2
import tkinter as tk
import numpy as np
import multiprocessing

from queue import Queue
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import Notebook
from PIL import Image, ImageTk, ImageGrab
from popUpWindow import *
from mvc import *

class subWindow(tk.Frame):
    def __init__(self, parent, fileName):
        super().__init__(parent)
        # self.grid_propagate(True)
        self.selectButton = tk.Button(self, text='Select Region', command=self.select)
        self.selectButton.grid(row=1, column=0)
        self.cloningButton = tk.Button(self, text='clone', command=self.cloning)
        self.cloningButton.grid(row=1, column=1)

        # self.grid_columnconfigure(0, weight=1)
        # self.grid_columnconfigure(1, weight=1)
        # self.grid_columnconfigure(2, weight=1)
        # self.grid_rowconfigure(2, weight=1)
        self.fileName = fileName
        self.imageCv = cv2.imread(self.fileName)
        self.image = ImageTk.PhotoImage(Image.open(fileName))
        self.canvas = tk.Canvas(self, height=self.image.height(), width=self.image.width())
        self.canvas.grid(row=0, column=0, columnspan=2, sticky=tk.N+tk.S+tk.E+tk.W)
        self.canvas.image = self.image  # <--- keep reference of your image
        self.canvas.create_image(0,0,anchor='nw',image=self.image)

        self.act = None
        self.selectedPoints = None
        self.linesId = None

        self.row = None
        self.col = None
        self.polygonMask = None
        self.roiPosMat = None
        self.boundMat = None


    def select(self):
        def reset(event):  
            self.act = None 
            self.selectedPoints = None
            for l in self.linesId:
                self.canvas.delete(l)
            self.linesId = None

        def Mousedown(event): 
            if self.act is None: 
            # the new line starts where the user clicked 
                x0 = event.x 
                y0 = event.y
                self.selectedPoints = []
                self.linesId = []

            else: 
            # the new line starts at the end of the previously 
            # drawn line 
                coords = event.widget.coords(self.act) 
                x0 = coords[2] 
                y0 = coords[3] 

            # create the new line 
            if len(self.selectedPoints) > 1 and (event.x - self.selectedPoints[0][0])**2 + (event.y - self.selectedPoints[0][1])**2 <= 100:
                self.selectedPoints.append([self.selectedPoints[0][0], self.selectedPoints[0][1]])
                self.act = event.widget.create_line(x0, y0, self.selectedPoints[0][0], self.selectedPoints[0][1], fill="red", dash=(4, 4), width=3)
                self.linesId.append(self.act)
                self.canvas.unbind("<ButtonPress-3>") 
                self.canvas.unbind("<Motion>") 
                self.canvas.unbind("<ButtonPress-1>")

                self.selectedPoints = boundedPoint(self.selectedPoints)
                self.polygonMask = np.zeros_like(self.imageCv)
                cv2.fillPoly(self.polygonMask, [self.selectedPoints], (255, 255, 255))
                self.row, self.col = np.where(np.all(self.polygonMask == (255, 255, 255), axis=-1))

                # self.roiValueMat = srcImg[(row, col)]
                self.roiPosMat = np.column_stack((self.row, self.col)) # N x 1 matrix
                self.boundMat = np.array(self.selectedPoints) # M x 1 matrix

            else:
                self.selectedPoints.append([event.x, event.y])
                self.act = event.widget.create_line(x0, y0, event.x, event.y, fill="red", dash=(4, 4), width=3) 
                self.linesId.append(self.act)

        def motion(event): 
            if self.act: 
            # modify the self.act line by changing the end coordinates 
            # to be the self.act mouse position 
                coords = event.widget.coords(self.act) 
                coords[2] = event.x 
                coords[3] = event.y 

                event.widget.coords(self.act, *coords)
        
        # if self.linesId is not None:
        #     for l in self.linesId:
        #         self.canvas.delete(l)
        # self.selectedPoints = None
        # self.linesId = None
        # self.act = None

        self.act = None 
        self.selectedPoints = None
        if self.linesId is not None:
            for l in self.linesId:
                self.canvas.delete(l)
        self.linesId = None

        self.canvas.bind("<ButtonPress-3>", reset) 
        self.canvas.bind("<Motion>", motion) 
        self.canvas.bind("<ButtonPress-1>", Mousedown)

    def cloning(self):
        if self.selectedPoints is None:
            messagebox.showinfo("Warning !!", "You should select region first")
        else:
            targetFileName = filedialog.askopenfilename(parent=self, title='Choose an image to paste clone region')
            newWindow = popUpWindow(self, self.fileName, targetFileName, self.selectedPoints)

            # saveFile = filedialog.asksaveasfilename(filetypes=[('Portable Network Graphics', '*.png')])
            # result_image = cv2.imread(self.fileName)
            # cv2.fillConvexPoly(result_image, np.int32(self.selectedPoints[:-2]), (0, 0, 255))
            # cv2.imwrite(saveFile, result_image)