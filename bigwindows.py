import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog

from smallwindows import AskValuesWindow, AccountFormWindow, ChangeSecurityWindow
from window import Window
from scrollframe import ScrollFrame

from mailmanager import MailManager
from dbmanager import DbManager

import re
import random


class StartWindow(Window):
    def __init__(self):
        super().__init__()

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
        self.root.mainloop()

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

        self.root.mainloop()

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

        login_in_db = DbManager.get_column_values('Users', 'login')

        if login in login_in_db:
            messagebox.showerror('Error', f'Login \'{login}\' is already used.')
            Window.delete_entries(self.regLogEntry, self.regPasswordEntry, self.regPasswordConfirmEntry,
                                  self.regEmailEntry, self.regPinEntry)
            return

        if len(password) < 8:   # password minimum length
            messagebox.showerror('Error', 'Password must be at least 8 characters long.')
            Window.delete_entries(self.regPasswordEntry, self.regPasswordConfirmEntry, self.regPinEntry)
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

        verification_code = random.randint(100000, 999999)
        MailManager.send_mail(email, msg_type='thanks', data=login, data2=verification_code)
        entered_code = simpledialog.askinteger('Email verification', 'Please verify your email by '
                                               'entering the code\nthat has been sent to your email address.')

        if entered_code != verification_code:
            messagebox.showerror('Error', 'Invalid verification code.')
            Window.delete_entries(self.regLogEntry, self.regPasswordEntry, self.regPasswordConfirmEntry,
                                  self.regEmailEntry, self.regPinEntry)
            return

        if entered_code == verification_code:
            DbManager.insert('Users', 'login, password, email, pin', (login, password, email, pin))
            Window.delete_entries(self.regLogEntry, self.regPasswordEntry, self.regPasswordConfirmEntry,
                                  self.regEmailEntry, self.regPinEntry)

    def login(self):
        login = self.logEntry.get()
        password = self.passwordEntry.get()

        if '' in (login, password):
            messagebox.showerror('Error', 'Please fill all entries.')
            Window.delete_entries(self.passwordEntry)
            return

        log_in_db = DbManager.get_column_values('Users', 'login')

        if login not in log_in_db:
            messagebox.showerror('Error', f'Login \'{login}\' is not correct.')
            Window.delete_entries(self.logEntry, self.passwordEntry)
            return

        if password != DbManager.get_column_value_where('Users', 'password', 'login', login):
            messagebox.showerror('Error', 'Entered password is not correct.')
            Window.delete_entries(self.passwordEntry)
            return

        self.user = {
            'id': DbManager.get_column_value_where('Users', 'id', 'login', login),
            'login': login,
            'password': password,
            'email': DbManager.get_column_value_where('Users', 'email', 'login', login),
            'pin': DbManager.get_column_value_where('Users', 'pin', 'login', login)
        }

        MailManager.send_mail(self.user['email'], 'alert', data=login)
        self.root.destroy()

        main_window = MainWindow(self.user)
        main_window.root.mainloop()

    def forgot_password(self):
        self.forgetBtn.config(state='disabled')
        forgot_from = AskValuesWindow(self.root, 'Forgot password?', ['Login', 'Email'], [self.logInBtn,
                                      self.forgetBtn, self.regBtn], self.bg_color)


class SettingsWindow(Window):
    def __init__(self, user, main_window):
        super().__init__()
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
        main_window = self.mainWindow.__init__(self.user)

    def log_out(self):
        if messagebox.askokcancel('Log out', 'Are you sure you want to log out?'):
            self.root.destroy()
            start_window = StartWindow()


