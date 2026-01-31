#!/usr/bin/env python3
import cgi
import cgitb
import sqlite3
import os
import sys
import stat
from hashlib import pbkdf2_hmac

# Ensure db_inc.py is in the same directory or python path
from db_inc import *

cgitb.enable()

print("Content-Type: text/html")     # HTML is following
print()                               # blank line, end of headers

try:
   conn = sqlite3.connect(databaseFile())
except sqlite3.Error:
   print("Error opening db. " + str(databaseFile()) + "\n")
   sys.exit(1)

cursor = conn.cursor()

form = cgi.FieldStorage()

print("<html><head>")
print("</head><body>")

if "User_ID" not in form:
    Update = False
    print("Adding a new User<br/>")
else:
    print("Editing User<br/>")
    Update = True
    User_ID = form["User_ID"].value

if "Name" not in form:
   print("Name must be entered")
   sys.exit(100)
else:
   Name = form["Name"].value

if "Email" not in form:
   print("Email must be entered")
   sys.exit(100)
else:
   Email = form["Email"].value

if "Password" not in form:
   if not Update:
      print("Password must be entered")
      sys.exit(100)
   Password = ""
else:
   Password = form["Password"].value

our_app_iters = 1000  # Application specific.

if Update:
    if Password == "":
       cursor.execute('''UPDATE Users SET
         Name=?,
         Email=?
         WHERE id=?''', (
           Name,
           Email,
           User_ID))
       print("Record Updated")
       conn.commit()
    else:
       # Retrieve salt (expecting bytes from DB BLOB)
       cursor.execute('SELECT Salt from Users WHERE ID=?', (User_ID,))
       result = cursor.fetchone()

       if result:
           salt = result[0]

           # Password must be bytes, salt must be bytes
           dk = pbkdf2_hmac('sha256', Password.encode('utf-8'), salt, our_app_iters)
           hashed = dk.hex() # Converts hash bytes to hex string for storage

           cursor.execute('''UPDATE Users SET
             Name=?,
             Email=?,
             PWHash=?
             WHERE id=?''', (
               Name,
               Email,
               hashed,
               User_ID))
           print("Record and password Updated")
           conn.commit()
       else:
           print("Error: User not found for update.")
else:
    # Generate new salt (bytes)
    salt = os.urandom(16)

    # Password must be bytes, salt must be bytes
    dk = pbkdf2_hmac('sha256', Password.encode('utf-8'), salt, our_app_iters)
    hashed = dk.hex()

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
    User_ID = str(cursor.lastrowid)

# Writing the Nagios config file
# Ensure directory exists or catch error if needed (omitted per original logic)
Nagios_FileName = "User/User-" + Name

try:
    with open(Nagios_FileName + ".cfg", "w", encoding="utf-8") as Nagios_File:
        Nagios_File.write("# a user definition for the GNSS Receiver, Auto Generated\n")
        Nagios_File.write("define contact {\n")
        Nagios_File.write("    contact_name                    " + Name + "\n")
        Nagios_File.write("    use                             generic-contact          ; Inherit default values\n")
        Nagios_File.write("    service_notification_commands   notify-service-by-email\n")
        Nagios_File.write("    host_notification_commands      notify-host-by-email\n")
        Nagios_File.write("    email                           " + Email + " ; Contacts email address\n")
        Nagios_File.write("}\n")
except IOError as e:
    print(f"<br>Error writing configuration file: {e}<br>")

print('<a href="/Dashboard/Receiver_List.php?User_ID=' + str(User_ID) + '">Back</a>')
print('</body>')
print('</html>')
