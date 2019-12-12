from dbmanager import DbManager
from mailmanager import MailManager
from bigwindows import StartWindow

dbm = DbManager('pass_manager.db')
dbm.setup_db()

mailm = MailManager()

startWindow = StartWindow(dbm, mailm)

