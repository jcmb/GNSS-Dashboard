#!/usr/bin/python2
import cgi
import cgitb

import sqlite3
import os.path
import stat

import subprocess

import logging
import logging.handlers

logger = logging.getLogger('Do_Edit_GNSS')

logger.setLevel(logging.INFO)
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',level=logging.DEBUG)

handler = logging.handlers.SysLogHandler(address='/dev/log')
logger.addHandler(handler)

logger.info("Do_Edit_GNSS started");

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

if "User_ID" not in form:
    print "Internal Error: User ID not provided<br/>"
    quit(100)
else:
    User_ID=form["User_ID"].value

cursor.execute('SELECT * from Users WHERE ID=? COLLATE NOCASE',(User_ID,));
user_details=cursor.fetchone()
if user_details == None:
   print "User ID invalid"
   quit(90)


#pprint (user_details)

User_Name=str(user_details[1])
User_Email=str(user_details[4])


Enabled="Enabled" in form

if "GNSS_ID" not in form:
    Update=False
    print "Adding a new GNSS<br/>"
else :
    Update=True
    GNSS_ID=form["GNSS_ID"].value

if "Name" not in form:
   print "Name must be entered"
   quit(100)
else :
   Name=form["Name"].value


if "Loc_Group" not in form:
   Loc_Group=""
else :
   Loc_Group=form["Loc_Group"].value

if "Address" not in form:
   print "Address must be entered"
   quit(100)
else :
   Address=form["Address"].value

if "Port" not in form:
   print "Port must be entered"
   quit(100)
else :
   Port=form["Port"].value

if "Firmware" not in form:
   print "Firmware must be entered"
   quit(100)
else :
   Firmware=form["Firmware"].value

if "Receiver_Type" not in form:
   print "Receiver_Type must be entered"
   quit(100)
else :
   Receiver_Type=form["Receiver_Type"].value

if "Password" not in form:
   print "Password must be entered"
   quit(100)
else :
   Password=form["Password"].value

if "Pos_Type" not in form:
   print "Pos_Type must be entered"
   quit(100)
else :
   Pos_Type=form["Pos_Type"].value

Static =  "Static" in form
LowLatency =  "LowLatency" in form

if "Elev_Mask" not in form:
   print "Elev_Mask must be entered"
   quit(100)
else :
   Elev_Mask=form["Elev_Mask"].value

if "PDOP" not in form:
   print "PDOP must be entered"
   quit(100)
else :
   PDOP=form["PDOP"].value

if "Frequencies" not in form:
   print "Frequencies must be entered"
   quit(100)
else :
   Frequencies=form["Frequencies"].value


GPS =  "GPS" in form
GLN =  "GLN" in form
GAL =  "GAL" in form
BDS =  "BDS" in form
QZSS =  "QZSS" in form
SBAS =  "SBAS" in form

Antenna=form["Antenna"].value
Measurement_Method=form["Measurement_Method"].value

if "Ant_Height" not in form:
   print "Antenna Height must be entered"
   quit(100)
else :
   Ant_Height=form["Ant_Height"].value

if "Ref_Name" not in form:
   print "Reference Name must be entered"
   quit(100)
else :
   Ref_Name=form["Ref_Name"].value

if "Ref_Code" not in form:
   Ref_Code=""
else :
   Ref_Code=form["Ref_Code"].value

if "Ref_Lat" not in form:
   print "Latitude must be entered"
   quit(100)
else :
   Ref_Lat=form["Ref_Lat"].value

if "Ref_Long" not in form:
   print "Longitude must be entered"
   quit(100)
else :
   Ref_Long=form["Ref_Long"].value

if "Ref_Height" not in form:
   print "Ref Height must be entered"
   quit(100)
else :
   Ref_Height=form["Ref_Height"].value


if "Auth" not in form:
   print "Auth must be entered"
   quit(100)
else :
   Auth=form["Auth"].value

FTP_Enabled =  "FTP_Enabled" in form

if "FTP_To" not in form:
   if FTP_Enabled:
      print "FTP_To must be entered when FTP enabled"
      quit(100)
   else:
      FTP_To=""
else :
  FTP_To=form["FTP_To"].value


Logging_Enabled =  "Logging_Enabled" in form

if "Logging_Duration" not in form:
   if Logging_Enabled:
       print "Logging_Duration must be entered if Logging enabled"
       quit(100)
   else:
       Logging_Duration=60
else :
   Logging_Duration=form["Logging_Duration"].value


