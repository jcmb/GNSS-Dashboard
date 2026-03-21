#!/usr/bin/python3
import cgi
import cgitb
import sys
import sqlite3
import os.path
import stat
import subprocess
import logging
import logging.handlers
from pprint import pprint
import time

def trigger_nagios_restart(cmd_file="/usr/local/nagios/var/rw/nagios.cmd"):
    now = int(time.time())
    # Format: [<timestamp>] RESTART_PROGRAM
    command = f"[{now}] RESTART_PROGRAM\n"

    try:
        with open(cmd_file, 'w') as f:
            f.write(command)
        print("Restart command sent to Nagios pipe.")
    except IOError as e:
        print(f"Error writing to Nagios pipe: {e}")

# Setup Logging
logger = logging.getLogger('Do_Edit_GNSS')
logger.setLevel(logging.INFO)
# basicConfig handles the formatting
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)

# SysLogHandler is platform dependent, usually /dev/log on Linux
try:
    handler = logging.handlers.SysLogHandler(address='/dev/log')
    logger.addHandler(handler)
except Exception as e:
    # Fallback if /dev/log is unavailable (e.g., non-Linux dev env)
    pass

logger.info("Do_Edit_GNSS started")

# execfile is removed in Python 3. Replaced with exec(open().read())
# Ensure db.inc.py is in the same directory or python path
try:
    exec(open("db.inc.py").read())
except FileNotFoundError:
    print("Content-Type: text/html\n")
    print("Error: db.inc.py not found.")
    sys.exit(1)

# from db.inc import databaseFile # (Implicitly imported via exec above)

cgitb.enable()

print("Content-Type: text/html")     # HTML is following
print()                              # blank line, end of headers

try:
    # Assuming databaseFile() is defined in db.inc.py
    conn = sqlite3.connect(databaseFile())
except sqlite3.Error:
    print("Error opening db. " + str(databaseFile()) + "\n")
    sys.exit()

cursor = conn.cursor()
form = cgi.FieldStorage()

print("<html><head>")
print("</head><body>")

if "User_ID" not in form:
    print("Internal Error: User ID not provided<br/>")
    sys.exit(100)
else:
    User_ID = form["User_ID"].value

cursor.execute('SELECT * from Users WHERE ID=? COLLATE NOCASE', (User_ID,))
user_details = cursor.fetchone()

if user_details is None:
    print("User ID invalid")
    sys.exit(90)

User_Name = str(user_details[1])
User_Email = str(user_details[4])

Enabled = "Enabled" in form

if "GNSS_ID" not in form:
    Update = False
    print("Adding a new GNSS<br/>")
else:
    Update = True
    GNSS_ID = form["GNSS_ID"].value

if "Name" not in form:
    print("Name must be entered")
    sys.exit(100)
else:
    Name = form["Name"].value

if "Loc_Group" not in form:
    Loc_Group = ""
else:
    Loc_Group = form["Loc_Group"].value

if "Address" not in form:
    print("Address must be entered")
    sys.exit(100)
else:
    Address = form["Address"].value

if "Port" not in form:
    print("Port must be entered")
    sys.exit(100)
else:
    Port = form["Port"].value

if "Firmware" not in form:
    print("Firmware must be entered")
    sys.exit(100)
else:
    Firmware = form["Firmware"].value

if "Receiver_Type" not in form:
    print("Receiver_Type must be entered")
    sys.exit(100)
else:
    Receiver_Type = form["Receiver_Type"].value

if "Password" not in form:
    print("Password must be entered")
    sys.exit(100)
else:
    Password = form["Password"].value

if "Pos_Type" not in form:
    print("Pos_Type must be entered")
    sys.exit(100)
else:
    Pos_Type = form["Pos_Type"].value

Static = "Static" in form
LowLatency = "LowLatency" in form

if "Elev_Mask" not in form:
    print("Elev_Mask must be entered")
    sys.exit(100)
else:
    Elev_Mask = form["Elev_Mask"].value

if "PDOP" not in form:
    print("PDOP must be entered")
    sys.exit(100)
else:
    PDOP = form["PDOP"].value

