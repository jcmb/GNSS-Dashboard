#!/usr/bin/python
import cgi
import cgitb

import sqlite3
import os.path
import stat
import hashlib
execfile("db.inc.py")
#from db.inc import databaseFile

from pprint import pprint
cgitb.enable()

print "Content-Type: text/html"     # HTML is following
print                               # blank line, end of headers

#print hashlib.algorithms

try:
   conn = sqlite3.connect(databaseFile())
#   print databaseFile()+ " Open\n"
except sqlite3.Error:
   print "Error opening db. " + databaseFile() +"\n"
   quit()

cursor = conn.cursor()

form = cgi.FieldStorage()

#pprint(form)

#print form["User_ID"].value
#print "<br/>"




print "<html><head>"
print "</head><body>"


if "User_ID" not in form:
    Update=False
    print "Adding a new User<br/>"
else :
    print "Editing User<br/>"
    Update=True
    User_ID=form["User_ID"].value

if "Name" not in form:
   print "Name must be entered"
   quit(100)
else :
   Name=form["Name"].value

if "Email" not in form:
   print "Email must be entered"
   quit(100)
else :
   Email=form["Email"].value

if "Password" not in form:
   if not Update :
      print "Password must be entered"
      quit(100)
   Password=""
else :
   Password=form["Password"].value


if Update:
    if Password == "":
       cursor.execute('''UPDATE Users SET
         Name=?,
         Email=?
         WHERE id=?''',(
           Name,
           Email,
           User_ID))
       print "Record Updated"
       conn.commit()
    else:
       cursor.execute('SELECT Salt from Users WHERE ID=?',(User_ID,));
       salt=cursor.fetchone()[0]

       hashed=hashlib.sha256(buffer(Password)+salt).digest()

       cursor.execute('''UPDATE Users SET
         Name=?,
         Email=?,
         PWHash=?
         WHERE id=?''',(
           Name,
           Email,
           buffer(hashed),
           User_ID))
       print "Record and password Updated"
       conn.commit()
else:
    salt=os.urandom(16)
#    print "salt<br/>"
#    print salt
#    print "<br/>"
    hashed=hashlib.sha256(Password+salt).digest()
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
        buffer(salt),
        buffer(hashed),
        Email
        ))
    print "Record added"
    conn.commit()
    User_ID=str(cursor.lastrowid)

print '<a href="/Dashboard/Receiver_List.php?User_ID='+User_ID+'">Back</a>'
print '</body>'
print '</html>'
