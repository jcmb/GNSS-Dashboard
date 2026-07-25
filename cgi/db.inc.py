def databaseFile():
   return "/usr/lib/cgi-bin/Dashboard/GNSS.db";

def firmwareLocation():
   return "/var/www/html/Dashboard/Firmware";

def open_database():
   import sqlite3
   conn = sqlite3.connect(databaseFile(), timeout=10.0)
   conn.row_factory = sqlite3.Row
   conn.execute("PRAGMA busy_timeout = 10000")
   conn.execute("PRAGMA journal_mode = WAL")
   return conn
