from dbmanager import DbManager
from mailmanager import MailManager
from startwindow import StartWindow
from mainwindow import MainWindow

dbm = DbManager('pass_manager.db')
dbm.setup_db()

mailm = MailManager()

startWindow = StartWindow(dbm, mailm)
startWindow.run()

try:
    mainWindow = MainWindow(dbm, mailm, startWindow.user)
    mainWindow.run()
except Exception as e:
    print(e)

