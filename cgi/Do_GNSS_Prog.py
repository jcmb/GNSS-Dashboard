#!/usr/bin/env python3
import cgi
import sqlite3
import sys
import urllib.parse
import urllib.request
import urllib.error
import base64
import ssl

try:
    from db_inc import databaseFile, open_database
except ImportError:
    with open("db.inc.py") as f:
        exec(f.read())

from gnss_security import (
    decrypt_receiver_password,
    validate_prog_command,
    validate_prog_params,
    verify_gnss_owner,
    verify_user_exists,
    receiver_url,
    gnss_use_https_enabled,
)

#cgitb.enable()

print("Content-Type: text/html")
print()

try:
   conn = open_database()
except sqlite3.Error as err:
   print("Error opening db. {}: {}\n".format(databaseFile(), err))
   sys.exit(1)

cursor = conn.cursor()
form = cgi.FieldStorage()

print("<html><head>")
print("</head><body>")

if "U" not in form:
    print("Internal Error: User ID (U) not provided<br/>")
    sys.exit(100)
User_ID = form["U"].value

if "G" not in form:
    print("Internal Error: GNSS ID (G) not provided<br/>")
    sys.exit(100)
GNSS_ID = form["G"].value

if "C" not in form:
   print("Internal Error: CMD (C) not in form")
   sys.exit(100)
CMD = form["C"].value

if "P" not in form:
   print("Internal Error: Params (P) not in form")
   sys.exit(100)
Params = form["P"].value

verify_user_exists(cursor, User_ID)
verify_gnss_owner(cursor, GNSS_ID, User_ID)

try:
    validate_prog_command(CMD)
    Params = validate_prog_params(Params)
except ValueError as exc:
    print(f"Invalid request: {exc}<br/>")
    sys.exit(400)

cursor.execute('SELECT id, User_ID, Address, Port, Password, UseHTTPS from GNSS WHERE (id=? and User_ID=?) ', (GNSS_ID, User_ID))
GNSS_details = cursor.fetchone()

if GNSS_details is None:
   print("Internal Error, GNSS user mismatch")
   sys.exit(90)

Address = str(GNSS_details[2])
Port = str(GNSS_details[3])
Password = decrypt_receiver_password(GNSS_details[4])
Use_HTTPS = gnss_use_https_enabled(GNSS_details[5])

if not re.match(r'^[0-9]+$', Port):
    print("Invalid receiver port<br/>")
    sys.exit(400)

URI = receiver_url(Address, Port, Use_HTTPS, "/prog/set?" + CMD + "&" + urllib.parse.unquote(Params))
request = urllib.request.Request(URI)

auth_string = f'admin:{Password}'
base64_string = base64.b64encode(auth_string.encode('utf-8')).decode('ascii')
request.add_header("Authorization", "Basic %s" % base64_string)

try:
    if Use_HTTPS:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        result = urllib.request.urlopen(request, timeout=30, context=ctx)
    else:
        result = urllib.request.urlopen(request, timeout=30)
    with result:
        print(result.read().decode('utf-8'))
except urllib.error.URLError as e:
    print(f"<br>Error contacting device: {e}")

print("<br/>")
print('<a href="/Dashboard/Receiver_List.php?User_ID=' + str(User_ID) + '">Back to Receiver List</a>')
print('</body></html>')
