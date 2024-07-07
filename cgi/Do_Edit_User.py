#!/usr/bin/python
import cgi
import cgitb

import sqlite3
import os.path
import stat
#import hashlib
from hashlib import pbkdf2_hmac

from db_inc import *

from pprint import pprint
cgitb.enable()

print("Content-Type: text/html")     # HTML is following
print()                               # blank line, end of headers

#print hashlib.algorithms

try:
   conn = sqlite3.connect(databaseFile())
#   print databaseFile()+ " Open\n"
except sqlite3.Error:
   print("Error opening db. " + databaseFile() +"\n")
   quit()

cursor = conn.cursor()

form = cgi.FieldStorage()

#pprint(form)

#print form["User_ID"].value
#print "<br/>"




print("<html><head>")
print("</head><body>")


if "User_ID" not in form:
    Update=False
    print("Adding a new User<br/>")
else :
    print("Editing User<br/>")
    Update=True
    User_ID=form["User_ID"].value

if "Name" not in form:
   print("Name must be entered")
   quit(100)
else :
   Name=form["Name"].value

if "Email" not in form:
   print("Email must be entered")
   quit(100)
else :
   Email=form["Email"].value

if "Password" not in form:
   if not Update :
      print("Password must be entered")
      quit(100)
   Password=""
else :
   Password=form["Password"].value

our_app_iters = 1000  # Application specific. It is on a Pi2...

if Update:
    if Password == "":
       cursor.execute('''UPDATE Users SET
         Name=?,
         Email=?
         WHERE id=?''',(
           Name,
           Email,
           User_ID))
       print("Record Updated")
       conn.commit()
    else:
       cursor.execute('SELECT Salt from Users WHERE ID=?',(User_ID,));
       salt=cursor.fetchone()[0]

       our_app_iters = 1000  # Application specific, read above.
       dk = pbkdf2_hmac('sha256', str.encode(Password), salt, our_app_iters)
       hashed=dk.hex()
#       hashed=hashlib.sha256(buffer(Password)+salt).digest()

       cursor.execute('''UPDATE Users SET
         Name=?,
         Email=?,
         PWHash=?
         WHERE id=?''',(
           Name,
           Email,
           hashed,
           User_ID))
       print("Record and password Updated")
       conn.commit()
else:
    salt=os.urandom(16)
#    print "salt<br/>"
#    print salt
#    print "<br/>"

    dk = pbkdf2_hmac('sha256', str.encode(Password), salt, our_app_iters)
    hashed=dk.hex()
#    hashed=hashlib.sha256(Password+salt).digest()
#    print "hashed<br/>"
#    print hashed
#      print "<br/>"
    cursor.execute('''INSERT INTO Users (
      Name,
      Salt,
      PWHash,
      Email )
      VALUES (?,?,?,?)''', (
        Name,
        salt,
        hashed,
        Email
        ))
    print("Record added")
    conn.commit()
    User_ID=str(cursor.lastrowid)

Nagios_FileName="User/User-"+Name

Nagios_File=open(Nagios_FileName+".cfg","w")

Nagios_File.write("# a user definition for the GNSS Receiver, Auto Generated\n")

Nagios_File.write("define contact {\n")
Nagios_File.write("    contact_name                    " + Name +"\n")
Nagios_File.write("    use                             generic-contact          ; Inherit default values from generic-contact template (defined above)\n")
Nagios_File.write("    service_notification_commands   notify-service-by-email\n")
Nagios_File.write("    host_notification_commands      notify-host-by-email\n")
Nagios_File.write("    email                           " + Email + " ; Contacts email address\n")
Nagios_File.write("}\n")


print('<a href="/Dashboard/Receiver_List.php?User_ID='+User_ID+'">Back</a>')
print('</body>')
print('</html>')
