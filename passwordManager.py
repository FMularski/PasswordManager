from dbmanager import DbManager
from mailmanager import MailManager
from startwindow import StartWindow
from mainwindow import MainWindow

dbm = DbManager('pass_manager.db')
dbm.setup_db()

mailm = MailManager()

startWindow = StartWindow(dbm, mailm)

try:
    mainWindow = MainWindow(dbm, mailm, startWindow.user)
except Exception as e:
    print(e)

