from time import gmtime, strftime

lp = {
    'English': {
        # START WINDOW
        'SW_login_title': 'Log In',
        'SW_login_login_entry': 'Login:',
        'SW_login_password_entry': 'Password:',
        'SW_login_login_btn': 'Log In',
        'SW_login_forgot_btn': 'Forgot password?',
        'SW_reg_title': 'Register',
        'SW_reg_login_entry': 'Login:',
        'SW_reg_password_entry': 'Password:',
        'SW_reg_password_confirm_entry': 'Confirm Password:',
        'SW_reg_email_entry': 'Email:',
        'SW_reg_pin_entry': 'PIN:',
        'SW_reg_reg_btn': 'Register',
        'error': 'Error',
        'fill_all_entries': 'Please fill all entries.',
        'login_used': 'Login \'{login}\' is already used.',
        'min_8_chars': 'Password must be at least 8 characters long.',
        'confirm_dont_match': 'Password and password confirmation don\'t match.',
        'invalid_email': 'Invalid email.',
        'msgs':
            {
                'thanks': 'Subject: Hello {data}!\n\nThank you for registering to Password Manager. '
                            'Please scroll down to see your verification code' + '.\n' * 50 +
                            'Verification code: {data2}\n\nAlways remember to keep your accounts safe!',

                'alert':    'Subject: Login Detected. \n\nLogin to your account {data} has been detected '
                            'in Password Manager at ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + '.'
                            '\n\nAlways remember to keep you accounts safe!{data2}',

                'password_request': 'Subject: Password reminder request.\n\nYou have requested a '
                                    'password reminder for your Password Manager account. '
                                    'Please scroll down' + '.\n' * 50 +
                                    'Password: {data}.\n\nAlways remember to keep your accounts safe!{data2}',

                'security_change': 'Subject: Validation code.\n\nYou have requested a validation code '
                                   'in order to change your {data2}. Please scroll down' + '.\n' * 45 +
                                   'Validation code: {data}.\n\nAlways remember to keep your accounts safe!'
            },
        'email_verification': 'Email verification',
        'please_verify_email': 'Please verify your email by entering the code\n'
                               'that has been sent to your email address.',
        'invalid_veri_code': 'Invalid verification code.',
        'success': 'Success',
        'user_created': 'User {user} has been successfully created.',
        'incorrect_login': 'Login \'{login}\' is not correct.',
        'incorrect_password': 'Incorrect password.',
        'forgot_password_title': 'Forgot password?',
        'Forgot password?': 'Forgot password?',
        'Export data': 'Export data',
        'Reset PIN': 'Reset PIN',
        'email_doesnt_match': 'Email \'{email}\' does not match the entered login.',
        'password_reminder_req': 'Password reminder request',
        'password_reminder_accepted': 'Your request has been accepted. You will receive an email with your password.',
        'Password': 'Password',

        # MAIN WINDOW
        'logged_as': 'Logged in as {login}',
        'acc_title': 'Title',
        'acc_login': 'Login',
        'acc_associated_email': 'Associated Email',
        'acc_password': 'Password',
        'add_acc_btn': '+ Add Account',
        'settings_btn': 'Settings',
        'export_btn': 'Export as .txt',
        'edit': 'Edit',
        'delete': 'Delete',
        'show': 'Show',
        'enter_pin_to_show': 'Enter PIN to show',
        'pin_or_password_invalid': 'Pin or password invalid.',
        'pin_and_password_req': 'PIN and password are both required.',
        'data_exported': 'Data exported',
        'data_exported_info': 'Remember that the exported file contains all of your passwords. Be cautious when '
                              'granting access to this file. Deleting the file from widely accessible disk space '
                              'is recommended.'
    },

    'Polish': {
        # START WINDOW
        'SW_login_title': 'Logowanie',
        'SW_login_login_entry': 'Login:',
        'SW_login_password_entry': 'Hasło:',
        'SW_login_login_btn': 'Zaloguj',
        'SW_login_forgot_btn': 'Nie pamiętasz hasła?',
        'SW_reg_title': 'Rejestracja',
        'SW_reg_login_entry': 'Login:',
        'SW_reg_password_entry': 'Hasło:',
        'SW_reg_password_confirm_entry': 'Potwierdź hasło:',
        'SW_reg_email_entry': 'Email:',
        'SW_reg_pin_entry': 'PIN:',
        'SW_reg_reg_btn': 'Zarejestruj',
        'error': 'Błąd',
        'fill_all_entries': 'Proszę wypełnić wszystkie pola.',
        'login_used': 'Login \'{login}\' jest już zajęty.',
        'min_8_chars': 'Hasło musi mieć przynajmniej 8 znaków długości.',
        'confirm_dont_match': 'Hasło i potwierdzenie hasła nie zgadzają się.',
        'invalid_email': 'Nieprawidłowy adres email.',
        'msgs':
            {
                'thanks': 'Subject: Witaj {data}!\n\nDziekujemy za zarejestrowanie sie w Password Manager. '
                            'Przewin w dol, aby zobaczyc kod weryfikacyjny' + '.\n' * 50 +
                            'Kod weryfikacyjny: {data2}\n\nPamietaj, aby zawsze chronic swoje konta!',

                'alert':    'Subject: Zarejestrowano logowanie\n\nLogowanie na Twoje konto {data} zostalo wykryte '
                            'w Password Manager o ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + '.'
                            '\n\nPamietaj, aby zawsze chronic swoje konta!{data2}',

                'password_request': 'Subject: Przypomnienie hasla\n\nZazadano przypomnienia hasla do Twojego konta '
                                    '{data2} w Password Manager. Przewin w dol' + '.\n' * 50 +
                                    'Haslo: {data}.\n\nPamietaj, aby zawsze chronic swoje konta!',

                'security_change': 'Subject: Kod weryfikacyjny\n\nZazadano wygenerowania kodu weryfikacyjnego '
                                   'w celu zmiany zabezpieczenia: {data2}. Przewin w dol' + '.\n' * 45 +
                                   'Kod weryfikacyjny: {data}.\n\nPamietaj, aby zawsze chronic swoje konta!'
            },
        'email_verification': 'Weryfikacja adresu email',
        'please_verify_email': 'Zweryfikuj podany adres email wpisując wysłany do Ciebie kod.',
        'invalid_veri_code': 'Nieprawidłowy kod weryfikacyjny.',
        'success': 'Sukces',
        'user_created': 'Użytkownik {user} został pomyślnie utworzony.',
        'incorrect_login': 'Login \'{login}\' jest nieprawidłowy.',
        'incorrect_password': 'Nieprawidłowe hasło.',
        'forgot_password_title': 'Zapomniałeś hasła?',
        'Zapomniałeś hasła?': 'Forgot password?',
        'Eksport danych': 'Export data',
        'Export data': 'Eksport danych',
        'Zapomniałeś PINu?': 'Reset PIN',
        'email_doesnt_match': 'Email \'{email}\' nie jest powiązany z wprowadzonym loginem.',
        'password_reminder_req': 'Żądanie przypomnienia hasła',
        'password_reminder_accepted': 'Żądanie przypomnienia hasła zaakceptowane. Hasło zostanie za chwilę wysłane '
                                      'na Twój adres email.',
        'Password': 'Hasło',

        # MAIN WINDOW
        'logged_as': 'Zalogowano jako {login}',
        'acc_title': 'Tytuł',
        'acc_login': 'Login',
        'acc_associated_email': 'Powiązany Email',
        'acc_password': 'Hasło',
        'add_acc_btn': '+ Dodaj Konto',
        'settings_btn': 'Ustawienia',
        'export_btn': 'Eksportuj jako .txt',
        'edit': 'Edytuj',
        'delete': 'Usuń',
        'show': 'Pokaż',
        'enter_pin_to_show': 'Wprowadź PIN, aby pokazać',
        'pin_or_password_invalid': 'Nieprawidłowy PIN lub hasło.',
        'pin_and_password_req': 'PIN i hasło wymagane.',
        'data_exported': 'Wyeksportowano dane',
        'data_exported_info': 'Pamiętaj, że wyeksportowany plik zawiera wszystkie Twoje hasła. Bądz ostrożny '
                              'podczas udzielania dostępu do tego pliku. Zalecane jest usunięcie go z ogólnodostępnej '
                              'przestrzeni dyskowej.'
    }
}
