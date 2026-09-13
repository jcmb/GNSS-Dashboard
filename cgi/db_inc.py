def cgiDir():
#   return "/Users/gkirk/Documents/GitHub/GNSS-Dashboard/cgi/";
   return "/usr/lib/cgi-bin/Dashboard/";

def wwwDir():
#   return "/Users/gkirk/Documents/GitHub/GNSS-Dashboard/www/";
   return "/var/www/html/Dashboard/";

def databaseFile():
   return cgiDir() + "GNSS.db";

def firmwareLocation():
   return "/var/www/html/Dashboard/Firmware";

def open_database():
   import os
   import sqlite3

   path = databaseFile()
   db_dir = os.path.dirname(path) or "."
   try:
      conn = sqlite3.connect(path, timeout=10.0)
   except sqlite3.Error as err:
      hint = ""
      if not os.access(db_dir, os.W_OK):
         hint = " Directory {} is not writable (SQLite WAL needs to create {}-wal/-shm there).".format(
            db_dir, os.path.basename(path)
         )
      raise sqlite3.OperationalError(
         "Cannot open {}: {}.{}".format(path, err, hint)
      ) from err

   conn.row_factory = sqlite3.Row
   conn.execute("PRAGMA busy_timeout = 10000")
   try:
      conn.execute("PRAGMA journal_mode = WAL")
   except sqlite3.Error as err:
      raise sqlite3.OperationalError(
         "Cannot enable WAL on {}: {}. Ensure {} is writable by this user "
         "(www-data/nagios group) and that GNSS.db-wal / GNSS.db-shm are group-writable.".format(
            path, err, db_dir
         )
      ) from err
   return conn