if "Logging_Measurement_Interval" not in form:
   if Logging_Enabled:
      print "Logging_Measurement_Interval must be entered, if logging enabled"
      quit(100)
   else:
      Logging_Measurement_Interval=1
else :
   Logging_Measurement_Interval=form["Logging_Measurement_Interval"].value


if "Logging_Position_Interval" not in form:
   if Logging_Enabled:
      print "Logging_Position_Interval must be entered if logging enabled"
      quit(100)
   else:
      Logging_Position_Interval=1
else :
   Logging_Position_Interval=form["Logging_Position_Interval"].value

Email_Enabled =  "Email_Enabled" in form

if "Email_To" not in form:
   if Email_Enabled:
      print "Email_To must be entered when email enabled"
      quit(100)
   else:
      Email_To=""
else :
  Email_To=form["Email_To"].value



NTRIP_Enabled =  "NTRIP_Enabled" in form

NTRIP_Enabled = False

if "NTRIP1_Mount" not in form:
    if NTRIP_Enabled:
      print "NTRIP1 Mount point must be entered when NTRIP enabled"
      quit(100)
    else:
        NTRIP1_Mount=""
else:
    NTRIP1_Mount=form["NTRIP1_Mount"].value

NTRIP1="OFF"

"""
if "NTRIP1" not in form:
   print "INTERNAL Error: NTRIP1 not provided"
   quit(100)
else:
    NTRIP1=form["NTRIP1"].value
"""

if "NTRIP2_Mount" not in form:
    if NTRIP_Enabled:
      print "NTRIP2 Mount point must be entered when NTRIP enavbled"
      quit(100)
    else:
        NTRIP2_Mount=""
else:
    NTRIP2_Mount=form["NTRIP2_Mount"].value

NTRIP2="OFF"
"""
if "NTRIP2" not in form:
   print "INTERNAL Error: NTRIP2 not provided"
   quit(100)
else:
    NTRIP2=form["NTRIP2"].value
"""

if "NTRIP3_Mount" not in form:
    if NTRIP_Enabled:
      print "NTRIP3 Mount point must be entered when NTRIP enavbled"
      quit(100)
    else:
        NTRIP3_Mount=""
else:
    NTRIP3_Mount=form["NTRIP3_Mount"].value

NTRIP3="OFF"
"""
if "NTRIP3" not in form:
   print "INTERNAL Error: NTRIP3 not provided"
   quit(100)
else:
    NTRIP3=form["NTRIP3"].value
"""

IBSS_Enabled ="IBSS_Enabled" in form

IBSS_Enabled=False

if "IBSS_Org" not in form:
    if IBSS_Enabled:
      print "IBSS_Org must be entered when IBSS enabled"
      quit(100)
    else:
      IBSS_Org=""
else:
    IBSS_Org=form["IBSS_Org"].value

if "IBSS_Test_User" not in form:
    if IBSS_Enabled:
        print "IBSS_Test_User must be entered when IBSS enabled"
        quit(100)
    else:
        IBSS_Test_User=""
else:
    IBSS_Test_User=form["IBSS_Test_User"].value

if "IBSS_Test_Password" not in form:
    if IBSS_Enabled:
        print "IBSS_Test_Password must be entered when IBSS enabled"
        quit(100)
    else:
        IBSS_Test_Password=""
else:
    IBSS_Test_Password=form["IBSS_Test_Password"].value

if "IBSS_1_Mount" not in form:
    if IBSS_Enabled:
        print "IBSS_1_Mount must be entered when IBSS enabled"
        quit(100)
    else:
        IBSS_1_Mount=""
else:
    IBSS_1_Mount=form["IBSS_1_Mount"].value

if "IBSS_1" not in form:
    if IBSS_Enabled:
        print "IBSS_1_Type must be entered when IBSS enabled"
        quit(100)
    else:
        IBSS_1_Type=""
else:
    IBSS_1_Type=form["IBSS_1"].value

NAGIOS =  "NAGIOS" in form

print "<br/>"
#print "DB File: "+databaseFile()

