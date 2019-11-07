from window import Window
import tkinter as tk
from accountformwindow import AccountFormWindow


class MainWindow(Window):
    def __init__(self, dbm, mailm, user):
        super().__init__(dbm, mailm)
        self.user = user

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
        self.addAccountBtn = tk.Button(self.root, text='+ Add Account', bg='#6bfc03', command=self.open_acc_form)

        self.place_widgets()
        self.display_accounts()

        print(self.dbm.get_user_accounts(self.user['id']))

    def place_widgets(self):
        self.userInfoLabel.place(relx=0, rely=0)
        self.accountsListLabel.place(relx=0, rely=0.05)
        self.titleLabel.place(relx=self.titleWidth, rely=0.1)
        self.loginLabel.place(relx=self.loginWidth, rely=0.1)
        self.associatedEmailLabel.place(relx=self.associatedEmailWidth, rely=0.1)
        self.passwordLabel.place(relx=self.passwordWidth, rely=0.1)
        self.optionsLabel.place(relx=self.passwordWidth + 0.275, rely=0.1)
        #self.addAccountBtn.place(relx=0.125, rely=0.025, relwidth=0.2, relheight=0.05)

    def open_acc_form(self):
        self.addAccountBtn.config(state='disabled')
        acc_form_window = AccountFormWindow(self.root, self.user, self.dbm, self.bg_color,
                                            self.addAccountBtn, mode='Add')

    def display_accounts(self):
        accounts = self.dbm.get_user_accounts(self.user['id'])
        for i in range(len(accounts)):
            title = tk.Label(self.root, text=accounts[i]['title'], bg=self.bg_color)
            title.place(relx=self.titleWidth, rely=0.15 + 0.05 * i)

            login = tk.Label(self.root, text=accounts[i]['login'], bg=self.bg_color)
            login.place(relx=self.loginWidth, rely=0.15 + 0.05 * i)

            associated_email = tk.Label(self.root, text=accounts[i]['associated_email'], bg=self.bg_color)
            associated_email.place(relx=self.associatedEmailWidth, rely=0.15 + 0.05 * i)

            show_btn = tk.Button(self.root, text='Show', bg='white')
            show_btn.place(relx=self.passwordWidth + 0.01, rely=0.15 + 0.05 * i, relheight=0.04)

            edit_btn = tk.Button(self.root, text='Edit', bg='white')
            edit_btn.place(relx=self.editWidth, rely=0.15 + 0.05 * i, relheight=0.04)

            edit_btn = tk.Button(self.root, text='Delete', bg='red', fg='white')
            edit_btn.place(relx=self.deleteWidth, rely=0.15 + 0.05 * i, relheight=0.04)

        self.addAccountBtn.place(relx=0.005, rely=0.15 + 0.05 * len(accounts))


