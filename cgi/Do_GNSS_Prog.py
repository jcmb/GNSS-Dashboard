#!/usr/bin/env python3
import cgi
import cgitb
import sqlite3
import os
import sys
import stat
import urllib.request
import urllib.parse
import urllib.error
import base64

# Python 3 replacement for execfile("db.inc.py")
# We use exec() because 'db.inc.py' contains a dot and cannot be imported as a standard module.
try:
    with open("db.inc.py") as f:
        exec(f.read())
except FileNotFoundError:
    # Fallback in case the file was renamed to db_inc.py (standard python naming)
    try:
        from db_inc import *
    except ImportError:
        print("Error: Could not find database configuration file (db.inc.py).")
        sys.exit(1)

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

if "U" not in form:
    print("Internal Error: User ID (U) not provided<br/>")
    sys.exit(100)
else:
    User_ID = form["U"].value

if "G" not in form:
    print("Internal Error: GNSS ID (G) not provided<br/>")
    sys.exit(100)
else:
    GNSS_ID = form["G"].value

if "C" not in form:
   print("Internal Error: CMD (C) not in form")
   sys.exit(100)
else:
   CMD = form["C"].value

if "P" not in form:
   print("Internal Error: Params (P) not in form")
   sys.exit(100)
else:
   Params = form["P"].value

cursor.execute('SELECT id, User_ID, Address, Port, Password from GNSS WHERE (id=? and User_ID=?) ', (GNSS_ID, User_ID))
GNSS_details = cursor.fetchone()

if GNSS_details is None:
   print("Internal Error, GNSS user mismatch")
   sys.exit(90)

print("GNSS Details")

Address = str(GNSS_details[2])
Port = str(GNSS_details[3])
Password = str(GNSS_details[4])

# urllib.unquote has moved to urllib.parse.unquote in Python 3
URI = "http://" + Address + ":" + Port + "/prog/set?" + CMD + "&" + urllib.parse.unquote(Params)

# urllib2.Request has moved to urllib.request.Request
request = urllib.request.Request(URI)

# Base64 encoding for Basic Auth
# In Python 3, b64encode expects bytes and returns bytes.
auth_string = f'admin:{Password}'
auth_bytes = auth_string.encode('utf-8')       # Convert string to bytes
base64_bytes = base64.b64encode(auth_bytes)    # Encode to base64 bytes
base64_string = base64_bytes.decode('ascii')   # Decode back to string for the header

request.add_header("Authorization", "Basic %s" % base64_string)

try:
    # urllib2.urlopen has moved to urllib.request.urlopen
    with urllib.request.urlopen(request) as result:
        # result.read() returns bytes in Py3, need to decode to print
        print(result.read().decode('utf-8'))
except urllib.error.URLError as e:
    print(f"<br>Error contacting device: {e}")

print("<br/>")
print('<a href="/cgi-bin/Dashboard/User/User_Dashboard_' + str(User_ID) + '.sh">Back to Dashboard</a>')

print('</body>')
print('</html>')
