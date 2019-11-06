import smtplib
from time import gmtime, strftime
import emailpass


class MailManager:
    def send_mail(self, to_address, login, msg_type='alert'):
        mail_conn = smtplib.SMTP('smtp.gmail.com', 587)
        mail_conn.ehlo()
        mail_conn.starttls()
        mail_conn.login(emailpass.login, emailpass.password)

        if msg_type == 'thanks':
            msg = f'Subject: Hello {login}!\n\nThank you for registering to Password Manager. Enjoy :)'
        else:
            time = strftime('%Y-%m-%d %H:%M:%S', gmtime())
            msg = f'Subject: Login Detected. \n\nLogin to your account {login} has been detected ' \
                  f'in the Password Manager at {time}. Always remember to keep you accounts safe!'

        mail_conn.sendmail(emailpass.login, to_address, msg)
        mail_conn.quit()