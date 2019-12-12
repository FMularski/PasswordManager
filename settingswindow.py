from window import Window
from startwindow import StartWindow
from tkinter import messagebox
import tkinter as tk


class SettingsWindow(Window):
    def __init__(self, dbm, mailm, user, main_window):
        super().__init__(dbm, mailm)
        self.user = user
        self.mainWindow = main_window

        self.settingsLabel = tk.Label(self.root, text='Settings', bg=self.bg_color, font=10)
        self.backBtn = tk.Button(self.root, text='<< Back', bg='#dedcd1', command=self.back_to_main)
        self.logoutBtn = tk.Button(self.root, text='Log out', bg='pink', command=self.log_out)
        self.place_widgets()

    def place_widgets(self):
        self.settingsLabel.place(relx=0, rely=0)
        self.backBtn.place(relx=0.9, rely=0.85)
        self.logoutBtn.place(relx=0, rely=0.05)

    def back_to_main(self):
        self.root.destroy()
        main_window = self.mainWindow.__init__(self.dbm, self.mailm, self.user)

    def log_out(self):
        if messagebox.askokcancel('Log out', 'Are you sure you want to log out?'):
            self.root.destroy()
            start_window = StartWindow(self.dbm, self.mailm)
            start_window.root.mainloop()

            # TODO: figure out why statring window does not pop out after 2nd logging in