class MainWindow(Window):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.accountsRowsWidgets = []
        self.showButtons = []
        self.editButtons = []
        self.toDisable = []

        self.titleWidth = 0
        self.loginWidth = 0.2
        self.associatedEmailWidth = 0.37
        self.passwordWidth = 0.6
        self.editWidth = 0.85
        self.deleteWidth = 0.9

        self.scrollframe = ScrollFrame(self.root)
        self.userInfoLabel = tk.Label(self.root, text=f'Logged in as {user["login"]}', bg=self.bg_color)
        self.titleLabel = tk.Label(self.scrollframe.viewPort, text='Title', bg=self.bg_color)
        self.loginLabel = tk.Label(self.scrollframe.viewPort, text='Login', bg=self.bg_color)
        self.associatedEmailLabel = tk.Label(self.scrollframe.viewPort, text='Associated Email', bg=self.bg_color)
        self.passwordLabel = tk.Label(self.scrollframe.viewPort, text='Password', bg=self.bg_color)
        self.separationLabel = tk.Label(self.scrollframe.viewPort, text=' ' * 40, bg=self.bg_color)
        self.addAccountBtn = tk.Button(self.root, text='+ Add Account', bg='#6bfc03', command=self.open_add_acc_form)
        self.settingBtn = tk.Button(self.root, text='Settings', bg='#dedcd1', command=self.open_settings)
        self.exportBtn = tk.Button(self.root, text='Export as txt', bg='#dedcd1', command=self.open_window_to_export)

        self.place_widgets()
        self.display_accounts()
        self.root.mainloop()

    def place_widgets(self):
        self.userInfoLabel.place(relx=0, rely=0)
        self.addAccountBtn.place(relx=0, rely=0.05)
        self.exportBtn.place(relx=0.12, rely=0.05)
        self.settingBtn.place(relx=0.9, rely=0.05)
        self.scrollframe.place(relx=0, rely=0.15, relwidth=1, relheight=0.80)
        self.titleLabel.grid(row=0, column=0)
        self.loginLabel.grid(row=0, column=1)
        self.associatedEmailLabel.grid(row=0, column=2)
        self.passwordLabel.grid(row=0, column=3)
        self.separationLabel.grid(row=0, column=4)

    def disable_buttons(self):
        for btn in self.toDisable:
            btn.config(state='disabled')

    def open_add_acc_form(self):
        self.disable_buttons()
        form_window = AccountFormWindow(self, mode='Add')

    def delete_account(self, acc_id):
        if messagebox.askokcancel(title='Delete account', message='Are you sure you want to delete this account?'):
            DbManager.delete('Accounts', 'id', acc_id)
            self.display_accounts()

    def edit_account(self, acc_id):
        self.disable_buttons()
        form_window = AccountFormWindow(self, mode='Edit')
        form_window.load_account_data(acc_id)

    def check_pin(self, pin, btn):
        if pin.get() != DbManager.get_column_value_where('Users', 'pin', 'id', self.user['id']):
            messagebox.showerror('Error', 'Invalid PIN.')
            pin.delete(0, 'end')
            return
        btn['btn'].destroy()
        pin.destroy()

        password = tk.Label(self.scrollframe.viewPort,
                            text=DbManager.get_column_value_where('Accounts', 'password', 'id', btn['acc_id']),
                            bg=self.bg_color)
        password.grid(row=btn['y'], column=3)

        # % same here, adding shown password label to accountsRowsWidgets eliminates the bug
        self.accountsRowsWidgets.append({'shown_password': password})

    def show_password(self, btn):
        btn['btn']['text'] = 'Show'
        pin_entry = tk.Entry(self.scrollframe.viewPort, width=17, show='*')
        pin_entry.grid(row=btn['y'], column=4)
        # pin_entry.place(relx=btn['x'] + 0.05, rely=btn['y'])

        btn['btn']['command'] = lambda: self.check_pin(pin_entry, btn)

        # % accountsRowsWidgets is cleared every time display_accounts is called so adding these
        # widgets gets rid of the bug which caused show btn and pin entry to be left
        # after add/delete account
        self.accountsRowsWidgets.append({'show_btn': btn['btn'], 'pin_entry': pin_entry})

    def display_accounts(self):
        self.showButtons.clear()
        self.toDisable.clear()
        for row in self.accountsRowsWidgets:
            for widget in row.values():
                widget.destroy()

        self.accountsRowsWidgets.clear()
        accounts = DbManager.get_user_accounts(self.user['id'])

        for i in range(len(accounts)):
            title = tk.Label(self.scrollframe.viewPort, text=accounts[i]['title'], bg=self.bg_color)
            title.grid(row=i + 1, column=0)

            login = tk.Label(self.scrollframe.viewPort, text=accounts[i]['login'], bg=self.bg_color)
            login.grid(row=i + 1, column=1)

            associated_email = tk.Label(self.scrollframe.viewPort, text=accounts[i]['associated_email'],
                                        bg=self.bg_color)
            associated_email.grid(row=i + 1, column=2)

            # SHOW BTN
            show_btn = tk.Button(self.scrollframe.viewPort, text='Enter PIN to show', bg='white')
            show_btn.grid(row=i + 1, column=3)
            self.showButtons.append({'btn': show_btn, 'y': i + 1, 'x': self.passwordWidth,
                                     'acc_id': accounts[i]['id']})
            self.showButtons[i]['btn']['command'] = lambda btn=self.showButtons[i]: self.show_password(btn)

            # EDIT BTN
            edit_btn = tk.Button(self.scrollframe.viewPort, text='Edit', bg='white',
                                 command=lambda index=i: self.edit_account(accounts[index]['id']))
            edit_btn.grid(row=i + 1, column=99)
            self.editButtons.append({'btn': edit_btn, 'x': self.editWidth, 'y': 0.05 * i})

            # DELETE BTN
            delete_btn = tk.Button(self.scrollframe.viewPort, text='Delete', bg='red', fg='white',
                                   command=lambda index=i: self.delete_account(accounts[index]['id']))
            delete_btn.grid(row=i + 1, column=100)

            row = {'title': title, 'login': login, 'associated_email': associated_email,
                   'show_btn': show_btn, 'edit_btn': edit_btn, 'delete_btn': delete_btn}

            self.accountsRowsWidgets.append(row)

            self.toDisable.append(edit_btn)
            self.toDisable.append(delete_btn)

        self.toDisable.append(self.addAccountBtn)

    def open_window_to_export(self):
        exportSecurityCheckWindow = AskValuesWindow(self.root, 'Export data', ['PIN', 'Password'], self.user,
                                                    self.toDisable + [self.exportBtn, self.settingBtn], self.bg_color)

    def open_settings(self):
        self.root.destroy()
        settings_window = SettingsWindow(self.user, self)
        settings_window.root.mainloop()


