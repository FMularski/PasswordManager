from dbmanager import DbManager
from startwindow import StartWindow

dbm = DbManager('pass_manager.db')
dbm.setup_db()

startWindow = StartWindow(dbm)
startWindow.run()
