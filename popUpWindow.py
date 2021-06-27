import cv2
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import Notebook
from PIL import Image, ImageTk
from mvc import * 

class popUpWindow(tk.Toplevel):
    def __init__(self, parent, srcFileName, targetFileName, selected_points):
        super().__init__(parent)
        self.title("drag the object to where you want")
        self.souceImage = cv2.imread(srcFileName)
        self.targetImage = cv2.imread(targetFileName)
        self.selected_points = selected_points
        
        self.displayImage = self.targetImage
        self.canvasImage = ImageTk.PhotoImage(image=Image.fromarray(self.displayImage[:,:,::-1]))
        self.canvas = tk.Canvas(self, height=self.canvasImage.height(), width=self.canvasImage.width())
        self.canvas.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        self.canvas.create_image(0,0, anchor='nw', image=self.canvasImage)

        self.saveButton = tk.Button(self, text='save edited image', command=self.saveImage)
        self.saveButton.grid(row=1, column=0)

        print(selected_points)

    def saveImage(self):
        saveFile = filedialog.asksaveasfilename(filetypes=[('Portable Network Graphics', '*.png')])
        cv2.imwrite(saveFile, self.displayImage)