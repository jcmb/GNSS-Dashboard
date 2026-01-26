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
import time

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


query = 'SELECT Titian_Version, AlloyFile, BarracudaFile, ChinstrapFile, KryptonFile, LancetFile, ClarkFile FROM Firmware where type="' + Firmware_ID + '"';
cursor.execute(query);

rows = cursor.fetchone()
#print rows
Firmware=(rows[0])
AlloyFile=rows[1]
BarracudaFile=rows[2]
ChinstrapFile=rows[3]
KryptonFile=rows[4]
LancetFile=rows[5]
ClarkFile=rows[6]


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
#      if Reciever_Type == 107 :
#         print "SPS852 ",
#         firmware_file=GamelFile
#      elif Reciever_Type == 118 :
#         print "SPS855 ",
#         firmware_file=GamelFile
      if Reciever_Type == 508 :
         print "BX992-MS ",
         firmware_file=KryptonFile
      elif Reciever_Type == 509 :
         print "BX992-SPS ",
         firmware_file=KryptonFile
      elif Reciever_Type == 330 :
         print "MP1086 ",
         firmware_file=KryptonFile
      elif Reciever_Type == 331 :
         print "MS1086 ",
         firmware_file=KryptonFile
      elif Reciever_Type == 164 :
         print "BD992-INS",
         firmware_file=KryptonFile
#      elif Reciever_Type == 38 :
#         print "SPS850 ",
#      elif Reciever_Type == 101 :
#         print "SPS985 ",
#         firmware_file=RockyFile
      elif Reciever_Type == 162 :
         print "Alloy ",
         firmware_file=AlloyFile
      elif Reciever_Type == 169 :
         print "SPS986 ",
         firmware_file=ChinstrapFile
      elif Reciever_Type == 188 :
         print "R750 ",
         firmware_file=BarracudaFile
      elif Reciever_Type == 191 :
         print "R750-2 ",
         firmware_file=LancetFile
      elif Reciever_Type == 193 :
         print "MPS566-2 ",
         firmware_file=LancetFile
      elif Reciever_Type == 327 :
         print "R780-0 ",
         firmware_file=ClarkFile
      elif Reciever_Type == 329 :
         print "R780-2 ",
         firmware_file=ClarkFile
#      elif Reciever_Type == 250 :
#         print "SPS585 ",
#         firmware_file=""
#      elif Reciever_Type == 138 :
#         print "SPS356 ",
#         firmware_file=""
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
            "-p" ,"admin:" + row["Password"],
#            "-c", "GPS_"+ str(row["id"]),
#            "-d", "/var/www/html/Dashboard/Clones",
            "-i", row["Address"]+":"+str(row["Port"]) ,
            "-f", firmwareLocation() + '/' + firmware_file ,
            "-u",
            "-v"
            ]

#            " -c GPS_"+ str(row["id"]) +\
#            " -d /var/www/html/Dashboard/Clones"  +\

         cmd = "./upgrade_with_clone.py" +\
            " -p admin:" + row["Password"] +\
            " -i " +  row["Address"]+":"+str(row["Port"])  +\
            " -f " + firmwareLocation() + '/' + firmware_file +\
            " -u"

         print (cmd)
#         Popen(cmd,stdout=None)
         pprint(Popen(cmd, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True))
         time.sleep(2)
#         call(cmd,stdout=None)
#      print ("</pre><br/>")
