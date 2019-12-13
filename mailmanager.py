import smtplib
from time import gmtime, strftime
import emailpass
from tkinter import messagebox


class MailManager:
    @classmethod
    def send_mail(cls, to_address, msg_type, data, data2=None):
        try:
            mail_conn = smtplib.SMTP('smtp.gmail.com', 587)
            mail_conn.ehlo()
            mail_conn.starttls()
            mail_conn.login(emailpass.login, emailpass.password)

            msgs = {
                    'thanks':           f'Subject: Hello {data}!\n\nThank you for registering to Password Manager. '
                                        f'Please scroll down to see your verification code' + '.\n' * 50 +
                                        f'Verification code: {data2}'
                                        f'\n\nAlways remember to keep your accounts safe!',

                    'alert':            f'Subject: Login Detected. \n\nLogin to your account {data} has been detected '
                                        f'in Password Manager at {strftime("%Y-%m-%d %H:%M:%S", gmtime())}.'
                                        f'\n\nAlways remember to keep you accounts safe!',

                    'password_request': f'Subject: Password reminder request.\n\nYou have requested a '
                                        f'password reminder for your Password Manager account. '
                                        f'Please scroll down' + '.\n' * 50 +
                                        f'Password: {data}.\n\nAlways remember to keep your accounts safe!',

                    'security_change': f'Subject: Validation code.\n\nYou have requested a validation code '
                                       f'in order to change your {data2}. '
                                       f'Please scroll down' + '.\n' * 45 + f'Validation code: {data}.\n\n'
                                       f'Always remember to keep your accounts safe!'
                    }

            mail_conn.sendmail(emailpass.login, to_address, msgs[msg_type])
            mail_conn.quit()
            return True
        except Exception as e:
            messagebox.showerror('Error', e)
            return False
