import tkinter as tk
from tkinter import messagebox
import pyautogui as pag
import re
from window import Window


class AccountFormWindow(tk.Toplevel):
    def __init__(self, master, mode):
        super().__init__(master.root)
        self.user = master.user
        self.dbm = master.dbm
        self.mode = mode
        self.toDisable = master.toDisable
        self.accId = None

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
        self.saveBtn = tk.Button(self, text='Save', bg='white')

        if mode == 'Add':
            self.saveBtn['command'] = self.add_account
        elif mode == 'Edit':
            self.saveBtn['command'] = self.edit_account
        else:
            self.saveBtn['command'] = None

        self.passwordLabel = tk.Label(self, text='Password:', bg=self.bg_color)
        self.passwordEntry = tk.Entry(self, width=25, show='*')
        self.passwordConfirmLabel = tk.Label(self, text='Confirm Password:', bg=self.bg_color)
        self.passwordConfirmEntry = tk.Entry(self, width=25, show='*')
        self.pinLabel = tk.Label(self, text='PIN:',  bg=self.bg_color)
        self.pinEntry = tk.Entry(self, width=25, show='*')

        self.place_widgets()
        self.protocol('WM_DELETE_WINDOW', lambda: Window.close_top_level(self, self.toDisable))

    def load_account_data(self, acc_id):
        self.accTitleEntry.insert(0, self.dbm.get_column_value_where('Accounts', 'title', 'id', acc_id))
        self.loginEntry.insert(0, self.dbm.get_column_value_where('Accounts', 'login', 'id', acc_id))
        self.associatedEmailEntry.insert(0,
                                         self.dbm.get_column_value_where('Accounts', 'associated_email', 'id', acc_id))
        self.passwordEntry.insert(0, self.dbm.get_column_value_where('Accounts', 'password', 'id', acc_id))
        self.passwordConfirmEntry.insert(0,
                                         self.dbm.get_column_value_where('Accounts', 'password', 'id', acc_id))
        self.accId = acc_id

    def place_widgets(self):
        self.canvas.pack()
        self.addAccountLabel.place(relx=0, rely=0)
        self.accTitleLabel.place(relx=0.15, rely=0.1)
        self.accTitleEntry.place(relx=0.15, rely=0.15)
        self.loginLabel.place(relx=0.15, rely=0.2)
        self.loginEntry.place(relx=0.15, rely=0.25)
        self.associatedEmailLabel.place(relx=0.15, rely=0.3)
        self.associatedEmailEntry.place(relx=0.15, rely=0.35)
        self.passwordLabel.place(relx=0.15, rely=0.4)
        self.passwordEntry.place(relx=0.15, rely=0.45)
        self.passwordConfirmLabel.place(relx=0.15, rely=0.5)
        self.passwordConfirmEntry.place(relx=0.15, rely=0.55)
        self.requiredInfo.place(relx=0.15, rely=0.65)
        self.saveBtn.place(relx=0.3, rely=0.8, relwidth=0.4)
        if self.mode == 'Edit':
            self.pinLabel.place(relx=0.15, rely=0.6)
            self.pinEntry.place(relx=0.15, rely=0.65)
            self.requiredInfo.place(relx=0.15, rely=0.75)
            self.saveBtn.place(relx=0.3, rely=0.9, relwidth=0.4)

    def add_account(self):
        validation_result = self.validation()

        if validation_result:
            title = validation_result[0]
            login = validation_result[1]
            associated_email = validation_result[2]
            password = validation_result[3]

            user_id = self.dbm.get_column_value_where('Users', 'id', 'login', self.user['login'])
            self.dbm.insert('Accounts', 'title, login, associated_email, password, user_id',
                            (title, login, associated_email, password, user_id))

            self.refreshAccountListMethod()
            Window.close_top_level(self, self.toDisable)

    def edit_account(self):
        validation_result = self.validation()

        if validation_result:
            title = validation_result[0]
            login = validation_result[1]
            associated_email = validation_result[2]
            password = validation_result[3]

            self.dbm.update('Accounts', 'title', title, 'id', self.accId)
            self.dbm.update('Accounts', 'login', login, 'id', self.accId)
            self.dbm.update('Accounts', 'associated_email', associated_email, 'id', self.accId)
            self.dbm.update('Accounts', 'password', password, 'id', self.accId)

            self.refreshAccountListMethod()
            Window.close_top_level(self, self.toDisable)

    def validation(self):
        title = self.accTitleEntry.get()
        login = self.loginEntry.get()
        associated_email = self.associatedEmailEntry.get()
        password = self.passwordEntry.get()
        password_confirm = self.passwordConfirmEntry.get()
        pin = self.pinEntry.get()

        if not (login or associated_email):
            Window.delete_entries(self.passwordEntry, self.passwordConfirmEntry, self.pinEntry)
            messagebox.showerror('Error', 'Only login or associated email may remain empty.')
            return None

        if not (title and password):
            Window.delete_entries(self.passwordEntry, self.passwordConfirmEntry, self.pinEntry)
            messagebox.showerror('Error', 'Title and password are required.')
            return None

        if password != password_confirm:
            Window.delete_entries(self.passwordEntry, self.passwordConfirmEntry, self.pinEntry)
            messagebox.showerror('Error', 'Password and password confirmation don\'t match.')
            return None

        if associated_email:
            if not re.match(r'[^@]+@[^@]+\.[^@]+', associated_email):
                Window.delete_entries(self.passwordEntry, self.passwordConfirmEntry, self.associatedEmailEntry,
                                      self.pinEntry)
                messagebox.showerror('Error', 'Invalid email.')
                return None

        if self.mode == 'Edit' and pin != self.dbm.get_column_value_where('Users', 'pin', 'id', self.user['id']):
            Window.delete_entries(self.pinEntry)
            messagebox.showerror('Error', 'Invalid PIN.')
            return None

        return title, login, associated_email, password,

