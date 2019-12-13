import tkinter as tk
from tkinter import messagebox

from window import Window

from mailmanager import MailManager
from dbmanager import DbManager

import pyautogui as pag
import re


class ForgetFormWindow(tk.Toplevel):
    def __init__(self, master, btn, bg_color):
        super().__init__(master)
        self.master = master
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

        log_in_db = DbManager.get_column_values('Users', 'login')

        if login not in log_in_db:
            messagebox.showerror('Error', f'Login \'{login}\' is not correct.')
            return

        if email != DbManager.get_column_value_where('Users', 'email', 'login', login):
            messagebox.showerror('Error', f'Email \'{email}\' does not match the entered login.')
            return

        password = DbManager.get_column_value_where('Users', 'password', 'login', login)

        if MailManager.send_mail(email, msg_type='password_request', data=password):
            messagebox.showinfo('Password reminder request', 'Your request has been accepted. '
                                                             'You will receive an email with your password.')
        Window.close_top_level(self, [self.btn])


class AccountFormWindow(tk.Toplevel):
    def __init__(self, master, mode):
        super().__init__(master.root)
        self.user = master.user
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
        self.accTitleEntry.insert(0, DbManager.get_column_value_where('Accounts', 'title', 'id', acc_id))
        self.loginEntry.insert(0, DbManager.get_column_value_where('Accounts', 'login', 'id', acc_id))
        self.associatedEmailEntry.insert(0,
                                         DbManager.get_column_value_where('Accounts', 'associated_email', 'id', acc_id))
        self.passwordEntry.insert(0, DbManager.get_column_value_where('Accounts', 'password', 'id', acc_id))
        self.passwordConfirmEntry.insert(0, DbManager.get_column_value_where('Accounts', 'password', 'id', acc_id))
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

            user_id = DbManager.get_column_value_where('Users', 'id', 'login', self.user['login'])
            DbManager.insert('Accounts', 'title, login, associated_email, password, user_id',
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

            DbManager.update('Accounts', 'title', title, 'id', self.accId)
            DbManager.update('Accounts', 'login', login, 'id', self.accId)
            DbManager.update('Accounts', 'associated_email', associated_email, 'id', self.accId)
            DbManager.update('Accounts', 'password', password, 'id', self.accId)

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

        if self.mode == 'Edit' and pin != DbManager.get_column_value_where('Users', 'pin', 'id', self.user['id']):
            Window.delete_entries(self.pinEntry)
            messagebox.showerror('Error', 'Invalid PIN.')
            return None

        return title, login, associated_email, password,


class ChangeSecurityWindow(tk.Toplevel):
    def __init__(self, master, mode):
        super().__init__()
        self.master = master
        self.user = master.user
        self.mode = mode
        self.bg_color = master.bg_color

        self.width, self.height = pag.size().width / 5, pag.size().height / 4

        self.canvas = tk.Canvas(self, width=self.width, height=self.height, bg=self.bg_color)

        self.titleLabel = tk.Label(self, text=f'Change {mode}', bg=self.bg_color, font=10)
        self.oldSecurityLabel = tk.Label(self, text=f'Old {mode}:', bg=self.bg_color)
        self.oldSecurityEntry = tk.Entry(self, width=20, bg='white', show='*')
        self.newSecurityLabel = tk.Label(self, text=f'New {mode}:', bg=self.bg_color)
        self.newSecurityEntry = tk.Entry(self, width=20, bg='white', show='*')
        self.confirmSecurityLabel = tk.Label(self, text=f'Confirm {mode}:', bg=self.bg_color)
        self.confirmSecurityEntry = tk.Entry(self, width=20, bg='white', show='*')
        self.saveBtn = tk.Button(self, text='Save', width=20, bg='white', command=self.save_new_security)

        self.place_widgets()
        self.protocol('WM_DELETE_WINDOW', lambda: Window.close_top_level(self, master.toDisable))

    def place_widgets(self):
        self.canvas.pack()
        self.titleLabel.place(relx=0, rely=0)
        self.oldSecurityLabel.place(relx=0.25, rely=0.2)
        self.oldSecurityEntry.place(relx=0.25, rely=0.3, relwidth=0.45)
        self.newSecurityLabel.place(relx=0.25, rely=0.4)
        self.newSecurityEntry.place(relx=0.25, rely=0.5, relwidth=0.45)
        self.confirmSecurityLabel.place(relx=0.25, rely=0.6)
        self.confirmSecurityEntry.place(relx=0.25, rely=0.7, relwidth=0.45)
        self.saveBtn.place(relx=0.25, rely=0.85)

    def save_new_security(self):
        old_security = self.oldSecurityEntry.get()
        new_security = self.newSecurityEntry.get()
        confirm_security = self.confirmSecurityEntry.get()

        if not (old_security and new_security and confirm_security):
            messagebox.showerror('Error', 'All fields required.')
            Window.delete_entries(self.oldSecurityEntry, self.newSecurityEntry, self.confirmSecurityEntry)
            return

        if old_security != DbManager.get_column_value_where('Users', self.mode, 'id', self.user["id"]):
            messagebox.showerror('Error', 'Invalid old PIN.')
            Window.delete_entries(self.oldSecurityEntry, self.newSecurityEntry, self.confirmSecurityEntry)
            return

        if new_security != confirm_security:
            messagebox.showerror('Error', '\'New password\' and \'Confirm password\' entries don\'t match.')
            Window.delete_entries(self.oldSecurityEntry, self.newSecurityEntry, self.confirmSecurityEntry)
            return

        DbManager.update('Users', self.mode, new_security, 'id', self.user['id'])    # mode is pwd or pin
        messagebox.showinfo('Success', f'Your {self.mode} has been successfully changed.\nRemember not to share it '
                                       'with anyone else.')
        self.master.user[self.mode] = new_security     # update user
        Window.close_top_level(self, self.master.toDisable)
