#!/usr/bin/python
import cgi
import cgitb
#import httplib2
import sqlite3
import os.path
import stat
import urllib
import urllib2
import base64


execfile("db.inc.py")
#from db.inc import databaseFile

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

if "U" not in form:
    print "Internal Error: User ID (U) not provided<br/>"
    quit(100)
#    User_ID="1"
else :
    User_ID=form["U"].value

if "G" not in form:
    print "Internal Error: GNSS ID (G) not provided<br/>"
    quit(100)
#    GNSS_ID="1"
else:
    GNSS_ID=form["G"].value

if "C" not in form:
   print "Internal Error: CMD (C) not in form"
   quit(100)
#   CMD="fred"
else:
   CMD=form["C"].value

if "P" not in form:
   print "Internal Error: Params (P) not in form"
   quit(100)
#   CMD="fred"
else:
   Params=form["P"].value

cursor.execute('SELECT id, User_ID, Address,Port, Password from GNSS WHERE (id=? and User_ID=?) ',(GNSS_ID, User_ID));
GNSS_details=cursor.fetchone()
if GNSS_details == None:
   print "Internal Error, GNSS user mismatch"
   quit(90)

print "GNSS Details"
#pprint (GNSS_details)

Address=str(GNSS_details[2])
Port=str(GNSS_details[3])
Password=str(GNSS_details[4])

URI="http://"+Address+":"+Port+"/prog/set?"+CMD+"&"+urllib.unquote(Params)
#URI="http://admin:"+Password+"@"+Address+":"+Port+"/prog/set?"+CMD+"&"+Params

#print URI
#print "<br/>"
#print "<br/>"

request = urllib2.Request(URI)
base64string = base64.encodestring('%s:%s' % ('admin', Password)).replace('\n', '')
request.add_header("Authorization", "Basic %s" % base64string)
result = urllib2.urlopen(request)
print (result.read())
#h = httplib2.Http()
#h.add_credentials('admin', Password)
#resp, content = h.request(URI, "GET")
#print resp
#print resp['status']
#print content
print "<br/>"
print '<a href="/cgi-bin/Dashboard/User/User_Dashboard_' + User_ID +'.sh">Back to Dashboard</a>'
