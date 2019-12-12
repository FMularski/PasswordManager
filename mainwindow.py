from window import Window
import tkinter as tk
from accountformwindow import AccountFormWindow
from tkinter import messagebox, filedialog, simpledialog
from scrollframe import ScrollFrame
from settingswindow import SettingsWindow


class MainWindow(Window):
    def __init__(self, dbm, mailm, user):
        super().__init__(dbm, mailm)
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
        self.exportBtn = tk.Button(self.root, text='Export as txt', bg='#dedcd1', command=self.export)

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
            self.dbm.delete('Accounts', 'id', acc_id)
            self.display_accounts()

    def edit_account(self, acc_id):
        self.disable_buttons()
        form_window = AccountFormWindow(self, mode='Edit')
        form_window.load_account_data(acc_id)

    def check_pin(self, pin, btn):
        if pin.get() != self.user['pin']:
            messagebox.showerror('Error', 'Invalid PIN.')
            pin.delete(0, 'end')
            return
        btn['btn'].destroy()
        pin.destroy()

        password = tk.Label(self.scrollframe.viewPort,
                            text=self.dbm.get_column_value_where('Accounts', 'password', 'id', btn['acc_id']),
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

        # TODO: 1) add comments

    def display_accounts(self):
        self.showButtons.clear()
        self.toDisable.clear()
        for row in self.accountsRowsWidgets:
            for widget in row.values():
                widget.destroy()

        self.accountsRowsWidgets.clear()
        accounts = self.dbm.get_user_accounts(self.user['id'])

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

    def export(self):
        pin = simpledialog.askstring('Export data', 'PIN:')
        if not pin:
            messagebox.showwarning('Aborted', 'Export aborted.')
            return

        password = simpledialog.askstring('Export data', 'Password:')
        if not password:
            messagebox.showwarning('Aborted', 'Export aborted.')
            return

        if pin == self.user['pin'] and password == self.user['password']:
            path = filedialog.askdirectory()
            path += '/exported_accounts.txt'

            accounts = self.dbm.get_user_accounts(self.user['id'])

            try:
                with open(path, 'w') as file:
                    for account in accounts:
                        row = 'title: ' + account['title'] + '\tlogin: ' + account['login'] + '\tassociated email: ' +\
                            account['associated_email'] + '\tpassword: ' + account['password'] + '\n'
                        file.write(row)
                messagebox.showinfo('Data exported', 'Remember that the exported file contains all of your '
                                    'passwords. Be cautious when granting access to this file. Deleting the file from '
                                    'widely accessible disk space is recommended. ')
            except PermissionError:
                pass
        else:
            messagebox.showerror('Error', 'Invalid PIN.')

    def open_settings(self):
        self.root.destroy()
        settings_window = SettingsWindow(self.dbm, self.mailm, self.user, self)
        settings_window.root.mainloop()









