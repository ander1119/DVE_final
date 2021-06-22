import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import Notebook
from PIL import Image, ImageTk, ImageGrab
from subWindow import *

class mainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Image-Cloning Editor")
        # self.grid_propagate()
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.imageButton = tk.Button(self, text='Open Image', command=self.openImage)
        self.imageButton.grid(row=0, column=0)
        self.tab = Notebook(self)
        # self.tab.grid_propagate()
        self.tab.grid(row=1, column=0, sticky=tk.N+tk.W+tk.E+tk.S)

    def openImage(self):
        fileName = filedialog.askopenfilename(parent=self, initialdir='./image', title='Choose an image.')
        # image = ImageTk.PhotoImage(Image.open(fileName))
        # self.geometry("{}x{}".format(image.width(), image.height()))
        newTab = subWindow(self.tab, fileName)
        self.tab.add(newTab, text=fileName.split("/")[-1])

        