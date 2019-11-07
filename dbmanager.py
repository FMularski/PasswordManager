import sqlite3
from tkinter import messagebox


class DbManager:
    def __init__(self, db):
        try:
            self.conn = sqlite3.connect(db)
        except sqlite3.Error as e:
            messagebox.showerror('Error', e)

    def setup_db(self):
        create_table_users_query = """
            CREATE TABLE IF NOT EXISTS Users(
            id integer PRIMARY KEY AUTOINCREMENT,
            login text NOT NULL,
            email text NOT NULL,
            pin text NOT NULL,
            password text NOT NULL
            );"""

        create_table_accounts_query = """
                CREATE TABLE IF NOT EXISTS Accounts(
                id integer PRIMARY KEY AUTOINCREMENT,
                title text NOT NULL,
                login text,
                associated_email text,
                password text NOT NULL,
                user_id integer NOT NULL,
                FOREIGN KEY (user_id) REFERENCES Users(id)
                );"""

        try:
            self.conn.execute(create_table_users_query)
            self.conn.execute(create_table_accounts_query)
            self.conn.commit()

        except sqlite3.Error as e:
            messagebox.showerror('Error', e)

    def get_column_values(self, table, column):
        cursor = self.conn.cursor()
        try:
            cursor.execute(f'SELECT {column} FROM {table}')

            values = list()  # making [login1, login2, ...] from [(login1,), (login2,), ...]

            for values_list in cursor.fetchall():
                values.append(values_list[0])

            return values
        except sqlite3.Error as e:
            messagebox.showerror('Error', e)
            return []

    def insert(self, table, columns, values):
        try:
            values_question_marks = '?, ' * len(values)  # generates ?, ?, ?, ?, for the query

            insert_query = f'INSERT INTO {table} ({columns}) VALUES({values_question_marks[0:-2]})'  # -2 cuts ', '
            self.conn.execute(insert_query, values)
            self.conn.commit()

        except sqlite3.Error as e:
            messagebox.showerror('Error', e)
            return

        messagebox.showinfo('Success', f'{table[0:-1]} {values[0]} has been successfully created.')

    def get_user_field(self, login, field):
        query = f'SELECT {field} FROM Users WHERE login = ?'
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, (login,))
            return cursor.fetchone()[0]
        except sqlite3.Error as e:
            messagebox.showerror('Error', e)
            return

    def get_user_accounts(self, user_id):
        query = f'SELECT title, login, associated_email, password FROM Accounts WHERE user_id = ?'
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, (user_id,))

            accounts = list()
            raw_accounts = cursor.fetchall()

            for i in range(len(raw_accounts)): # mapping raw accounts data to dict
                accounts.append({'title': raw_accounts[i][0], 'login': raw_accounts[i][1],
                                 'associated_email': raw_accounts[i][2], 'password': raw_accounts[i][3]})
            return accounts
        except sqlite3.Error as e:
            messagebox.showerror('Error', e)
            return []





