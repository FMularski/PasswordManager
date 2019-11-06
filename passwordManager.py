import tkinter as tk
from tkinter import messagebox
import pyautogui as pag
import sqlite3

### DB SETUP ###

try:
    conn = sqlite3.connect('passmanager.db')

    createTableUsersQuery = """
    CREATE TABLE IF NOT EXISTS Users(
    id integer PRIMARY KEY AUTOINCREMENT,
    login text NOT NULL,
    password text NOT NULL
    );"""

    createTableAccountsQuery = """
        CREATE TABLE IF NOT EXISTS Accounts(
        id integer PRIMARY KEY,
        name text NOT NULL,
        login text NOT NULL,
        password text NOT NULL,
        user_id integer NOT NULL,
        FOREIGN KEY (user_id) REFERENCES Users(id)
        );"""

    conn.execute(createTableUsersQuery)
    conn.execute(createTableAccountsQuery)
except sqlite3.Error as e:
    messagebox.showerror('Error', e)


### METHODS ###
def register(login, password, password_confirm, entries):

    if '' in (login, password, password_confirm):
        messagebox.showerror('Error', 'Please fill all entries.')
        return

    cursor = conn.cursor()
    cursor.execute('SELECT login FROM Users')

    login_in_db = list()    # making [login1, login2, ...] from [(login1,), (login2,), ...]
    for log_in_db_list in cursor.fetchall():
        login_in_db.append(log_in_db_list[0])

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

    try:
        insert_query = f'INSERT INTO Users (login, password) VALUES(?, ?)'
        conn.execute(insert_query, (login, password))
        conn.commit()

        for entry in entries:
            entry.delete(0, 'end')

        messagebox.showinfo('Success', f'User {login} has been successfully created.')

    except sqlite3.Error as e:
        messagebox.showerror('Error', e)


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