if "Frequencies" not in form:
    print("Frequencies must be entered")
    sys.exit(100)
else:
    Frequencies = form["Frequencies"].value

if "BaseFollow" not in form:
    print("BaseFollow must be entered")
    sys.exit(100)
else:
    BaseFollow = form["BaseFollow"].value

GPS = "GPS" in form
GLN = "GLN" in form
GAL = "GAL" in form
BDS = "BDS" in form
QZSS = "QZSS" in form
SBAS = "SBAS" in form

Antenna = form["Antenna"].value
Measurement_Method = form["Measurement_Method"].value

if "Ant_Height" not in form:
    print("Antenna Height must be entered")
    sys.exit(100)
else:
    Ant_Height = form["Ant_Height"].value

if "Ref_Name" not in form:
    print("Reference Name must be entered")
    sys.exit(100)
else:
    Ref_Name = form["Ref_Name"].value

if "Ref_Code" not in form:
    Ref_Code = ""
else:
    Ref_Code = form["Ref_Code"].value

if "Ref_Lat" not in form:
    print("Latitude must be entered")
    sys.exit(100)
else:
    try:
        Ref_Lat = float(form["Ref_Lat"].value.strip())
    except ValueError:
        print("Latitude must be a number")
        sys.exit(100)

if "Ref_Long" not in form:
    print("Longitude must be entered")
    sys.exit(100)
else:
    try:
        Ref_Long = float(form["Ref_Long"].value.strip())
    except ValueError:
        print("Longitude must be a number")
        sys.exit(100)

if "Ref_Height" not in form:
    print("Ref Height must be entered")
    sys.exit(100)
else:
    try:
        Ref_Height = float(form["Ref_Height"].value.strip())
    except ValueError:
        print("Height must be a number")
        sys.exit(100)

if "Auth" not in form:
    print("Auth must be entered")
    sys.exit(100)
else:
    Auth = form["Auth"].value

FTP_Enabled = "FTP_Enabled" in form

if "FTP_To" not in form:
    if FTP_Enabled:
        print("FTP_To must be entered when FTP enabled")
        sys.exit(100)
    else:
        FTP_To = ""
else:
    FTP_To = form["FTP_To"].value.strip()

Logging_Enabled = "Logging_Enabled" in form

if "Logging_Duration" not in form:
    if Logging_Enabled:
        print("Logging_Duration must be entered if Logging enabled")
        sys.exit(100)
    else:
        Logging_Duration = 60
else:
    Logging_Duration = form["Logging_Duration"].value

if "Logging_Measurement_Interval" not in form:
    if Logging_Enabled:
        print("Logging_Measurement_Interval must be entered, if logging enabled")
        sys.exit(100)
    else:
        Logging_Measurement_Interval = 1
else:
    Logging_Measurement_Interval = form["Logging_Measurement_Interval"].value

if "Logging_Position_Interval" not in form:
    if Logging_Enabled:
        print("Logging_Position_Interval must be entered if logging enabled")
        sys.exit(100)
    else:
        Logging_Position_Interval = 1
else:
    Logging_Position_Interval = form["Logging_Position_Interval"].value

Email_Enabled = "Email_Enabled" in form

if "Email_To" not in form:
    if Email_Enabled:
        print("Email_To must be entered when email enabled")
        sys.exit(100)
    else:
        Email_To = ""
else:
    Email_To = form["Email_To"].value

Timed_Enabled = "Timed_Enabled" in form

if "Timed_Minimum" not in form:
    if Timed_Enabled:
        print("Timed_Minimum must be entered when Timered enabled")
        sys.exit(100)
    else:
        Timed_Minimum = 30
else:
    Timed_Minimum = form["Timed_Minimum"].value

if "Timed_Maximum" not in form:
    if Timed_Enabled:
        print("Timed_Maximum must be entered when Timed enabled")
        sys.exit(100)
    else:
        Timed_Maximum = 120
else:
    Timed_Maximum = form["Timed_Maximum"].value

Radio_Enabled = "Radio_Enabled" in form
Radio_OnOffState = "RadioOnOffState" in form

