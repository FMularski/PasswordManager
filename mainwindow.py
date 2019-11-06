from window import Window
import tkinter as tk


class MainWindow(Window):
    def __init__(self, dbm, mailm, user):
        super().__init__(dbm, mailm)
        self.user = user

        self.userInfoLabel = tk.Label(self.root, text=f'Logged in as {user["login"]}', bg=self.bg_color)

        self.place_widgets()

    def place_widgets(self):
        self.userInfoLabel.place(relx=0, rely=0)