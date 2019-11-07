from window import Window
import tkinter as tk
from accountformwindow import AccountFormWindow


class MainWindow(Window):
    def __init__(self, dbm, mailm, user):
        super().__init__(dbm, mailm)
        self.user = user

        self.userInfoLabel = tk.Label(self.root, text=f'Logged in as {user["login"]}', bg=self.bg_color)
        self.accountsListLabel = tk.Label(self.root, text='Accounts List:', bg=self.bg_color)
        self.nameLabel = tk.Label(self.root, text='Name', bg=self.bg_color)
        self.loginLabel = tk.Label(self.root, text='Login', bg=self.bg_color)
        self.associatedEmailLabel = tk.Label(self.root, text='Associated Email', bg=self.bg_color)
        self.passwordLabel = tk.Label(self.root, text='Password', bg=self.bg_color)
        self.addAccountBtn = tk.Button(self.root, text='+ Add Account', bg='#6bfc03', command=self.open_acc_form)

        self.place_widgets()

        print(self.dbm.get_user_accounts(self.user['id']))

    def place_widgets(self):
        self.userInfoLabel.place(relx=0, rely=0)
        self.accountsListLabel.place(relx=0, rely=0.05)
        self.nameLabel.place(relx=0, rely=0.1)
        self.loginLabel.place(relx=0.2, rely=0.1)
        self.associatedEmailLabel.place(relx=0.37, rely=0.1)
        self.passwordLabel.place(relx=0.6, rely=0.1)
        self.addAccountBtn.place(relx=0.75, rely=0.1, relwidth=0.2, relheight=0.05)

    def open_acc_form(self):
        self.addAccountBtn.config(state='disabled')
        acc_form_window = AccountFormWindow(self.root, self.user, self.dbm, self.bg_color,
                                            self.addAccountBtn, mode='Add')