class SettingsWindow(Window):
    def __init__(self, user, main_window):
        super().__init__()
        self.user = user
        self.mainWindow = main_window
        self.toDisable = []
        self.children = []  # adding this field removes bug: closing 'X' settings_window after
        # closing security_change_window

        self.settingsLabel = tk.Label(self.root, text='Settings', bg=self.bg_color, font=10)

        self.securityLabel = tk.Label(self.root, text='Security', bg=self.bg_color)
        self.securityLine = tk.Frame(self.root, height=1, width=self.windowWidth * 0.9, bg='black')
        self.changePasswordBtn = tk.Button(self.root, text='Change password',
                                           command=lambda: self.change_security('password'))
        self.changePasswordLabel = tk.Label(self.root, text='You can change your password here.', bg=self.bg_color)
        self.changePinBtn = tk.Button(self.root, text='Change PIN', command=lambda: self.change_security('PIN'))
        self.changePinLabel = tk.Label(self.root, text='You can change your PIN here.', bg=self.bg_color)
        self.forgotPinBtn = tk.Button(self.root, text='Forgot PIN?', command=self.reset_pin)
        self.forgotPinLabel = tk.Label(self.root, text='If you forgot your PIN you can request a reminder here.',
                                       bg=self.bg_color)

        self.languageLabel = tk.Label(self.root, text='Language', bg=self.bg_color)
        self.languageLine = tk.Frame(self.root, height=1, width=self.windowWidth * 0.9, bg='black')
        self.changeLangDropdown = tk.OptionMenu(self.root, self.language, *('English', 'Polish'))
        self.saveLanguageBtn = tk.Button(self.root, text='Save', command='')
        self.changeLanguageLabel = tk.Label(self.root, text='You can select language here. Click \'Save\' to confirm.',
                                            bg=self.bg_color)

        self.backBtn = tk.Button(self.root, text='<< Back', bg='#dedcd1', command=self.back_to_main)
        self.logoutBtn = tk.Button(self.root, text='Log out', bg='pink', command=self.log_out)

        self.toDisable = [self.changePasswordBtn, self.changePinBtn, self.forgotPinBtn,
                          self.saveLanguageBtn, self.logoutBtn, self.backBtn, self.changeLangDropdown]

        print(self.language.get())
        self.place_widgets()

    def place_widgets(self):
        self.settingsLabel.place(relx=0, rely=0)
        self.securityLabel.place(relx=0, rely=0.1)
        self.securityLine.place(relx=0, rely=0.15)
        self.changePasswordBtn.place(relx=0.01, rely=0.175, relwidth=0.175)
        self.changePasswordLabel.place(relx=0.2, rely=0.175)
        self.changePinBtn.place(relx=0.01, rely=0.225, relwidth=0.175)
        self.changePinLabel.place(relx=0.2, rely=0.225)
        self.forgotPinBtn.place(relx=0.01, rely=0.275, relwidth=0.175)
        self.forgotPinLabel.place(relx=0.2, rely=0.275)

        self.languageLabel.place(relx=0, rely=0.35)
        self.languageLine.place(relx=0, rely=0.4)
        self.changeLangDropdown.place(relx=0.01, rely=0.425)
        self.saveLanguageBtn.place(relx=0.125, rely=0.425, relwidth=0.1)
        self.changeLanguageLabel.place(relx=0.25, rely=0.425)

        self.backBtn.place(relx=0.9, rely=0.8)
        self.logoutBtn.place(relx=0.01, rely=0.8, relwidth=0.225)

    def disable_buttons(self):
        for btn in self.toDisable:
            btn.config(state='disabled')

    def change_security(self, mode):
        validation_code = random.randint(100000, 999999)
        print(validation_code)
        MailManager.send_mail(self.user['email'], msg_type='security_change', data=validation_code, data2=mode)

        entered_code = simpledialog.askinteger(f'Change {mode}', 'A validation code has been sent to your email.\n'
                                                                 f'Enter it below to proceed with {mode} changing.')
        if not validation_code:
            messagebox.showerror('Error', f'{mode} change cancelled.')

        if validation_code == entered_code:
            self.disable_buttons()
            change_security_window = ChangeSecurityWindow(self, mode)
        else:
            messagebox.showerror('Error', 'Invalid validation code.')

    def reset_pin(self):
        verification_code = random.randint(100000, 999999)
        print(verification_code)
        MailManager.send_mail(self.user['email'], msg_type='security_change', data=verification_code, data2='PIN')

        entered_code = simpledialog.askinteger('Reset PIN', 'You will be able to reset your PIN\n'
                                                            'after entering the verification code\n'
                                                            'which has been sent to your email.')
        if entered_code != verification_code:
            messagebox.showerror('Error', 'Invalid verification PIN.')
            return

        reset_pin_window = AskValuesWindow(self.root, 'Reset PIN', ['New PIN', 'Confirm new PIN'],
                                           self.user, self.toDisable, self.bg_color)

    def back_to_main(self):
        self.root.destroy()
        main_window = self.mainWindow.__init__(self.user)

    def log_out(self):
        if messagebox.askokcancel('Log out', 'Are you sure you want to log out?'):
            self.user = None
            self.root.destroy()
            start_window = StartWindow()
