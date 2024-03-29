import tkinter as tk
import pyautogui as pag


class Window:
    def __init__(self, language):
        self.language = language
        self.windowWidth, self.windowHeight = pag.size()
        self.user = None

        self.root = tk.Tk()
        self.root.title('Password Manager')

        self.setLanguage = tk.StringVar(self.root)
        self.setLanguage.set(self.language)

        self.bg_color = '#fff8ad'

        self.canvas = tk.Canvas(self.root, width=self.windowWidth / 2, height=self.windowHeight / 2, bg=self.bg_color)
        self.canvas.pack()
        self.titleLabel = tk.Label(self.root, text="Password Manager v1.0")
        self.titleLabel.pack()

    @classmethod
    def delete_entries(cls, *entries):
        for entry in entries:
            entry.delete(0, 'end')

    @classmethod
    def close_top_level(cls, top, to_disable):
        for button in to_disable:
            button.config(state='normal')
        top.destroy()

    @classmethod
    def clear_widgets(cls, widgets):
        for widget in widgets:
            widget.destroy()
