from window import Window
import tkinter as tk
from tkinter import messagebox
import re
from forgetformwindow import ForgetFormWindow


class StartWindow(Window):
    def __init__(self, db_manager, mail_manager):
        super().__init__(db_manager, mail_manager)

        # log in widgets
        self.logInLabel = tk.Label(self.root, text="Log In", font="12", bg=self.bg_color)
        self.logLabel = tk.Label(self.root, text="Login:", bg=self.bg_color)
        self.logEntry = tk.Entry(self.root, width=25)
        self.passwordLabel = tk.Label(self.root, text="Password:", bg=self.bg_color)
        self.passwordEntry = tk.Entry(self.root, width=25, show='*')
        self.logInBtn = tk.Button(self.root, text="Log In", bg='white', command=self.login)
        self.forgetBtn = tk.Button(self.root, text="Forgot password?", bg="white", command=self.forgot_password)

        # registration widgets
        self.regLabel = tk.Label(self.root, text="Registration", font="12", bg=self.bg_color)
        self.regLogLabel = tk.Label(self.root, text="Login:", bg=self.bg_color)
        self.regLogEntry = tk.Entry(self.root, width=25)
        self.regPasswordLabel = tk.Label(self.root, text="Password:", bg=self.bg_color)
        self.regPasswordEntry = tk.Entry(self.root, width=25, show='*')
        self.regPasswordConfirmLabel = tk.Label(self.root, text="Confirm Password:", bg=self.bg_color)
        self.regPasswordConfirmEntry = tk.Entry(self.root, width=25, show='*')
        self.regEmailLabel = tk.Label(self.root, text="Email:", bg=self.bg_color)
        self.regEmailEntry = tk.Entry(self.root, width=25)
        self.regPinLabel = tk.Label(self.root, text="PIN:", bg=self.bg_color)
        self.regPinEntry = tk.Entry(self.root, width=25, show='*')
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
        self.forgetBtn.place(relx=0.1, rely=0.65)

        # registration widgets
        self.regLabel.place(relx=0.6, rely=0.2)
        self.regLogLabel.place(relx=0.6, rely=0.3)
        self.regLogEntry.place(relx=0.6, rely=0.35)
        self.regPasswordLabel.place(relx=0.6, rely=0.4)
        self.regPasswordEntry.place(relx=0.6, rely=0.45)
        self.regPasswordConfirmLabel.place(relx=0.6, rely=0.5)
        self.regPasswordConfirmEntry.place(relx=0.6, rely=0.55)
        self.regEmailLabel.place(relx=0.6, rely=0.60)
        self.regEmailEntry.place(relx=0.6, rely=0.65)
        self.regPinLabel.place(relx=0.6, rely=0.70)
        self.regPinEntry.place(relx=0.6, rely=0.75)
        self.regBtn.place(relx=0.6, rely=0.85)

    def register(self):
        login = self.regLogEntry.get()
        password = self.regPasswordEntry.get()
        password_confirm = self.regPasswordConfirmEntry.get()
        email = self.regEmailEntry.get()
        pin = self.regPinEntry.get()

        if '' in (login, password, password_confirm, email, pin):
            messagebox.showerror('Error', 'Please fill all entries.')
            Window.delete_entries(self.regPasswordEntry, self.regPasswordConfirmEntry, self.regPinEntry)
            return

        login_in_db = self.dbm.get_column_values('Users', 'login')

        if login in login_in_db:
            messagebox.showerror('Error', f'Login \'{login}\' is already used.')
            Window.delete_entries(self.regLogEntry, self.regPasswordEntry, self.regPasswordConfirmEntry,
                                  self.regEmailEntry, self.regPinEntry)
            return

        if password != password_confirm:
            messagebox.showerror('Error', 'Password and password confirmation don\'t match.')
            Window.delete_entries(self.regPasswordEntry, self.regPasswordConfirmEntry,
                                  self.regEmailEntry, self.regPinEntry)
            return

        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            messagebox.showerror('Error', 'Invalid email.')
            Window.delete_entries(self.regPasswordEntry, self.regPasswordConfirmEntry,
                                  self.regEmailEntry, self.regPinEntry)
            return

        self.dbm.insert('Users', 'login, password, email, pin', (login, password, email, pin))

        Window.delete_entries(self.regLogEntry, self.regPasswordEntry, self.regPasswordConfirmEntry,
                              self.regEmailEntry, self.regPinEntry)

        self.mailm.send_mail(email, login, msg_type='thanks')

    def login(self):
        login = self.logEntry.get()
        password = self.passwordEntry.get()

        if '' in (login, password):
            messagebox.showerror('Error', 'Please fill all entries.')
            Window.delete_entries(self.passwordEntry)
            return

        log_in_db = self.dbm.get_column_values('Users', 'login')

        if login not in log_in_db:
            messagebox.showerror('Error', f'Login \'{login}\' is not correct.')
            Window.delete_entries(self.logEntry, self.passwordEntry)
            return

        if password != self.dbm.get_column_value_where('Users', 'password', 'login', login):
            messagebox.showerror('Error', 'Entered password is not correct.')
            Window.delete_entries(self.passwordEntry)
            return

        self.user = {
            'id': self.dbm.get_column_value_where('Users', 'id', 'login', login),
            'login': login,
            'password': password,
            'email': self.dbm.get_column_value_where('Users', 'email', 'login', login),
            'pin': self.dbm.get_column_value_where('Users', 'pin', 'login', login)
        }

        self.mailm.send_mail(self.user['email'], login)
        self.root.destroy()

    def forgot_password(self):
        self.forgetBtn.config(state='disabled')
        forgot_from = ForgetFormWindow(self.root, self.dbm, self.mailm, self.forgetBtn, self.bg_color)


