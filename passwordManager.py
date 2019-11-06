import tkinter as tk
from tkinter import messagebox
import pyautogui as pag
import sqlite3
from dbmanager import DbManager

dbm = DbManager('pass_manager.db')
dbm.setup_db()


def register(login, password, password_confirm, entries):

    if '' in (login, password, password_confirm):
        messagebox.showerror('Error', 'Please fill all entries.')
        return

    login_in_db = dbm.get_column_values('login', 'Users')

    if login in login_in_db:
        messagebox.showerror('Error', 'Entered login is already used.')
        entries[1].delete(0, 'end')
        entries[2].delete(0, 'end')
        return

    if password != password_confirm:
        messagebox.showerror('Error', 'Password and password confirmation don\'t match.')
        entries[1].delete(0, 'end')
        entries[2].delete(0, 'end')
        return

    dbm.insert('Users', 'login, password', (login, password))

    for entry in entries:
        entry.delete(0, 'end')


### GUI ###
windowWidth, windowHeight = pag.size()

root = tk.Tk()
root.title('Password Manager')

bg_color = '#fff8ad'

canvas = tk.Canvas(root, width=windowWidth / 2, height=windowHeight / 2, bg=bg_color)
canvas.pack()
titleLabel = tk.Label(root, text="Password Manager v1.0")
titleLabel.pack()

# log in widgets

logInLabel = tk.Label(root, text="Log In", font="12", bg=bg_color)
logInLabel.place(relx=0.1, rely=0.2)

logLabel = tk.Label(root, text="Login:", bg=bg_color)
logLabel.place(relx=0.1, rely=0.3)

logEntry = tk.Entry(root, width=25)
logEntry.place(relx=0.1, rely=0.35)

passwordLabel = tk.Label(root, text="Password:", bg=bg_color)
passwordLabel.place(relx=0.1, rely=0.4)

passwordEntry = tk.Entry(root, width=25, show='*')
passwordEntry.place(relx=0.1, rely=0.45)


logInBtn = tk.Button(root, text="Log In", bg='white')
logInBtn.place(relx=0.1, rely=0.55)

# registration widgets

regLabel = tk.Label(root, text="Registration", font="12", bg=bg_color)
regLabel.place(relx=0.6, rely=0.2)

regLogLabel = tk.Label(root, text="Login:", bg=bg_color)
regLogLabel.place(relx=0.6, rely=0.3)

regLogEntry = tk.Entry(root, width=25)
regLogEntry.place(relx=0.6, rely=0.35)

regPasswordLabel = tk.Label(root, text="Password:", bg=bg_color)
regPasswordLabel.place(relx=0.6, rely=0.4)

regPasswordEntry = tk.Entry(root, width=25, show='*')
regPasswordEntry.place(relx=0.6, rely=0.45)

regPasswordConfirmLabel = tk.Label(root, text="Confirm Password:", bg=bg_color)
regPasswordConfirmLabel.place(relx=0.6, rely=0.5)

regPasswordConfirmEntry = tk.Entry(root, width=25, show='*')
regPasswordConfirmEntry.place(relx=0.6, rely=0.55)

regBtn = tk.Button(root, text="Register", bg='white', command=lambda: register(regLogEntry.get(),
                                                                               regPasswordEntry.get(),
                                                                               regPasswordConfirmEntry.get(),
                                                                               entries=(regLogEntry, regPasswordEntry,
                                                                               regPasswordConfirmEntry)))
regBtn.place(relx=0.6, rely=0.65)

root.mainloop()

