import tkinter as tk
from tkinter import messagebox
import pyautogui as pag
import re
from window import Window


class AccountFormWindow(tk.Toplevel):
    #  def __init__(self, main, master, user, dbm, bg_color, btn, mode):
    def __init__(self, master, mode):
        super().__init__(master.root)
        self.user = master.user
        self.dbm = master.dbm
        self.mode = mode
        self.btn = master.addAccountBtn

        self.refreshAccountListMethod = master.display_accounts

        self.bg_color = master.bg_color
        self.width, self.height = pag.size()

        self.canvas = tk.Canvas(self, width=self.width / 7, height=self.height / 2, bg=self.bg_color)
        self.addAccountLabel = tk.Label(self, text=f'{self.mode} account', bg=self.bg_color, font='12')
        self.accTitleLabel = tk.Label(self, text='Title:', bg=self.bg_color)
        self.accTitleEntry = tk.Entry(self, width=25)
        self.loginLabel = tk.Label(self, text='Login*:', bg=self.bg_color)
        self.loginEntry = tk.Entry(self, width=25)
        self.associatedEmailLabel = tk.Label(self, text='Associated Email*:', bg=self.bg_color)
        self.associatedEmailEntry = tk.Entry(self, width=25)
        self.requiredInfo = tk.Label(self, text='* At least one of these two\nis required.', bg=self.bg_color)
        self.saveBtn = tk.Button(self, text='Save', bg='white', command=self.add_account)

        if mode == 'Add':
            self.passwordLabel = tk.Label(self, text='Password:', bg=self.bg_color)
            self.passwordEntry = tk.Entry(self, width=25, show='*')
            self.passwordConfirmLabel = tk.Label(self, text='Confirm Password:', bg=self.bg_color)
            self.passwordConfirmEntry = tk.Entry(self, width=25, show='*')
        elif mode == 'Edit':
            pass
        else:
            pass

        self.place_widgets()
        self.protocol('WM_DELETE_WINDOW', lambda: Window.close_top_level(self, self.btn))

    def place_widgets(self):
        self.canvas.pack()
        self.addAccountLabel.place(relx=0, rely=0)
        self.accTitleLabel.place(relx=0.15, rely=0.1)
        self.accTitleEntry.place(relx=0.15, rely=0.15)
        self.loginLabel.place(relx=0.15, rely=0.2)
        self.loginEntry.place(relx=0.15, rely=0.25)
        self.associatedEmailLabel.place(relx=0.15, rely=0.3)
        self.associatedEmailEntry.place(relx=0.15, rely=0.35)
        self.requiredInfo.place(relx=0.15, rely=0.65)

        if self.mode == 'Add':
            self.passwordLabel.place(relx=0.15, rely=0.4)
            self.passwordEntry.place(relx=0.15, rely=0.45)
            self.passwordConfirmLabel.place(relx=0.15, rely=0.5)
            self.passwordConfirmEntry.place(relx=0.15, rely=0.55)
            self.saveBtn.place(relx=0.3, rely=0.8, relwidth=0.4)

    def add_account(self):
        title = self.accTitleEntry.get()
        login = self.loginEntry.get()
        associated_email = self.associatedEmailEntry.get()
        password = self.passwordEntry.get()
        password_confirm = self.passwordConfirmEntry.get()

        if '' in (title, password, password_confirm) or not (login or associated_email):
            Window.delete_entries(self.passwordEntry, self.passwordConfirmEntry)
            messagebox.showerror('Error', 'Only login or associated email may remain empty.')
            return

        if password != password_confirm:
            Window.delete_entries(self.passwordEntry, self.passwordConfirmEntry)
            messagebox.showerror('Error', 'Password and password confirmation don\'t match.')
            return

        if associated_email:
            if not re.match(r'[^@]+@[^@]+\.[^@]+', associated_email):
                Window.delete_entries(self.passwordEntry, self.passwordConfirmEntry, self.associatedEmailEntry)
                messagebox.showerror('Error', 'Invalid email.')
                return

        user_id = self.dbm.get_user_field(self.user['login'], 'id')

        self.dbm.insert('Accounts', 'title, login, associated_email, password, user_id',
                               (title, login, associated_email, password, user_id))

        self.refreshAccountListMethod()
        Window.close_top_level(self, self.btn)