if "RadioMode" not in form:
    if Radio_Enabled:
        print("RadioMode must be entered when Radio enabled")
        sys.exit(100)
    else:
        Radio_Mode = "Base"
else:
    Radio_Mode = form["RadioMode"].value

# --- NTRIP Processing and Validation ---

ntrip_data = {}

# Process Client 1-3
for i in range(1, 4):
    enabled_key = "NTRIP_Client_{}_Enabled".format(i)
    mount_key = "NTRIP_Client_{}_Mount".format(i)

    ntrip_data[enabled_key] = enabled_key in form
    ntrip_data[mount_key] = form.getvalue(mount_key, "").strip()

    if ntrip_data[enabled_key] and not ntrip_data[mount_key]:
        print("Mountpoint must be entered when NTRIP Client {} is enabled.<br>".format(i))
        sys.exit(100)

# Process Server 1-3
for i in range(1, 4):
    enabled_key = "NTRIP_Server_{}_Enabled".format(i)
    mount_key = "NTRIP_Server_{}_Mount".format(i)
    format_key = "NTRIP_Server_{}_Format".format(i)

    ntrip_data[enabled_key] = enabled_key in form
    ntrip_data[mount_key] = form.getvalue(mount_key, "").strip()
    ntrip_data[format_key] = form.getvalue(format_key, "CMR")

    if ntrip_data[enabled_key] and not ntrip_data[mount_key]:
        print("Mountpoint must be entered when NTRIP Server {} is enabled.<br>".format(i))
        sys.exit(100)

# Process Caster 1-3
for i in range(1, 4):
    enabled_key = "NTRIP_Caster_{}_Enabled".format(i)
    mount_key = "NTRIP_Caster_{}_Mount".format(i)
    format_key = "NTRIP_Caster_{}_Format".format(i)

    ntrip_data[enabled_key] = enabled_key in form
    ntrip_data[mount_key] = form.getvalue(mount_key, "").strip()
    ntrip_data[format_key] = form.getvalue(format_key, "CMR")

    if ntrip_data[enabled_key] and not ntrip_data[mount_key]:
        print("Mountpoint must be entered when NTRIP Caster {} is enabled.<br>".format(i))
        sys.exit(100)

NAGIOS = "NAGIOS" in form

# --- DynDNS Processing ---
DynDNS_Enabled = "DynDNS_Enabled" in form

if "DynDNS_Host" not in form:
    if DynDNS_Enabled:
        print("DynDNS Hostname must be entered when DynDNS check is enabled.<br>")
        sys.exit(100)
    else:
        DynDNS_Host = ""
else:
    DynDNS_Host = form["DynDNS_Host"].value.strip()

print("<br/>")
# --- Single UPSERT Execution ---

# Pass the ID if updating, otherwise pass None to trigger SQLite Autoincrement
upsert_id = GNSS_ID if Update else None

