from window import Window
import tkinter as tk
from tkinter import messagebox


class StartWindow(Window):
    def __init__(self, db_manager):
        super().__init__(db_manager)

        # log in widgets
        self.logInLabel = tk.Label(self.root, text="Log In", font="12", bg=self.bg_color)
        self.logLabel = tk.Label(self.root, text="Login:", bg=self.bg_color)
        self.logEntry = tk.Entry(self.root, width=25)
        self.passwordLabel = tk.Label(self.root, text="Password:", bg=self.bg_color)
        self.passwordEntry = tk.Entry(self.root, width=25, show='*')
        self.logInBtn = tk.Button(self.root, text="Log In", bg='white', command=self.login)

        # registration widgets
        self.regLabel = tk.Label(self.root, text="Registration", font="12", bg=self.bg_color)
        self.regLogLabel = tk.Label(self.root, text="Login:", bg=self.bg_color)
        self.regLogEntry = tk.Entry(self.root, width=25)
        self.regPasswordLabel = tk.Label(self.root, text="Password:", bg=self.bg_color)
        self.regPasswordEntry = tk.Entry(self.root, width=25, show='*')
        self.regPasswordConfirmLabel = tk.Label(self.root, text="Confirm Password:", bg=self.bg_color)
        self.regPasswordConfirmEntry = tk.Entry(self.root, width=25, show='*')
        self.regBtn = tk.Button(self.root, text="Register", bg='white', command=self.register)

        self.place_widgets()

    def place_widgets(self):
        # log in widgets
        self.logInLabel.place(relx=0.1, rely=0.2)
        self.logLabel.place(relx=0.1, rely=0.3)
        self.logEntry.place(relx=0.1, rely=0.35)
        self.passwordLabel.place(relx=0.1, rely=0.4)
        self.passwordEntry.place(relx=0.1, rely=0.45)
        self.logInBtn.place(relx=0.1, rely=0.55)

        # registration widgets
        self.regLabel.place(relx=0.6, rely=0.2)
        self.regLogLabel.place(relx=0.6, rely=0.3)
        self.regLogEntry.place(relx=0.6, rely=0.35)
        self.regPasswordLabel.place(relx=0.6, rely=0.4)
        self.regPasswordEntry.place(relx=0.6, rely=0.45)
        self.regPasswordConfirmLabel.place(relx=0.6, rely=0.5)
        self.regPasswordConfirmEntry.place(relx=0.6, rely=0.55)
        self.regBtn.place(relx=0.6, rely=0.65)

    def register(self):
        login = self.regLogEntry.get()
        password = self.regPasswordEntry.get()
        password_confirm = self.regPasswordConfirmEntry.get()

        if '' in (login, password, password_confirm):
            messagebox.showerror('Error', 'Please fill all entries.')
            self.regPasswordEntry.delete(0, 'end')
            self.regPasswordConfirmEntry.delete(0, 'end')
            return

        login_in_db = self.dbm.get_column_values('Users', 'login')

        if login in login_in_db:
            messagebox.showerror('Error', f'Login \'{login}\' is already used.')
            self.regPasswordEntry.delete(0, 'end')
            self.regPasswordConfirmEntry.delete(0, 'end')
            return

        if password != password_confirm:
            messagebox.showerror('Error', 'Password and password confirmation don\'t match.')
            self.regPasswordEntry.delete(0, 'end')
            self.regPasswordConfirmEntry.delete(0, 'end')
            return

        self.dbm.insert('Users', 'login, password', (login, password))

        self.regLogEntry.delete(0, 'end')
        self.regPasswordEntry.delete(0, 'end')
        self.regPasswordConfirmEntry.delete(0, 'end')

    def login(self):
        login = self.logEntry.get()
        password = self.passwordEntry.get()

        if '' in (login, password):
            messagebox.showerror('Error', 'Please fill all entries.')
            self.passwordEntry.delete(0, 'end')
            return

        log_in_db = self.dbm.get_column_values('Users', 'login')

        if login not in log_in_db:
            messagebox.showerror('Error', f'Login \'{login}\' is not correct.')
            self.logEntry.delete(0, 'end')
            self.passwordEntry.delete(0, 'end')
            return

        if password != self.dbm.get_user_password(login):
            messagebox.showerror('Error', 'Entered password is not correct.')
            self.passwordEntry.delete(0, 'end')
            return

        self.root.destroy()
