from dbmanager import DbManager
from bigwindows import StartWindow

dbm = DbManager('pass_manager.db')
dbm.setup_db()

startWindow = StartWindow(dbm)