cursor.execute('''
    INSERT INTO GNSS (
        id, User_ID, Enabled, name, Firmware, Loc_Group, Address, Port, Reciever_Type,
        Password, Pos_Type, Static, LowLatency, Elev_Mask, PDOP, Logging_Enabled,
        Logging_Duration, Logging_Measurement_Interval, Logging_Position_Interval,
        FTP_Enabled, FTP_To, Antenna, Measurement_Method, Ant_Height, Ref_Name,
        Ref_Code, Ref_Lat, Ref_Long, Ref_Height, Email_Enabled, Email_To, Auth,
        Frequencies, GPS, GLN, GAL, BDS, QZSS, SBAS, NAGIOS, TIMED_ACTIVE,
        TIMED_MIN_DELTA, TIMED_MAX_DELTA, RadioEnabled, RadioOnOffState, RadioMode,
        BASEFOLLOW,
        NTRIP_Client_1_Enabled, NTRIP_Client_1_Mount,
        NTRIP_Client_2_Enabled, NTRIP_Client_2_Mount,
        NTRIP_Client_3_Enabled, NTRIP_Client_3_Mount,
        NTRIP_Server_1_Enabled, NTRIP_Server_1_Mount, NTRIP_Server_1_Format,
        NTRIP_Server_2_Enabled, NTRIP_Server_2_Mount, NTRIP_Server_2_Format,
        NTRIP_Server_3_Enabled, NTRIP_Server_3_Mount, NTRIP_Server_3_Format,
        NTRIP_Caster_1_Enabled, NTRIP_Caster_1_Mount, NTRIP_Caster_1_Format,
        NTRIP_Caster_2_Enabled, NTRIP_Caster_2_Mount, NTRIP_Caster_2_Format,
        NTRIP_Caster_3_Enabled, NTRIP_Caster_3_Mount, NTRIP_Caster_3_Format,
        DynDNS_Enabled, DynDNS_Host
    ) VALUES (
        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
    )
    ON CONFLICT(id) DO UPDATE SET
        User_ID=excluded.User_ID,
        Enabled=excluded.Enabled,
        name=excluded.name,
        Firmware=excluded.Firmware,
        Loc_Group=excluded.Loc_Group,
        Address=excluded.Address,
        Port=excluded.Port,
        Reciever_Type=excluded.Reciever_Type,
        Password=excluded.Password,
        Pos_Type=excluded.Pos_Type,
        Static=excluded.Static,
        LowLatency=excluded.LowLatency,
        Elev_Mask=excluded.Elev_Mask,
        PDOP=excluded.PDOP,
        Logging_Enabled=excluded.Logging_Enabled,
        Logging_Duration=excluded.Logging_Duration,
        Logging_Measurement_Interval=excluded.Logging_Measurement_Interval,
        Logging_Position_Interval=excluded.Logging_Position_Interval,
        FTP_Enabled=excluded.FTP_Enabled,
        FTP_To=excluded.FTP_To,
        Antenna=excluded.Antenna,
        Measurement_Method=excluded.Measurement_Method,
        Ant_Height=excluded.Ant_Height,
        Ref_Name=excluded.Ref_Name,
        Ref_Code=excluded.Ref_Code,
        Ref_Lat=excluded.Ref_Lat,
        Ref_Long=excluded.Ref_Long,
        Ref_Height=excluded.Ref_Height,
        Email_Enabled=excluded.Email_Enabled,
        Email_To=excluded.Email_To,
        Auth=excluded.Auth,
        Frequencies=excluded.Frequencies,
        GPS=excluded.GPS,
        GLN=excluded.GLN,
        GAL=excluded.GAL,
        BDS=excluded.BDS,
        QZSS=excluded.QZSS,
        SBAS=excluded.SBAS,
        NAGIOS=excluded.NAGIOS,
        TIMED_ACTIVE=excluded.TIMED_ACTIVE,
        TIMED_MIN_DELTA=excluded.TIMED_MIN_DELTA,
        TIMED_MAX_DELTA=excluded.TIMED_MAX_DELTA,
        RadioEnabled=excluded.RadioEnabled,
        RadioOnOffState=excluded.RadioOnOffState,
        RadioMode=excluded.RadioMode,
        BASEFOLLOW=excluded.BASEFOLLOW,
        NTRIP_Client_1_Enabled=excluded.NTRIP_Client_1_Enabled,
        NTRIP_Client_1_Mount=excluded.NTRIP_Client_1_Mount,
        NTRIP_Client_2_Enabled=excluded.NTRIP_Client_2_Enabled,
        NTRIP_Client_2_Mount=excluded.NTRIP_Client_2_Mount,
        NTRIP_Client_3_Enabled=excluded.NTRIP_Client_3_Enabled,
        NTRIP_Client_3_Mount=excluded.NTRIP_Client_3_Mount,
        NTRIP_Server_1_Enabled=excluded.NTRIP_Server_1_Enabled,
        NTRIP_Server_1_Mount=excluded.NTRIP_Server_1_Mount,
        NTRIP_Server_1_Format=excluded.NTRIP_Server_1_Format,
        NTRIP_Server_2_Enabled=excluded.NTRIP_Server_2_Enabled,
        NTRIP_Server_2_Mount=excluded.NTRIP_Server_2_Mount,
        NTRIP_Server_2_Format=excluded.NTRIP_Server_2_Format,
        NTRIP_Server_3_Enabled=excluded.NTRIP_Server_3_Enabled,
        NTRIP_Server_3_Mount=excluded.NTRIP_Server_3_Mount,
        NTRIP_Server_3_Format=excluded.NTRIP_Server_3_Format,
        NTRIP_Caster_1_Enabled=excluded.NTRIP_Caster_1_Enabled,
        NTRIP_Caster_1_Mount=excluded.NTRIP_Caster_1_Mount,
        NTRIP_Caster_1_Format=excluded.NTRIP_Caster_1_Format,
        NTRIP_Caster_2_Enabled=excluded.NTRIP_Caster_2_Enabled,
        NTRIP_Caster_2_Mount=excluded.NTRIP_Caster_2_Mount,
        NTRIP_Caster_2_Format=excluded.NTRIP_Caster_2_Format,
        NTRIP_Caster_3_Enabled=excluded.NTRIP_Caster_3_Enabled,
        NTRIP_Caster_3_Mount=excluded.NTRIP_Caster_3_Mount,
        NTRIP_Caster_3_Format=excluded.NTRIP_Caster_3_Format,
        DynDNS_Enabled=excluded.DynDNS_Enabled,
        DynDNS_Host=excluded.DynDNS_Host;
''', (
    upsert_id,
    User_ID, Enabled, Name, Firmware, Loc_Group, Address, Port, Receiver_Type,
    Password, Pos_Type, Static, LowLatency, Elev_Mask, PDOP, Logging_Enabled,
    Logging_Duration, Logging_Measurement_Interval, Logging_Position_Interval,
    FTP_Enabled, FTP_To, Antenna, Measurement_Method, Ant_Height, Ref_Name,
    Ref_Code, Ref_Lat, Ref_Long, Ref_Height, Email_Enabled, Email_To, Auth,
    Frequencies, GPS, GLN, GAL, BDS, QZSS, SBAS, NAGIOS, Timed_Enabled,
    Timed_Minimum, Timed_Maximum, Radio_Enabled, Radio_OnOffState, Radio_Mode,
    BaseFollow,
    ntrip_data["NTRIP_Client_1_Enabled"], ntrip_data["NTRIP_Client_1_Mount"],
    ntrip_data["NTRIP_Client_2_Enabled"], ntrip_data["NTRIP_Client_2_Mount"],
    ntrip_data["NTRIP_Client_3_Enabled"], ntrip_data["NTRIP_Client_3_Mount"],
    ntrip_data["NTRIP_Server_1_Enabled"], ntrip_data["NTRIP_Server_1_Mount"], ntrip_data["NTRIP_Server_1_Format"],
    ntrip_data["NTRIP_Server_2_Enabled"], ntrip_data["NTRIP_Server_2_Mount"], ntrip_data["NTRIP_Server_2_Format"],
    ntrip_data["NTRIP_Server_3_Enabled"], ntrip_data["NTRIP_Server_3_Mount"], ntrip_data["NTRIP_Server_3_Format"],
    ntrip_data["NTRIP_Caster_1_Enabled"], ntrip_data["NTRIP_Caster_1_Mount"], ntrip_data["NTRIP_Caster_1_Format"],
    ntrip_data["NTRIP_Caster_2_Enabled"], ntrip_data["NTRIP_Caster_2_Mount"], ntrip_data["NTRIP_Caster_2_Format"],
    ntrip_data["NTRIP_Caster_3_Enabled"], ntrip_data["NTRIP_Caster_3_Mount"], ntrip_data["NTRIP_Caster_3_Format"],
    DynDNS_Enabled, DynDNS_Host
))
conn.commit()

