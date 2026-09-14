def databaseFile():
   return "/usr/lib/cgi-bin/Dashboard/GNSS.db";

def firmwareLocation():
   return "/var/www/html/Dashboard/Firmware";

def sysLogLocation():
   return "/var/www/html/Dashboard/SysLog";

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
         hint = (
            " Directory {} is not writable (SQLite WAL needs to create {}-wal/-shm there). "
            "Fix: sudo chown www-data:nagios {dir} && sudo chmod 2775 {dir}; "
            "then re-run as www-data/nagios, or: sudo -u www-data {script}"
         ).format(
            db_dir,
            os.path.basename(path),
            dir=db_dir,
            script="Status_Update.py <id>",
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
         "(www-data:nagios, mode 2775) and GNSS.db-wal / GNSS.db-shm are group-writable. "
         "Or: sudo -u www-data Status_Update.py <id>".format(
            path, err, db_dir
         )
      ) from err
   return conn
