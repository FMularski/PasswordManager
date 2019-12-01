import tkinter as tk
from tkinter import messagebox
import pyautogui as pag
from window import Window


class ForgetFormWindow(tk.Toplevel):
    def __init__(self, master, dbm, mailm, btn, bg_color):
        super().__init__(master)
        self.master = master
        self.dbm = dbm
        self.mailm = mailm
        self.btn = btn
        self.width, self.height = pag.size()

        self.canvas = tk.Canvas(self, width=self.width / 5, height=self.height / 5, bg=bg_color)
        self.forgetPassLabel = tk.Label(self, text='Forgot password?', font='12', bg=bg_color)
        self.forgetLoginLabel = tk.Label(self, text='Login:', bg=bg_color)
        self.forgetLoginEntry = tk.Entry(self, width=25)
        self.forgetEmailLabel = tk.Label(self, text='Email: ', bg=bg_color)
        self.forgetEmailEntry = tk.Entry(self, width=25)
        self.remindPasswordBtn = tk.Button(self, text='Remind Password', bg='white', command=self.remind_password)

        self.place_widgets()

        self.protocol('WM_DELETE_WINDOW', lambda: Window.close_top_level(self, [self.btn]))

    def place_widgets(self):
        self.canvas.pack()
        self.forgetPassLabel.place(relx=0, rely=0)
        self.forgetLoginLabel.place(relx=0.25, rely=0.2)
        self.forgetLoginEntry.place(relx=0.25, rely=0.3)
        self.forgetEmailLabel.place(relx=0.25, rely=0.4)
        self.forgetEmailEntry.place(relx=0.25, rely=0.5)
        self.remindPasswordBtn.place(relx=0.28, rely=0.7, relwidth=0.4)

    def remind_password(self):
        login = self.forgetLoginEntry.get()
        email = self.forgetEmailEntry.get()

        if '' in (login, email):
            messagebox.showerror('Error', 'Please fill all entries.')
            return

        log_in_db = self.dbm.get_column_values('Users', 'login')

        if login not in log_in_db:
            messagebox.showerror('Error', f'Login \'{login}\' is not correct.')
            return

        if email != self.dbm.get_column_value_where('Users', 'email', 'login', login):
            messagebox.showerror('Error', f'Email \'{email}\' does not match the entered login.')
            return

        password = self.dbm.get_column_value_where('Users', 'password', 'login', login)

        if self.mailm.send_mail(email, password, msg_type='password_request'):
            messagebox.showinfo('Password reminder request', 'Your request has been accepted. '
                                                             'You will receive an email with your password.')
        Window.close_top_level(self, [self.btn])
