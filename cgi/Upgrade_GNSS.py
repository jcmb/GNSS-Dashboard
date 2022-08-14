#!/usr/bin/python2

print "Content-Type: text/html"     # HTML is following
print                               # blank line, end of headers

import cgi
import cgitb

import sqlite3
import os
import os.path
import stat
import sys

from db_inc import *

sys.stdout.flush()
from subprocess import Popen, call


from pprint import pprint
cgitb.enable()

try:
   conn = sqlite3.connect(databaseFile())
#   print databaseFile()+ " Open\n"
except sqlite3.Error:
   print "Error opening db. " + databaseFile() +"\n"
   quit()

conn.row_factory = sqlite3.Row
cursor = conn.cursor()

form = cgi.FieldStorage()

#pprint(form)

#print form["User_ID"].value
#print "<br/>"


print "<html><head>"
print "<title>GNSS Firmware Upgrade</title>"
print "</head><body>"

if "User_ID" not in form:
    print "Internal Error: User ID not provided<br/>"
    quit(100)
else:
    User_ID=form["User_ID"].value

if "Firmware" not in form:
    print "Internal Error: Firmware not provided<br/>"
    quit(100)
else:
    Firmware_ID=form["Firmware"].value


query = 'SELECT Version, BarracudaFile, ChinstrapFile, GamelFile, MetallicaFile, RockyFile, KryptonFile FROM Firmware where type="' + Firmware_ID + '"';
cursor.execute(query);

rows = cursor.fetchone()
#print rows
Firmware=(rows[0])
BarracudaFile=rows[1]
ChinstrapFile=rows[2]
GamelFile=rows[3]
MetallicaFile=rows[4]
RockyFile=rows[5]
KryptonFile=rows[6]

print "Upgrading to firmware V" + Firmware + "<br/>"
#print os.getcwd()
query = 'SELECT * FROM GNSS where User_ID="' + User_ID + '"'

print ("<br/><pre>")

cursor.execute(query);
rows = cursor.fetchall()
for row in rows:
   if "Upgrade_" + str(row["id"]) in form:
#      print (row["name"]+", ")
      firmware_file=""
      GNSS_ID=row["id"]
      print row["name"]+ " (" + str(GNSS_ID) + ") Type: ",
      Reciever_Type = int(row["Reciever_Type"])
      if Reciever_Type == 107 :
         print "SPS852 ",
         firmware_file=GamelFile
      elif Reciever_Type == 118 :
         print "SPS855 ",
         firmware_file=GamelFile
      elif Reciever_Type == 38 :
         print "SPS850 ",
      elif Reciever_Type == 101 :
         print "SPS985 ",
         firmware_file=RockyFile
      elif Reciever_Type == 169 :
         print "SPS986 ",
         firmware_file=ChinstrapFile
      elif Reciever_Type == 188 :
         print "R750 ",
         firmware_file=BarracudaFile
      elif Reciever_Type == 250 :
         print "SPS585 ",
         firmware_file=""
      elif Reciever_Type == 138 :
         print "SPS356 ",
         firmware_file=""
      else :
         print "Unknown Receiver Type: {}".format(Reciever_Type)

      cursor.execute("UPDATE GNSS SET FIRMWARE_Version=? where id=?",(Firmware,GNSS_ID))
      conn.commit()

      if firmware_file=="" :
         print "Not Upgrading"
      else :
         print "Upgrading"
         cmd=[
            "./upgrade_with_clone.py",
            "-padmin:" + row["Password"],
            "-cGPS_"+ str(row["id"]),
            "-d/var/www/html/Dashboard/Clones",
            "-i" + row["Address"]+":"+str(row["Port"]) ,
            "-f" + firmwareLocation() + '/' + firmware_file
            ]
#         print cmd
#         Popen(cmd,stdout=None)
         call(cmd,stdout=None)
#      print ("</pre><br/>")
