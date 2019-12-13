import smtplib
from time import gmtime, strftime
import emailpass
from tkinter import messagebox


class MailManager:
    def send_mail(self, to_address, data, msg_type='alert'):
        try:
            mail_conn = smtplib.SMTP('smtp.gmail.com', 587)
            mail_conn.ehlo()
            mail_conn.starttls()
            mail_conn.login(emailpass.login, emailpass.password)

            if msg_type == 'thanks':
                msg = f'Subject: Hello {data}!\n\nThank you for registering to Password Manager.\n\nAlways remember' \
                      f' to keep your accounts safe!'
            elif msg_type == 'alert':
                time = strftime('%Y-%m-%d %H:%M:%S', gmtime())
                msg = f'Subject: Login Detected. \n\nLogin to your account {data} has been detected ' \
                      f'in Password Manager at {time}.\n\nAlways remember to keep you accounts safe!'
            elif msg_type == 'password_request':
                msg = f'Subject: Password reminder request.\n\nYou have requested a password reminder for your ' \
                      'Password Manager account. Please scroll down' + '.\n' * 50 + \
                      f'Password: {data}.\n\nAlways remember to ' \
                      f'keep your accounts safe!'
            elif msg_type == 'security_change':
                msg = f'Subject: Validation code.\n\nYou have requested a validation code in order to change your ' \
                      f'{data[0]}. Please scroll down' + '.\n' * 50 + f'Validation code: {data[1]}.\n\n' \
                                                                      f'Always remember to keep your accounts safe!'
            else:
                msg = 'Invalid msg_type. Ignore this message.'

            mail_conn.sendmail(emailpass.login, to_address, msg)
            mail_conn.quit()
            return True
        except Exception as e:
            messagebox.showerror('Error', e)
            return False
