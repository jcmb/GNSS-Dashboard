#!/usr/bin/env python3

import sqlite3
import os
import os.path
import stat
import datetime

from subprocess import Popen

from db_inc import *

from pprint import pprint

#print "Content-Type: text/html"     # HTML is following
#print                               # blank line, end of headers

try:
   conn = sqlite3.connect(databaseFile())
#   print (databaseFile()+ " Open\n")
except sqlite3.Error:
   print("Error opening db. " + databaseFile() +"\n")
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
         try:
            os.mkdir(wwwDir()+ "Clones/"+str(row["name"]))
         except:
            pass

         try:
             os.mkdir(wwwDir()+ "PI/"+str(row["name"]))
         except:
            pass

         cmd=[
            cgiDir() + "upgrade_with_clone.py",
            "--no_upgrade",
            "--clonedate",
            "--clonedir", wwwDir()+ "Clones/"+str(row["name"]),
            "-padmin:" + row["Password"],
            "-c" + "GPS_"+ str(row["id"]),
            "-i" + row["Address"]+":"+str(row["Port"]) ,
            ]
#         print ("<br/>")
         print(cmd)
#         Popen(cmd,stdout=None)
         clone=Popen(cmd)
         clone.wait()

         cmd=[
            cgiDir() + "Programmatic_Backup.py",
            "--Output", wwwDir()+ "PI/"+str(row["name"]+"/"+datetime.datetime.now().strftime("%Y-%m-%d")+".PI"),
            "--User", "admin",
            "--Password",  row["Password"],
            "--Host" , row["Address"],
            "--Port", str(row["Port"]),
            ]
#         print ("<br/>")
         print(cmd)
#         Popen(cmd,stdout=None)
         clone=Popen(cmd)
         clone.wait()

