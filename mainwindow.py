from window import Window
import tkinter as tk
from accountformwindow import AccountFormWindow
from tkinter import messagebox


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

        self.userInfoLabel = tk.Label(self.root, text=f'Logged in as {user["login"]}', bg=self.bg_color)
        self.accountsListLabel = tk.Label(self.root, text='Accounts List:', bg=self.bg_color)
        self.titleLabel = tk.Label(self.root, text='Name', bg=self.bg_color)
        self.loginLabel = tk.Label(self.root, text='Login', bg=self.bg_color)
        self.associatedEmailLabel = tk.Label(self.root, text='Associated Email', bg=self.bg_color)
        self.passwordLabel = tk.Label(self.root, text='Password', bg=self.bg_color)
        self.optionsLabel = tk.Label(self.root, text='Options', bg=self.bg_color)
        self.addAccountBtn = tk.Button(self.root, text='+ Add Account', bg='#6bfc03', command=self.open_add_acc_form)

        self.place_widgets()
        self.display_accounts()

    def place_widgets(self):
        self.userInfoLabel.place(relx=0, rely=0)
        self.accountsListLabel.place(relx=0, rely=0.05)
        self.titleLabel.place(relx=self.titleWidth, rely=0.1)
        self.loginLabel.place(relx=self.loginWidth, rely=0.1)
        self.associatedEmailLabel.place(relx=self.associatedEmailWidth, rely=0.1)
        self.passwordLabel.place(relx=self.passwordWidth, rely=0.1)
        self.optionsLabel.place(relx=self.passwordWidth + 0.275, rely=0.1)

    def disable_buttons(self):
        for btn in self.toDisable:
            btn.config(state='disabled')

    def open_add_acc_form(self):
        self.disable_buttons()
        form_window = AccountFormWindow(self, mode='Add')

    def delete_account(self, acc_id):
        if messagebox.askokcancel(title='Deleting account', message='Are you sure you want to delete this account?'):
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

        password = tk.Label(self.root,
                            text=self.dbm.get_column_value_where('Accounts', 'password', 'id', btn['acc_id']),
                            bg=self.bg_color)
        password.place(relx=btn['x'], rely=btn['y'])

        # % same here, adding shown password label to accountsRowsWidgets eliminates the bug
        self.accountsRowsWidgets.append({'shown_password': password})

    def show_password(self, btn):
        btn['btn']['text'] = 'Show'
        pin_entry = tk.Entry(self.root, width=17, show='*')
        pin_entry.place(relx=btn['x'] + 0.05, rely=btn['y'])

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
            title = tk.Label(self.root, text=accounts[i]['title'], bg=self.bg_color)
            title.place(relx=self.titleWidth, rely=0.15 + 0.05 * i)

            login = tk.Label(self.root, text=accounts[i]['login'], bg=self.bg_color)
            login.place(relx=self.loginWidth, rely=0.15 + 0.05 * i)

            associated_email = tk.Label(self.root, text=accounts[i]['associated_email'], bg=self.bg_color)
            associated_email.place(relx=self.associatedEmailWidth, rely=0.15 + 0.05 * i)

            # SHOW BTN
            show_btn = tk.Button(self.root, text='Enter PIN to show', bg='white')
            show_btn.place(relx=self.passwordWidth, rely=0.15 + 0.05 * i, relheight=0.04)
            self.showButtons.append({'btn': show_btn, 'y': 0.15 + 0.05 * i, 'x': self.passwordWidth,
                                     'acc_id': accounts[i]['id']})
            self.showButtons[i]['btn']['command'] = lambda btn=self.showButtons[i]: self.show_password(btn)

            # EDIT BTN
            edit_btn = tk.Button(self.root, text='Edit', bg='white',
                                 command=lambda index=i: self.edit_account(accounts[index]['id']))
            edit_btn.place(relx=self.editWidth, rely=0.15 + 0.05 * i, relheight=0.04)
            self.editButtons.append({'btn': edit_btn, 'x': self.editWidth, 'y': 0.15 + 0.05 * i})

            # DELETE BTN
            delete_btn = tk.Button(self.root, text='Delete', bg='red', fg='white',
                                   command=lambda index=i: self.delete_account(accounts[index]['id']))
            delete_btn.place(relx=self.deleteWidth, rely=0.15 + 0.05 * i, relheight=0.04)

            row = {'title': title, 'login': login, 'associated_email': associated_email,
                   'show_btn': show_btn, 'edit_btn': edit_btn, 'delete_btn': delete_btn}

            self.accountsRowsWidgets.append(row)

            self.toDisable.append(edit_btn)
            self.toDisable.append(delete_btn)

        self.toDisable.append(self.addAccountBtn)
        self.addAccountBtn.place(relx=0.005, rely=0.15 + 0.05 * len(accounts))