if Update:
    cursor.execute('''UPDATE GNSS SET
      User_ID=?,
      Enabled=?,
      name=?,
      Firmware=?,
      Loc_Group=?,
      Address=?,
      Port=?,
      Reciever_Type=?,
      Password=?,
      Pos_Type=?,
      Static=?,
      LowLatency=?,
      Elev_Mask=?,
      PDOP=?,
      Logging_Enabled=?,
      Logging_Duration=?,
      Logging_Measurement_Interval=?,
      Logging_Position_Interval=?,
      FTP_Enabled=?,
      FTP_To=?,
      Antenna=?,
      Measurement_Method=?,
      Ant_Height=?,
      Ref_Name=?,
      Ref_Code=?,
      Ref_Lat=?,
      Ref_Long=?,
      Ref_Height=?,
      Email_Enabled=?,
      Email_To=?,
      Auth=?,
      NTRIP_Enabled=?,
      NTRIP_1_Mount=?,
      NTRIP_1_Type=?,
      NTRIP_2_Mount=?,
      NTRIP_2_Type=?,
      NTRIP_3_Mount=?,
      NTRIP_3_Type=?,
      IBSS_Enabled=?,
      IBSS_Org=?,
      IBSS_Test_User=?,
      IBSS_Test_Password=?,
      IBSS_1_Mount=?,
      IBSS_1_Type=?,
      Frequencies=?,
      GPS=?,
      GLN=?,
      GAL=?,
      BDS=?,
      QZSS=?,
      SBAS=?,
      NAGIOS=?
      WHERE id=?''',(
        User_ID,
        Enabled,
        Name,
        Firmware,
        Loc_Group,
        Address,
        Port,
        Receiver_Type,
        Password,
        Pos_Type,
        Static,
        LowLatency,
        Elev_Mask,
        PDOP,
        Logging_Enabled,
        Logging_Duration,
        Logging_Measurement_Interval,
        Logging_Position_Interval,
        FTP_Enabled,
        FTP_To,
        Antenna,
        Measurement_Method,
        Ant_Height,
        Ref_Name,
        Ref_Code,
        Ref_Lat,
        Ref_Long,
        Ref_Height,
        Email_Enabled,
        Email_To,
        Auth,
        NTRIP_Enabled,
        NTRIP1_Mount,        NTRIP1,
        NTRIP2_Mount,        NTRIP2,
        NTRIP3_Mount,        NTRIP3,
        IBSS_Enabled,
        IBSS_Org,
        IBSS_Test_User,
        IBSS_Test_Password,
        IBSS_1_Mount,       IBSS_1_Type,
        Frequencies,
        GPS,
        GLN,
        GAL,
        BDS,
        QZSS,
        SBAS,
        NAGIOS,
        GNSS_ID))
    print "Record Updated"
    conn.commit()
