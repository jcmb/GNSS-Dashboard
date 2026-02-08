#!/usr/bin/env python3
import cgi
import cgitb
import sqlite3
import os
import sys
import time
from subprocess import Popen, call
from pprint import pprint

# Ensure db_inc.py is accessible
try:
    from db_inc import *
except ImportError:
    print("Content-Type: text/html\n")
    print("Error: db_inc.py not found.")
    sys.exit(1)

cgitb.enable()

print("Content-Type: text/html")     # HTML is following
print()                               # blank line, end of headers

sys.stdout.flush()

try:
   conn = sqlite3.connect(databaseFile())
except sqlite3.Error:
   print("Error opening db. " + str(databaseFile()) + "\n")
   sys.exit(1)

conn.row_factory = sqlite3.Row
cursor = conn.cursor()

form = cgi.FieldStorage()

print("<html><head>")
print("<title>GNSS Firmware Upgrade</title>")
print("</head><body>")

if "User_ID" not in form:
    print("Internal Error: User ID not provided<br/>")
    sys.exit(100)
else:
    User_ID = form["User_ID"].value

if "Firmware" not in form:
    print("Internal Error: Firmware not provided<br/>")
    sys.exit(100)
else:
    Firmware_ID = form["Firmware"].value

# Fetch firmware filenames
# Note: The original code does not select 'AlloyFile' in this query,
# but tries to use it later. Ensure AlloyFile is defined in db_inc.py or add it to this query.
query = 'SELECT Titian_Version, AlloyFile, BarracudaFile, ChinstrapFile, ClarkFile, KryptonFile, LancetFile FROM Firmware where type=?'
cursor.execute(query, (Firmware_ID,))

rows = cursor.fetchone()

if not rows:
    print(f"Error: Firmware ID {Firmware_ID} not found.<br/>")
    sys.exit(1)

Firmware = rows[0]
AlloyFile = rows[1]
BarracudaFile = rows[2]
ChinstrapFile = rows[3]
ClarkFile = rows[4]
KryptonFile = rows[5]
LancetFile = rows[6]

print("Upgrading to firmware V" + str(Firmware) + "<br/>")

query = 'SELECT * FROM GNSS where User_ID=?'

print("<br/><pre>")

cursor.execute(query, (User_ID,))
rows = cursor.fetchall()

for row in rows:
   if "Upgrade_" + str(row["id"]) in form:
      firmware_file = ""
      GNSS_ID = row["id"]

      # Python 3 print with end=" " prevents the newline
      print(row["name"] + " (" + str(GNSS_ID) + ") Type: ", end=" ")

      Reciever_Type = int(row["Reciever_Type"])

      if Reciever_Type == 107:
         print("SPS852 ", end=" ")
         firmware_file = ""
         print("Not Supported")
      elif Reciever_Type == 118:
         print("SPS855 ", end=" ")
         firmware_file = ""
         print("Not Supported")
      elif Reciever_Type == 508:
         print("BX992-MS ", end=" ")
         firmware_file = KryptonFile
      elif Reciever_Type == 509:
         print("BX992-SPS ", end=" ")
         firmware_file = KryptonFile
      elif Reciever_Type == 164:
         print("BD992 ", end=" ")
         firmware_file = KryptonFile
      elif Reciever_Type == 330:
         print("MP86 ", end=" ")
         firmware_file = KryptonFile
      elif Reciever_Type == 331:
         print("MS96 ", end=" ")
         firmware_file = KryptonFile
      elif Reciever_Type == 38:
         print("SPS850 ", end=" ")
         firmware_file = ""
         print("Not Supported")
      elif Reciever_Type == 101:
         print("SPS985 ", end=" ")
         print("Not Supported")
      elif Reciever_Type == 162:
         print("Alloy ", end=" ")
         firmware_file = AlloyFile
      elif Reciever_Type == 169:
         print("SPS986 ", end=" ")
         firmware_file = ChinstrapFile
      elif Reciever_Type == 188:
         print("R750 ", end=" ")
         firmware_file = BarracudaFile
      elif Reciever_Type == 191:
         print("R750-2 ", end=" ")
         firmware_file = LancetFile
      elif Reciever_Type == 327:
         print("R780 ", end=" ")
         firmware_file = ChinstrapFile
      elif Reciever_Type == 329:
         print("R780-2 ", end=" ")
         firmware_file = ClarkFile
      elif Reciever_Type == 250:
         print("SPS585 ", end=" ")
         firmware_file = ""
         print("Not Supported")
      elif Reciever_Type == 138:
         print("SPS356 ", end=" ")
         firmware_file = ""
         print("Not Supported")
      else:
         print("Unknown Receiver Type: {}".format(Reciever_Type))

      # Update DB
      cursor.execute("UPDATE GNSS SET FIRMWARE_Version=? where id=?", (Firmware, GNSS_ID))
      conn.commit()

      if firmware_file == "" or firmware_file is None:
         print("Not Upgrading")
      else:
         print("Upgrading")

         # Construct the command
         cmd = "./upgrade_with_clone.py" +\
            " -p admin:" + str(row["Password"]) +\
            " -c GPS_"+ str(row["id"]) +\
            " -d /var/www/html/Dashboard/Clones"  +\
            " -i " +  str(row["Address"]) + ":" + str(row["Port"])  +\
            " -f " + firmwareLocation() + '/' + firmware_file +\
            " -u"

         print(cmd)

         # Execute subprocess
         # Popen in Py3 behaves similarly, strictly separating bytes/str in streams if piped.
         # Shell=True allows the string command to run.
         proc = Popen(cmd, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
         pprint(proc)
         time.sleep(2)

print("</pre>") # Closed the pre tag properly
print("</body></html>")

