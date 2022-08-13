#!/usr/bin/python

import sqlite3
import os
import os.path
import stat

from subprocess import Popen

try:
   execfile("db.inc.py")
except :
   execfile("/usr/lib/cgi-bin/Dashboard/db.inc.py")
#from db.inc import databaseFile

from pprint import pprint

#print "Content-Type: text/html"     # HTML is following
#print                               # blank line, end of headers

try:
   conn = sqlite3.connect(databaseFile())
#   print databaseFile()+ " Open\n"
except sqlite3.Error:
   print "Error opening db. " + databaseFile() +"\n"
   quit()

conn.row_factory = sqlite3.Row
cursor = conn.cursor()

#print "<html><head>"
#print "</head><body>"

query = 'SELECT * FROM GNSS WHERE Enabled=1'

cursor.execute(query);
rows = cursor.fetchall()

"""
for row in rows:
#         print row
         cmd=[
            "/usr/lib/cgi-bin/Dashboard/upgrade_with_clone.sh",
            "-n",
            "-padmin:" + row["Password"],
            "-cGPS_"+ str(row["id"]),
            "-i" + row["Address"]+":"+str(row["Port"]) ,
            ]
         print ("<br/>")
         print cmd
#         Popen(cmd,stdout=None)
         clone=Popen(cmd)
         clone.wait()
"""



for row in rows:
         print row
         cmd=[
            "/usr/lib/cgi-bin/Dashboard/upgrade_with_clone.py",
            "--no_upgrade",
            "--clonedate",
            "--clonedir", "/var/www/clones",
            "-padmin:" + row["Password"],
            "-c" + "GPS_"+ str(row["id"]),
            "-i" + row["Address"]+":"+str(row["Port"]) ,
            ]
#         print ("<br/>")
#         print cmd
#         Popen(cmd,stdout=None)
         clone=Popen(cmd)
         clone.wait()

         cmd=[
            "/usr/lib/cgi-bin/Dashboard/Programmatic_Backup.py",
            "--no_upgrade",
            "--clonedate",
            "--clonedir", "/var/www/clones",
            "-padmin:" + row["Password"],
            "--Host" + row["Address"],
            "--Port", row["Port"],
            ]
#         print ("<br/>")
#         print cmd
#         Popen(cmd,stdout=None)
         clone=Popen(cmd)
         clone.wait()

