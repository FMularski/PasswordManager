import tkinter as tk
import pyautogui as pag


class Window:
    def __init__(self, db_manager):
        self.windowWidth, self.windowHeight = pag.size()
        self.dbm = db_manager

        self.root = tk.Tk()
        self.root.title('Password Manager')

        self.bg_color = '#fff8ad'

        self.canvas = tk.Canvas(self.root, width=self.windowWidth / 2, height=self.windowHeight / 2, bg=self.bg_color)
        self.canvas.pack()
        self.titleLabel = tk.Label(self.root, text="Password Manager v1.0")
        self.titleLabel.pack()

    def run(self):
        self.root.mainloop()
