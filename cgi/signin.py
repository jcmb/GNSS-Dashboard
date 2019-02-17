#!/usr/bin/python
import cgi
import cgitb

import sqlite3
import os.path
import stat
import hashlib
execfile("db.inc.py")


from pprint import pprint
cgitb.enable()

print "Content-Type: text/html"     # HTML is following
print                               # blank line, end of headers


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


if "user_name" not in form:
   print "user name must be entered"
   quit(100)
else :
   Name=form["user_name"].value

if "password" not in form:
   print "Password must be entered"
   quit(100)
else :
   Password=form["password"].value


cursor.execute('SELECT * from Users WHERE name=? COLLATE NOCASE',(Name,));
user_details=cursor.fetchone()
if user_details == None:
   print "User Name or Password incorrect"
   quit(90)


#pprint (user_details)

User_ID=str(user_details[0])
salt=buffer(user_details[2])
PWHash=buffer(user_details[3])

hashed=hashlib.sha256(buffer(Password)+salt).digest()


#print "User_ID: "
#print(User_ID)
#print "<br/>"

#print "Password: "
#pprint(Password)
#print "<br/>"

#print "salt: "
#print(salt)
#print "<br/>"

#print "PWHash: "
#print(PWHash)
#print "<br/>"


#print "Hashed: "
#print(hashed)
#print "<br/>"

if str(hashed) != str(PWHash):
   print "Password or User Name incorrect:"
   print '<a href="/Dashboard">Try Again</a>'
   print '<a href="/Dashboard/reset_password.html">Reset Password</a>'
else:
   print "Logged in, "
   print "<p/>"
   print "You might now of course think that you are secure, but the login screen is the only place that checks your password in the rest of the system:-("
   print "<p/>"
   print "You can now:<ul>"
   print '<li><a href="/cgi-bin/Dashboard/List_Status.php?User_ID='+User_ID+'">Receiver Dashboard</a>'
   print '<li><a href="/Dashboard/Receiver_List.php?User_ID='+User_ID+'">View and edit receivers</a>'
   print '<li><a href="/Dashboard/Receiver_Upgrade.php?User_ID='+User_ID+'">Update Reciever Firmware</a>'
   print '<li><a href="/Dashboard/fw_upload.php?User_ID='+User_ID+'">Upload firmware</a>'
   print '<li><a href="/Dashboard/Edit_User.php?User_ID='+User_ID+'">Edit your user details</a>'
print '</body>'
print '</html>'
