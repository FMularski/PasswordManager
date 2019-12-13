import sqlite3
from tkinter import messagebox


class DbManager:
    conn = sqlite3.connect('pass_manager.db')

    @classmethod
    def initialize(cls):
        try:
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
            cls.conn.execute(create_table_users_query)
            cls.conn.execute(create_table_accounts_query)
            cls.conn.commit()
        except sqlite3.Error as e:
            messagebox.showerror('Error', e)

    @classmethod
    def get_column_values(cls, table, column):
        cursor = cls.conn.cursor()
        try:
            cursor.execute(f'SELECT {column} FROM {table}')

            values = list()  # making [login1, login2, ...] from [(login1,), (login2,), ...]

            for values_list in cursor.fetchall():
                values.append(values_list[0])

            return values
        except sqlite3.Error as e:
            messagebox.showerror('Error', e)
            return []

    @classmethod
    def insert(cls, table, columns, values):
        try:
            values_question_marks = '?, ' * len(values)  # generates ?, ?, ?, ?, for the query

            insert_query = f'INSERT INTO {table} ({columns}) VALUES({values_question_marks[0:-2]})'  # -2 cuts ', '
            cls.conn.execute(insert_query, values)
            cls.conn.commit()

        except sqlite3.Error as e:
            messagebox.showerror('Error', e)
            return

        messagebox.showinfo('Success', f'{table[0:-1]} {values[0]} has been successfully created.')

    @classmethod
    def update(cls, table, column, new_value, where_column, where_column_value):
        try:
            update_query = f'UPDATE {table} SET {column} = ? WHERE {where_column} = ?'
            cls.conn.execute(update_query, (new_value, where_column_value,))
            cls.conn.commit()

        except sqlite3.Error as e:
            messagebox.showerror('Error', e)
            return

    @classmethod
    def get_column_value_where(cls, table, column, where_col, value):
        query = f'SELECT {column} FROM {table} WHERE {where_col} = ?'
        try:
            cursor = cls.conn.cursor()
            cursor.execute(query, (value,))
            return cursor.fetchone()[0]
        except sqlite3.Error as e:
            messagebox.showerror('Error', e)
            return

    @classmethod
    def get_user_accounts(cls, user_id):
        query = f'SELECT id, title, login, associated_email, password FROM Accounts WHERE user_id = ?'
        try:
            cursor = cls.conn.cursor()
            cursor.execute(query, (user_id,))

            accounts = list()
            raw_accounts = cursor.fetchall()

            for i in range(len(raw_accounts)):  # mapping raw accounts data to dict
                accounts.append({'id': raw_accounts[i][0], 'title': raw_accounts[i][1], 'login': raw_accounts[i][2],
                                 'associated_email': raw_accounts[i][3], 'password': raw_accounts[i][4]})
            return accounts
        except sqlite3.Error as e:
            messagebox.showerror('Error', e)
            return []

    @classmethod
    def delete(cls, table, column, value):
        cls.conn.execute(f'DELETE FROM {table} WHERE {column} = {value}')
        cls.conn.commit()