# Provide user feedback and capture ID if it was newly created
if Update:
    print("Record Updated.<br>")
else:
    print("Record added<br>")
    GNSS_ID = str(cursor.lastrowid)

Nagios_FileName = "User/GNSS_" + str(GNSS_ID)

# Open for writing (text mode is default in Py3)
Nagios_File = open(Nagios_FileName + ".cfg", "w")

Nagios_File.write("# a host definition for the GNSS Receiver, Auto Generated\n")

if Enabled:
    if NAGIOS:
        if not os.path.exists("User/" + Loc_Group + ".cfg"):
            Nagios_Parent = open("User/" + Loc_Group + ".cfg", "w")
            Nagios_Parent.write("# a host definition for the GNSS Receiver parent, Auto Generated\n")
            Nagios_Parent.write("\n")
            Nagios_Parent.write("define host {\n")
            Nagios_Parent.write("   host_name " + Loc_Group + "\n")
            # Nagios_Parent.write("   address "+Address+"\n")
            Nagios_Parent.write("   alias " + Loc_Group + "\n")
            Nagios_Parent.write("   use  generic-host" + "\n")
            Nagios_Parent.write("   check_command SUCCESS\n")
            Nagios_Parent.write("   max_check_attempts 2\n")
            Nagios_Parent.write("   parents gateway\n")
            Nagios_Parent.write("   contacts " + User_Name + "\n")
            Nagios_Parent.write("    }" + "\n")
            Nagios_Parent.write("\n")
            Nagios_Parent.close()

        Nagios_File.write("\n")
        Nagios_File.write("define host {\n")
        Nagios_File.write("   use  generic-host" + "\n")
        Nagios_File.write("   host_name " + Name + "\n")
        Nagios_File.write("   alias " + Name + "\n")
        Nagios_File.write("   address " + Address + "\n")
        Nagios_File.write("   _port " + Port + "\n")
        Nagios_File.write("   check_command http_active\n")
        Nagios_File.write("   max_check_attempts 2\n")
        Nagios_File.write("   parents " + Loc_Group + "\n")
        Nagios_File.write("   contacts " + User_Name + "\n")
        Nagios_File.write("    }" + "\n")
        Nagios_File.write("\n")

        Nagios_File.write("\n")
        Nagios_File.write("define service {\n")
        Nagios_File.write("       use     generic-service\n")
        Nagios_File.write("       host_name " + Name + "\n")
        Nagios_File.write("       service_description Overview\n")
        Nagios_File.write("       check_command  sps_check_Status!" + GNSS_ID + "\n")
        Nagios_File.write("    }\n")

        NTRIP_Enabled=False

        if NTRIP_Enabled:
            Nagios_File.write("# NTRIP Enabled\n")
            Nagios_File.write("\n")
            Nagios_File.write("define service {\n")
            Nagios_File.write("       use     generic-service\n")
            Nagios_File.write("       host_name " + Name + "\n")
            Nagios_File.write("       service_description ntrip_v1_2101\n")
            Nagios_File.write("       check_command ntrip_v1!2101\n")
            Nagios_File.write("    }\n")
            Nagios_File.write("\n")
            Nagios_File.write("define service {\n")
            Nagios_File.write("       use     generic-service\n")
            Nagios_File.write("       host_name " + Name + "\n")
            Nagios_File.write("       service_description ntrip_v1_2102\n")
            Nagios_File.write("       check_command ntrip_v1!2102\n")
            Nagios_File.write("    }\n")
            Nagios_File.write("\n")
            Nagios_File.write("define service {\n")
            Nagios_File.write("       use     generic-service\n")
            Nagios_File.write("       host_name " + Name + "\n")
            Nagios_File.write("       service_description ntrip_v1_2103\n")
            Nagios_File.write("       check_command ntrip_v1!2103\n")
            Nagios_File.write("    }\n")

            Nagios_File.write("\n")
            Nagios_File.write("define service {\n")
            Nagios_File.write("       use     generic-service\n")
            Nagios_File.write("       host_name " + Name + "\n")
            Nagios_File.write("       service_description ntrip_v1_2101_mount\n")
            Nagios_File.write("       check_command ntrip_v1!2101!" + NTRIP1_Mount + "\n")
            Nagios_File.write("    }\n")

            Nagios_File.write("\n")
            Nagios_File.write("define service {\n")
            Nagios_File.write("       use     generic-service\n")
            Nagios_File.write("       host_name " + Name + "\n")
            Nagios_File.write("       service_description ntrip_v1_2102_mount\n")
            Nagios_File.write("       check_command ntrip_v1!2102!" + NTRIP2_Mount + "\n")
            Nagios_File.write("    }\n")

            Nagios_File.write("\n")
            Nagios_File.write("define service {\n")
            Nagios_File.write("       use     generic-service\n")
            Nagios_File.write("       host_name " + Name + "\n")
            Nagios_File.write("       service_description ntrip_v1_2103_mount\n")
            Nagios_File.write("       check_command ntrip_v1!2103!" + NTRIP3_Mount + "\n")
            Nagios_File.write("    }\n")

            if (NTRIP1 != "OFF") and (NTRIP1 != "DGPS"):
                Nagios_File.write("\n")
                Nagios_File.write("define service {\n")
                Nagios_File.write("       use     generic-service\n")
                Nagios_File.write("       host_name " + Name + "\n")
                Nagios_File.write("       service_description Ntrip 1 2101 Data\n")
                if NTRIP1 != "CMRp":
                    Nagios_File.write("       check_command ntrip_check_data!60!" + Address + "!2101!IBS!IBS!" + NTRIP1_Mount + "!" + NTRIP1 + "\n")
                else:
                    Nagios_File.write("       check_command ntrip_check_data!60!" + Address + "!2101!IBS!IBS!" + NTRIP1_Mount + "!CMR+\n")
                Nagios_File.write("       normal_check_interval    10\n")
                Nagios_File.write("    }\n")

            if (NTRIP2 != "OFF") and (NTRIP2 != "DGPS"):
                Nagios_File.write("\n")
                Nagios_File.write("define service {\n")
                Nagios_File.write("       use     generic-service\n")
                Nagios_File.write("       host_name " + Name + "\n")
                Nagios_File.write("       service_description Ntrip 2 2102 Data\n")
                if NTRIP2 != "CMRp":
                    Nagios_File.write("       check_command ntrip_check_data!60!" + Address + "!2102!IBS!IBS!" + NTRIP2_Mount + "!" + NTRIP2 + "\n")
                else:
                    Nagios_File.write("       check_command ntrip_check_data!60!" + Address + "!2102!IBS!IBS!" + NTRIP2_Mount + "!CMR+\n")
                Nagios_File.write("       normal_check_interval    10\n")
                Nagios_File.write("    }\n")

            if (NTRIP3 != "OFF") and (NTRIP3 != "DGPS"):
                Nagios_File.write("\n")
                Nagios_File.write("define service {\n")
                Nagios_File.write("       use     generic-service\n")
                Nagios_File.write("       host_name " + Name + "\n")
                Nagios_File.write("       service_description Ntrip 3 2103 Data\n")
                if NTRIP3 != "CMRp":
                    Nagios_File.write("       check_command ntrip_check_data!60!" + Address + "!2103!IBS!IBS!" + NTRIP3_Mount + "!" + NTRIP3 + "\n")
                else:
                    Nagios_File.write("       check_command ntrip_check_data!60!" + Address + "!2103!IBS!IBS!" + NTRIP3_Mount + "!CMR+\n")
                Nagios_File.write("       normal_check_interval    10\n")
                Nagios_File.write("    }\n")
    else:
        Nagios_File.write("# Monitoring disabled for this receiver\n")
else:
    Nagios_File.write("# Receiver is disabled\n")
    Nagios_File.write("# Enabled: {}\n".format(Enabled))

Nagios_File.close()

print("<a href=\"/Dashboard/Receiver_List.php?User_ID=" + str(User_ID) + "\">Receiver List</a>")

print("<br/><pre>")
logger.info("/usr/lib/cgi-bin/Dashboard/Status_Update.py " + str(GNSS_ID))
trigger_nagios_restart()

subprocess.Popen(["/usr/lib/cgi-bin/Dashboard/Status_Update.py", str(GNSS_ID)], stdin=None, stdout=None, stderr=None, close_fds=True)
logger.info("Finished")

# subprocess.call("service nagios reload",shell=True)