else:
    cursor.execute('''INSERT INTO GNSS (
      User_ID,
      Enabled,
      name,
      Firmware,
      Loc_Group,
      Address,
      Port,
      Reciever_Type,
      Password,
      Pos_Type,
      Static,
      LowLatency,
      Elev_Mask,
      PDOP,
      Logging_Enabled,
      Logging_Duration,
      Logging_Measurement_Interval,
      Logging_Position_Interval,
      FTP_Enabled,
      FTP_To,
      Antenna,
      Measurement_Method,
      Ant_Height,
      Ref_Name,
      Ref_Code,
      Ref_Lat,
      Ref_Long,
      Ref_Height,
      Email_Enabled,
      Email_To,
      Auth,
      NTRIP_Enabled,
      NTRIP_1_Mount,       NTRIP_1_Type,
      NTRIP_2_Mount,       NTRIP_2_Type,
      NTRIP_3_Mount,       NTRIP_3_Type,
      IBSS_Enabled,
      IBSS_Org,
      IBSS_Test_User,      IBSS_Test_Password,
      IBSS_1_Mount,        IBSS_1_Type,
      Frequencies,
      GPS,
      GLN,
      GAL,
      BDS,
      QZSS,
      SBAS,
      NAGIOS )
      VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (
        User_ID,
        Enabled,
        Name,
        Firmware,
        Loc_Group,
        Address,
        Port,
        Receiver_Type,
        Password,
        Pos_Type,
        Static,
        LowLatency,
        Elev_Mask,
        PDOP,
        Logging_Enabled,
        Logging_Duration,
        Logging_Measurement_Interval,
        Logging_Position_Interval,
        FTP_Enabled,
        FTP_To,
        Antenna,
        Measurement_Method,
        Ant_Height,
        Ref_Name,
        Ref_Code,
        Ref_Lat,
        Ref_Long,
        Ref_Height,
        Email_Enabled,
        Email_To,
        Auth,
        NTRIP_Enabled,
        NTRIP1_Mount,
        NTRIP1,
        NTRIP2_Mount,
        NTRIP2,
        NTRIP3_Mount,
        NTRIP3,
        IBSS_Enabled,
        IBSS_Org,
        IBSS_Test_User,
        IBSS_Test_Password,
        IBSS_1_Mount,
        IBSS_1_Type,
        Frequencies,
        GPS,
        GLN,
        GAL,
        BDS,
        QZSS,
        SBAS,
        NAGIOS))
    print "Record added"
    conn.commit()
    GNSS_ID=str(cursor.lastrowid)


Nagios_FileName="User/GNSS_"+str(GNSS_ID)

Nagios_File=open(Nagios_FileName+".cfg","w")

Nagios_File.write("# a host definition for the GNSS Receiver, Auto Generated\n")

if Enabled:
    if NAGIOS:
        Nagios_Parent=open("User/"+Loc_Group+".cfg","w")
        Nagios_Parent.write("# a host definition for the GNSS Receiver parent, Auto Generated\n")

        Nagios_Parent.write("\n");
        Nagios_Parent.write("define host {\n")
        Nagios_Parent.write("   host_name "+ Loc_Group +"\n")
        Nagios_Parent.write("   alias "+ Loc_Group+"\n")
#        Nagios_Parent.write("   address "+Address+"\n")
        Nagios_Parent.write("   use  generic-host"+"\n")
        Nagios_Parent.write("   check_command SUCCESS\n")
        Nagios_Parent.write("   max_check_attempts 2\n")
        Nagios_Parent.write("   parents gateway\n")
        Nagios_Parent.write("   contacts " + User_Name +"\n")

        Nagios_Parent.write("    }"+"\n")
        Nagios_Parent.write("\n");

        Nagios_Parent.close()

        Nagios_File.write("\n");
        Nagios_File.write("define host {\n")
        Nagios_File.write("   host_name "+ Name+"\n")
        Nagios_File.write("   alias "+ Name+"\n")
        Nagios_File.write("   address "+Address+"\n")
        Nagios_File.write("   _port "+Port+"\n")
        Nagios_File.write("   check_command http_active\n")
        Nagios_File.write("   max_check_attempts 2\n")
        Nagios_File.write("   parents "+Loc_Group+"\n")
        Nagios_File.write("   contacts " + User_Name +"\n")

        Nagios_File.write("    }"+"\n")
        Nagios_File.write("\n");

        Nagios_File.write("\n");
        Nagios_File.write("define service {\n");
        Nagios_File.write("       use     generic-service\n");
        Nagios_File.write("       host_name "+ Name+"\n");
        Nagios_File.write("       service_description Overview\n");
        Nagios_File.write("       check_command  sps_check_Status!"+GNSS_ID+"\n")
        Nagios_File.write("    }\n");

        if NTRIP_Enabled:
           Nagios_File.write("# NTRIP Enabled\n")
           Nagios_File.write("\n")
           Nagios_File.write("define service {\n")
           Nagios_File.write("       use     generic-service\n")
           Nagios_File.write("       host_name "+ Name+"\n")
           Nagios_File.write("       service_description ntrip_v1_2101\n")
           Nagios_File.write("       check_command ntrip_v1!2101\n")
           Nagios_File.write("    }\n");
           Nagios_File.write("\n");
           Nagios_File.write("define service {\n");
           Nagios_File.write("       use     generic-service\n");
           Nagios_File.write("       host_name "+ Name+"\n");
           Nagios_File.write("       service_description ntrip_v1_2102\n")
           Nagios_File.write("       check_command ntrip_v1!2102\n");
           Nagios_File.write("    }\n");
           Nagios_File.write("\n");
           Nagios_File.write("define service {\n")
           Nagios_File.write("       use     generic-service\n")
           Nagios_File.write("       host_name "+ Name+"\n");
           Nagios_File.write("       service_description ntrip_v1_2103\n");
           Nagios_File.write("       check_command ntrip_v1!2103\n");
           Nagios_File.write("    }\n");

           Nagios_File.write("\n");
           Nagios_File.write("define service {\n");
           Nagios_File.write("       use     generic-service\n");
           Nagios_File.write("       host_name "+ Name+"\n")
           Nagios_File.write("       service_description ntrip_v1_2101_mount\n")
           Nagios_File.write("       check_command ntrip_v1!2101!"+NTRIP1_Mount+"\n");
           Nagios_File.write("    }\n");

           Nagios_File.write("\n")
           Nagios_File.write("define service {\n")
           Nagios_File.write("       use     generic-service\n")
           Nagios_File.write("       host_name "+ Name+"\n")
           Nagios_File.write("       service_description ntrip_v1_2102_mount\n")
           Nagios_File.write("       check_command ntrip_v1!2102!"+NTRIP2_Mount+"\n")
           Nagios_File.write("    }\n")

           Nagios_File.write("\n")
           Nagios_File.write("define service {\n")
           Nagios_File.write("       use     generic-service\n")
           Nagios_File.write("       host_name "+ Name+"\n")
           Nagios_File.write("       service_description ntrip_v1_2103_mount\n")
           Nagios_File.write("       check_command ntrip_v1!2103!"+NTRIP3_Mount+"\n")
           Nagios_File.write("    }\n")


           if (NTRIP1 != "OFF" ) and (NTRIP1 !="DGPS" ):
              Nagios_File.write("\n")
              Nagios_File.write("define service {\n")
              Nagios_File.write("       use     generic-service\n")
              Nagios_File.write("       host_name "+ Name+"\n")
              Nagios_File.write("       service_description Ntrip 1 2101 Data\n")
              if NTRIP1 != "CMRp" :
                 Nagios_File.write("       check_command ntrip_check_data!60!"+Address+"!2101!IBS!IBS!"+NTRIP1_Mount+"!"+NTRIP1+"\n")
              else:
                 Nagios_File.write("       check_command ntrip_check_data!60!"+Address+"!2101!IBS!IBS!"+NTRIP1_Mount+"!CMR+\n")
              Nagios_File.write("       normal_check_interval    10\n")
              Nagios_File.write("    }\n");

           if (NTRIP2 != "OFF" ) and (NTRIP2 !="DGPS" ):
              Nagios_File.write("\n")
              Nagios_File.write("define service {\n")
              Nagios_File.write("       use     generic-service\n")
              Nagios_File.write("       host_name "+ Name+"\n")
              Nagios_File.write("       service_description Ntrip 2 2102 Data\n")
              if NTRIP2 != "CMRp" :
                 Nagios_File.write("       check_command ntrip_check_data!60!"+Address+"!2102!IBS!IBS!"+NTRIP2_Mount+"!"+NTRIP2+"\n")
              else:
                 Nagios_File.write("       check_command ntrip_check_data!60!"+Address+"!2102!IBS!IBS!"+NTRIP2_Mount+"!CMR+\n")
              Nagios_File.write("       normal_check_interval    10\n")
              Nagios_File.write("    }\n");

           if (NTRIP3 != "OFF" ) and (NTRIP3 !="DGPS" ):
              Nagios_File.write("\n")
              Nagios_File.write("define service {\n")
              Nagios_File.write("       use     generic-service\n")
              Nagios_File.write("       host_name "+ Name+"\n")
              Nagios_File.write("       service_description Ntrip 3 2103 Data\n")
              if NTRIP3 != "CMRp" :
                 Nagios_File.write("       check_command ntrip_check_data!60!"+Address+"!2103!IBS!IBS!"+NTRIP3_Mount+"!"+NTRIP3+"\n")
              else:
                 Nagios_File.write("       check_command ntrip_check_data!60!"+Address+"!2103!IBS!IBS!"+NTRIP3_Mount+"!CMR+\n")
              Nagios_File.write("       normal_check_interval    10\n")
              Nagios_File.write("    }\n");
    else:
        Nagios_File.write("# Monitoring disabled for this receiver\n")
else:
    Nagios_File.write("# Receiver is disabled\n")
    Nagios_File.write("# Enabled: {}\n".format(Enabled))

Nagios_File.close();

print "<a ref=\"/Dashboard/Receiver_List.php?User_ID=" + str(User_ID) + "\">Receiver List</a>"

print "<br/><pre>"
logger.info("/usr/lib/cgi-bin/Dashboard/Status_Update.py "+ str(GNSS_ID))

#subprocess.call("/usr/lib/cgi-bin/Dashboard/Status_Update.py " + str(GNSS_ID) ,shell=True)
#subprocess.Popen(["/usr/lib/cgi-bin/Dashboard/Status_Update.py",str(GNSS_ID)]).pid
subprocess.Popen(["/usr/lib/cgi-bin/Dashboard/Status_Update.py",str(GNSS_ID)],stdin=None, stdout=None, stderr=None, close_fds=True)
logger.info("Finished");

#subprocess.call("service nagios reload",shell=True)
