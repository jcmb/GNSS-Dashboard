#!/usr/bin/python3

import cgi
import cgitb

import sqlite3
import os.path
import stat
from hashlib import pbkdf2_hmac

from db_inc import *
#execfile("db.inc.py")


from pprint import pprint
cgitb.enable()

print ("Content-Type: text/html")     # HTML is following
print ()                              # blank line, end of headers


try:
   conn = sqlite3.connect(databaseFile())
#   print databaseFile()+ " Open\n"
except sqlite3.Error:
   print ("Error opening db. " + databaseFile() +"\n")
   quit()

cursor = conn.cursor()

form = cgi.FieldStorage()

#pprint(form)

#print form["User_ID"].value
#print "<br/>"




print ("<html><head>")
print ("""<title>GNSS receiver signin</title>
<link rel="stylesheet" type="text/css" href="/Dashboard/style.css"></link>
<link rel="stylesheet" type="text/css" href="/Dashboard/tcui-styles.css">
<script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
<script src="/jquery.tablesorter.min.js"></script>
<body class="page">
<div class="container clearfix">
  <div style="padding: 10px 10px 10px 0 ;"> <a href="http://construction.trimble.com/">
        <img src="/Dashboard/trimble-logo.png" alt="Trimble Logo" id="logo"> </a>
      </div>
  <!-- end #logo-area -->
</div>
<div id="top-header-trim"></div>
<div id="content-area">
<div id="content">
<div id="main-content" class="clearfix">""")

print ("</head><body>")


if "user_name" not in form:
   print ("user name must be entered")
   quit(100)
else :
   Name=form["user_name"].value

if "password" not in form:
   print ("Password must be entered")
   quit(100)
else :
   Password=form["password"].value


cursor.execute('SELECT * from Users WHERE name=? COLLATE NOCASE',(Name,));
user_details=cursor.fetchone()
if user_details == None:
   print ("User Name or Password incorrect")
   quit(90)


#pprint (user_details)

User_ID=str(user_details[0])
salt=user_details[2]
PWHash=user_details[3]

our_app_iters = 1000  # Application specific. It is on a Pi2...

dk = pbkdf2_hmac('sha256', str.encode(Password), salt, our_app_iters)
hashed=dk.hex()


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
   print ("Password or User Name incorrect:")
   print ('<a href="/Dashboard">Try Again</a>')
   print ('<a href="/Dashboard/reset_password.html">Reset Password</a>')
else:
   print ("Logged in, ")
   print ("<p/>")
   print ("You might now of course think that you are secure, but the login screen is the only place that checks your password in the rest of the system:-(")
   print ("<p/>")
   print ("You can now:<ul>")
   print ('<li><a href="/cgi-bin/Dashboard/List_Status.php?User_ID='+User_ID+'">Receiver Dashboard</a>')
   print ('<li><a href="/Dashboard/Receiver_List.php?User_ID='+User_ID+'">View and edit receivers</a>')
   print ('<li><a href="/Dashboard/Error_List.php?User_ID='+User_ID+'">View Errors and Warnings receivers</a>')
   print ('<li><a href="/Dashboard/Receiver_Upgrade.php?User_ID='+User_ID+'">Update Reciever Firmware</a>')
   print ('<li><a href="/Dashboard/fw_upload.php?User_ID='+User_ID+'">Upload firmware</a>')
   print ('<li><a href="/Dashboard/Edit_User.php?User_ID='+User_ID+'">Edit your user details</a>')
print ('</div></div></div></body>')
print ('</html>')
