#! /usr/bin/env python2
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')


# Rewrite of the SPS Dashboard tools into python and instead of writing the HTML it writes to the database
import cgitb
#cgitb.enable(display=0, logdir="/var/www/Crashes")

import argparse
#import urllib2
import sqlite3
import os.path
import stat
#import base64
import requests
import datetime
import logging
import logging.handlers

logger = logging.getLogger('Status_Update')
logger.setLevel(logging.ERROR)
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')

handler = logging.handlers.SysLogHandler(address='/dev/log')
logger.addHandler(handler)
#logger.removeHandler(logger.handlers[0])
#logger.propagate = False

#logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',level=logging.INFO)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger('requests').addHandler(logging.NullHandler())

import xml.etree.ElementTree as ET
import re

from pprint import pprint

parser = argparse.ArgumentParser()
parser.add_argument("GNSS_ID")
args=parser.parse_args()

execfile("/usr/lib/cgi-bin/Dashboard/db.inc.py")

#print databaseFile()

class DB_Class:

    def __init__(self):
        self.conn=None
        pass;

    def open (self):

        try:
           fd = os.open(databaseFile(), os.O_RDONLY)
           self.conn = sqlite3.connect('/dev/fd/%d' % fd)
           os.close(fd)
#           self.conn = sqlite3.connect(databaseFile())
        #   print databaseFile()+ " Open\n"
        except sqlite3.Error:
           print "Error opening db. " + databaseFile() +"\n"
           quit()

        self.conn.row_factory = sqlite3.Row
        self.GNSS   = self.conn.cursor()
        self.STATUS = self.conn.cursor()
        self.FIRMWARE = self.conn.cursor()

    def read_Firmware_configuration (self):
        query = 'SELECT * FROM Firmware'
        self.FIRMWARE.execute(query);
        row = self.FIRMWARE.fetchone()
        vers={}
        while (row != None):
#           pprint(row)
#           pprint(tuple(row))
           vers[row["Type"]]=(row["Version"],row["Titian_Version"])
           row = self.FIRMWARE.fetchone()
#        pprint(vers)
        return(vers)


    def read_GNSS_configuration (self,GNSS_ID):
        query = 'SELECT * FROM GNSS where id="' + str(GNSS_ID) + '"'
        self.GNSS.execute(query);

        row = self.GNSS.fetchone()
#        pprint(row.keys())

        self.User_Name="admin"
        self.Enabled=row["Enabled"]
        self.GNSS_ID=row["id"]
        self.Password=row["Password"]
        self.Address=row["Address"]
        self.Port=row["Port"]
        self.Enabled=row["Enabled"]
        self.User_ID=row["User_ID"]
        self.name=row["name"]
        self.Firmware=row["Firmware"]
        self.Reciever_Type=row["Reciever_Type"]
        self.Password=row["Password"]
        self.Pos_Type=row["Pos_Type"]
        self.Static=row["Static"]
        self.LowLatency=row["LowLatency"]
        self.Elev_Mask=row["Elev_Mask"]
        self.PDOP=row["PDOP"]
        self.Logging_Enabled=row["Logging_Enabled"]==1
        self.Logging_Duration=row["Logging_Duration"]
        self.Logging_Measurement_Interval=row["Logging_Measurement_Interval"]
        self.Logging_Position_Interval=row["Logging_Position_Interval"]
        self.FTP_Enabled=row["FTP_Enabled"]==1
        self.FTP_To=row["FTP_To"]
        self.Antenna=row["Antenna"]
        self.Measurement_Method=row["Measurement_Method"]
        self.Ant_Height=row["Ant_Height"]
        self.Email_Enabled=row["Email_Enabled"]==1
        self.Email_To=row["Email_To"]
        self.Auth=row["Auth"]
        self.NTRIP_Enabled=row["NTRIP_Enabled"]==1
        self.NTRIP_1_Mount=row["NTRIP_1_Mount"]
        self.NTRIP_1_Type=row["NTRIP_1_Type"]
        self.NTRIP_2_Mount=row["NTRIP_2_Mount"]
        self.NTRIP_2_Type=row["NTRIP_2_Type"]
        self.NTRIP_3_Mount=row["NTRIP_3_Mount"]
        self.NTRIP_3_Type=row["NTRIP_3_Type"]
        self.IBSS_Enabled=row["IBSS_Enabled"]==1
        self.IBSS_Org=row["IBSS_Org"]
        self.IBSS_Test_User=row["IBSS_Test_User"]
        self.IBSS_Test_Password=row["IBSS_Test_Password"]
        self.IBSS_1_Mount=row["IBSS_1_Mount"]
        self.IBSS_1_Type=row["IBSS_1_Type"]

        self.Frequencies=row["Frequencies"]
        self.GPS=row["GPS"]
        self.GLN=row["GLN"]==1
        self.GAL=row["GAL"]==1
        self.BDS=row["BDS"]==1
        self.QZSS=row["QZSS"]==1
        self.SBAS=row["SBAS"]==1

        self.Ref_Lat=row["Ref_Lat"]
        self.Ref_Long=row["Ref_Long"]
        self.Ref_Height=row["Ref_Height"]
        self.Ref_Name=row["Ref_Name"]
        self.Ref_Code=row["Ref_Code"]

        if self.Ref_Name:
            self.Ref_Name=self.Ref_Name.upper()

        if self.Ref_Code:
            self.Ref_Code=self.Ref_Code.upper()

        self.Timed_Active=row["TIMED_ACTIVE"]==1
        self.Timed_Delta_Min=row["TIMED_MIN_DELTA"]
        self.Timed_Delta_Max=row["TIMED_MAX_DELTA"]


class HTTP_Class:
    def __init__(self,Host,Port,User_Name,Password,TimeOut):
        self.Ses = requests.Session()
        self.Ses.auth = (User_Name, Password)
        self.Host=Host
        self.Port=Port
        self.TimeOut=TimeOut

    def get(self,url_part):
        try:
#            print "http://" + self.Host + ":" + str(self.Port) + url_part
#            pprint (self.Ses)
            Response=self.Ses.get("http://" + self.Host + ":" + str(self.Port) + url_part,timeout=self.TimeOut)
            if Response.status_code != 200:
                reply=None
            else:
                reply=Response.text
            return (reply,Response.status_code)
        except:
            return (None,0)


def STATUS_Update_Check (DB,GNSS_ID,Enabled):
    if not Enabled:
        logger.warning(DB.Address+":"+str(DB.Port)+ " Disabled: ")
        DB.STATUS.execute("DELETE FROM STATUS WHERE id = ? ",(GNSS_ID,))
        DB.STATUS.execute("INSERT or REPLACE into STATUS (id,Checked,Last_Check) VALUES (?,?,?)",(GNSS_ID,False,datetime.datetime.now()))
        DB.conn.commit()
        return (False)
    else:
        logger.debug(DB.Address+":"+str(DB.Port)+ " Enabled: " )
        DB.STATUS.execute("DELETE FROM STATUS WHERE id = ? ",(GNSS_ID,))
        DB.STATUS.execute("INSERT or REPLACE into STATUS (id,Checked,Last_Check) VALUES (?,?,?)",(GNSS_ID,True,datetime.datetime.now()))
        DB.conn.commit()
        return (True)



def check_firmware_and_password(GNSS_ID,DB,HTTP):

#todo move the password checking into a place that works with enabled with anonymous and make it a seperate sub

    Firmware_Version_Base=0.0
    (reply,result)=HTTP.get("/prog/show?firmwareVersion")

    if reply:
        version=""
        m=re.search(" pendingVersion=(\d*\.\d*) ",reply)
        if m:
#            print "Pending", m.group(0)
#            print "Pending", m.group(1)
            Firmware_Version_Base=float(1)
            Firmware_Version=m.group(1)+"-"
            m=re.search(" version=\d*\.(\d*) ",reply)
            if m:
#                print "version", m.group(0)
                Firmware_Version+=m.group(1)
        else:
            m=re.search(" version=(\d*\.\d*) ",reply)
            if m:
                Firmware_Version=m.group(1)
                Firmware_Version_Base=float(1)
            else:
                logger.info(DB.Address+":"+str(DB.Port)+" ERROR: Programatic Interface not installed")
                print "ERROR: Programatic interface not installed "
                quit(2)

        m=re.search(" date=(\d*-\d*-\d*)",reply)
        if m :
            Firmware_Date=m.group(1)
        else:
            Firmware_Date="N/A"

#        print Firmware_Version,Firmware_Date
        DB.STATUS.execute("UPDATE STATUS SET Firmware_Version=?, Firmware_Date=?, Password_Valid=? where id=?",(Firmware_Version,Firmware_Date,True,GNSS_ID))
        DB.STATUS.execute("UPDATE STATUS SET Password_Valid=? where id=?",(True,GNSS_ID))
        DB.STATUS.execute("UPDATE STATUS SET Alive=? where id=?",(True,GNSS_ID))
        DB.conn.commit()

        return Firmware_Version_Base

    else:
        DB.STATUS.execute("UPDATE STATUS SET Alive=? where id=?",(False,GNSS_ID))
        if result==401 :
            logger.warning(DB.Address+":"+str(DB.Port)+ " has wrong password")
            DB.STATUS.execute("UPDATE STATUS SET Password_Valid=? where id=?",(False,GNSS_ID))
            DB.conn.commit()

        logger.warning(DB.Address+":"+str(DB.Port)+ " Alive:: " + str(result != 0))

        DB.STATUS.execute("UPDATE STATUS SET Alive=? where id=?",(result != 0,GNSS_ID))
        DB.conn.commit()
        return False

def check_firmware(GNSS_ID,FirmwareVersions,DB,HTTP):

    Firmware_Version_Base=0.0
    (reply,result)=HTTP.get("/prog/show?firmwareVersion")

    if reply:
        version=""
        m=re.search(" pendingVersion=(\d*\.\d*) ",reply)
        if m:
            Firmware_Version=m.group(1)+"-"
            m=re.search(" version=\d*\.(\d*) ",reply)
            if m:
                Firmware_Version+=m.group(1)
        else:
            m=re.search(" version=(\d*\.\d*) ",reply)
            if m:
                Firmware_Version=m.group(1)

    firmwareValid=True
    Message=""
    firmwareType=0

    if (DB.Reciever_Type == "162"):
        firmwareType=1

    if (DB.Reciever_Type == "169"):
        firmwareType=1

    if (DB.Reciever_Type == "188"):
        firmwareType=1

    if (DB.Reciever_Type == "189"):
        firmwareType=1

    if (DB.Reciever_Type == "507"):
        firmwareType=1

    if (DB.Reciever_Type == "509"):
        firmwareType=1


#    print (DB.Reciever_Type)
#    print (firmwareType)
    if (DB.Firmware in FirmwareVersions) :
#        pprint(FirmwareVersions[DB.Firmware])
        firmwareValid= Firmware_Version == FirmwareVersions[DB.Firmware][firmwareType]
        Message="Receiver Firmware is " + Firmware_Version + " Should be " + FirmwareVersions[DB.Firmware][firmwareType] + " Ring " + DB.Firmware + "\n";

    return(firmwareValid,Message)


def check_serial_and_type(GNSS_ID,DB,HTTP):
    SerialNumber="N/A"
    rxType="N/A"
    rxValid=False
    Message=""

    (reply,result)=HTTP.get("/prog/show?SerialNumber")

#    print reply
    if reply:
        m=re.search("SerialNumber sn=(.*) *rxType='(.*),.*,(.*)'",reply)
        if m:
            SerialNumber=m.group(1)
            rxType=m.group(2)
            rxTypeName=m.group(3)
            rxValid=(DB.Reciever_Type==rxType);
            if not rxValid:
                Message="Receiver Type is " + rxType + " ("+ rxTypeName + ") Should be " +DB.Reciever_Type +"\n";
                logger.debug(DB.Address+":"+str(DB.Port)+ " Receiver Type: " + DB.Reciever_Type + " Current: " + rxType + " Rx Type Valid: " + str(rxValid))
        else :
            m=re.search("SerialNumber sn=(.*)",reply)
            if m:
                SerialNumber=m.group(1)
                rxValid=True
            else:
                logger.warning(DB.Address+":"+str(DB.Port)+ " Could not determine serial number")

    logger.debug(DB.Address+":"+str(DB.Port)+ " Serial_Number: "  + str(SerialNumber) +" Reciever_Type: " + str(rxType) + " Reciever_Type_Valid: " + str(rxValid))
    DB.STATUS.execute("UPDATE STATUS SET Serial_Number=?, Reciever_Type=?, Reciever_Type_Valid=? where id=?",(SerialNumber,rxType,rxValid,GNSS_ID))
    DB.conn.commit()
    return(rxValid,Message)



def check_position_type(GNSS_ID,DB,HTTP):
    current_pos="N/A"
    Pos_Type_Valid=False
    Message="Position Type could not be determined\n";

    (reply,result)=HTTP.get("/prog/show?position")

#    print reply
    if reply:
        found_pos=False
        for line in reply.split('\n'):
#            print line
            m=re.search('Qualifiers *(.*)',line)
            if m:
                current_pos=m.group(1)
                found_pos=True
#                print current_pos
                m=re.search(DB.Pos_Type,current_pos)
                if m:
                    Pos_Type_Valid=True
                    Message=""
                else:
                    Message="Position is " + current_pos + " which does not contain " + DB.Pos_Type + "\n"
                    logger.debug(DB.Address+":"+str(DB.Port)+ " Pos Type: " + DB.Pos_Type + " Current Pos: " + current_pos + " Valid: " + str(Pos_Type_Valid))
                DB.STATUS.execute("UPDATE STATUS SET Pos_Type=?, Pos_Type_Valid=? where id=?",(current_pos,Pos_Type_Valid,GNSS_ID))
                DB.conn.commit()

        return(Pos_Type_Valid,Message)


        if not found_pos :
            logger.warning(DB.Address+":"+str(DB.Port)+ " Could not determine position type")

#        DB.STATUS.execute("UPDATE STATUS SET Serial_Number=?, Reciever_Type=?, Reciever_Type_Valid=? where id=?",(SerialNumber,rxType,rxValid,GNSS_ID))
#        DB.conn.commit()
    else:
        return(False,"Could not determine position type")

def check_motion_type(GNSS_ID,DB,HTTP):
    Motion=-1
    Motion_Valid=False
    LowLatency=-1
    LowLatency_Valid=False

    Message="Could not determine motion"

    (reply,result)=HTTP.get("/prog/show?rtkControls")

#    print reply
    if reply:
        m=re.search('RtkControls mode=(.*) motion=(.*)',reply)
        if m:
            Message=""
            LowLatency=m.group(1)=="lowLatency"
            Motion=m.group(2)=="static"
            Motion_Valid = Motion == DB.Static

            if not Motion_Valid:
                Message+="Motion is "+ str(Motion)+ " Expected " +  str(DB.Static)+"\n"
                logger.debug(DB.Address+":"+str(DB.Port)+ " Static: " + str(DB.Static) + " Current: " + str(Motion) + " Motion Valid: " + str(Motion_Valid))

            DB.STATUS.execute("UPDATE STATUS SET Static=?, Static_Valid=? where id=?",(Motion,Motion_Valid,GNSS_ID))

            LowLatency_Valid=LowLatency==DB.LowLatency

            if not LowLatency_Valid:
                Message+="LowLatency is "+ str(LowLatency)+ " Expected " +  str(DB.LowLatency)+"\n"
                logger.debug(DB.Address+":"+str(DB.Port)+ " Low Latency: " + str(LowLatency) + " Expected: " + str(DB.LowLatency))

            DB.STATUS.execute("UPDATE STATUS SET LowLatency=?, LowLatency_Valid=? where id=?",(LowLatency,LowLatency_Valid,GNSS_ID))
            DB.conn.commit()
        else:
            Pos_Mode="N/A"
            Motion="N/A"
            Motion_Valid = False
            logger.info(DB.Address+":"+str(DB.Port)+ " Could not determine RTK controls")
            logger.debug(DB.Address+":"+str(DB.Port)+ " Static: " + str(DB.Static) + " Current: " + str(Motion) + " Motion Valid: " + str(Motion_Valid))
            DB.STATUS.execute("UPDATE STATUS SET Static=?, Static_Valid=? where id=?",(Motion,Motion_Valid,GNSS_ID))
            logger.debug(DB.Address+":"+str(DB.Port)+ " LowLatency: " + str(LowLatency))
            DB.STATUS.execute("UPDATE STATUS SET LowLatency=?, LowLatency_Valid=? where id=?",(LowLatency,LowLatency_Valid,GNSS_ID))
            DB.conn.commit()

    return(LowLatency_Valid and Motion_Valid,Message)

def check_antenna(GNSS_ID,DB,HTTP):
    Measurement_Method="N/A"
    Antenna = -1
    Ant_Height = -1.0
    Antenna_Valid = False
    Antenna_Serial="N/A"
    Message="Could not determine antenna type\n"
    (reply,result)=HTTP.get("/prog/show?antenna")

#    print reply
    if reply:
        m=re.search("Antenna type=(.*) name='(.*)' height=(.*) measMethod=(.*) serial='(.*)'",reply)
        if not m:
            m=re.search('Antenna type=(.*) name="(.*)" height=(.*) measMethod=(.*) serial="(.*)"',reply)
        if m:
            Antenna_Valid = True
            Message=""
            Antenna=int(m.group(1))
            Name=m.group(2)
            Ant_Height=float(m.group(3))
            Measurement_Method=m.group(4)


            if Measurement_Method == "BottomOfAntennaMount" :
                Measurement_Method="ARP"

            if Measurement_Method == "BottomOfMagneticMount" :
                Measurement_Method="ARP"



            Antenna_Serial=m.group(4)

            if not (Antenna == DB.Antenna):
                Antenna_Valid=False
                Message+="Antenna is " + str(Antenna) + " expected " + str(DB.Antenna)+"\n"
                logger.info(DB.Address+":"+str(DB.Port)+ " Antenna: " + str(DB.Antenna) + " Current: " + str(Antenna) + " Valid: " + str(Antenna_Valid))

            if not (Ant_Height == DB.Ant_Height):
                Antenna_Valid=False
                Message+="Antenna height is " + str(Ant_Height) + " expected " + str(DB.Ant_Height)+"\n"
                logger.info(DB.Address+":"+str(DB.Port)+ " Height: " + str(DB.Ant_Height) + " Current: " + str(Ant_Height) + " Valid: " + str(Antenna_Valid))

            ant_method=DB.Measurement_Method;

            if not (Measurement_Method == DB.Measurement_Method):
                Antenna_Valid=False
                Message+="Antenna method is " + str(Measurement_Method) + " expected " + str(DB.Measurement_Method)+"\n"
                logger.info(DB.Address+":"+str(DB.Port)+ " Measurment: " + str(DB.Measurement_Method) + " Current: " + str(Measurement_Method) + " Valid: " + str(Antenna_Valid))


    logger.debug(DB.Address+":"+str(DB.Port)+ " Antenna: " + str(Antenna) + " Height: " + str(Ant_Height) + " Measurement_Method: " + str(Measurement_Method) + " Valid: " + str(Antenna_Valid))
    DB.STATUS.execute("UPDATE STATUS SET Antenna=?, Ant_Height=?, Measurement_Method=?, Antenna_Valid=? where id=?",(Antenna,Ant_Height,Measurement_Method,Antenna_Valid,GNSS_ID))
    DB.conn.commit()
    return(Antenna_Valid,Message)


def check_logging(GNSS_ID,DB,HTTP):

    if not DB.Logging_Enabled:
       return(True,"Logging not checked")

    current_pos="N/A"
    Logging_Valid=False
    Message="Logging could not be detemined\n"

    (reply,result)=HTTP.get("/prog/show?sessions")

#    print reply
    if reply:
        Logging_Valid=True
        Message=""
        line=reply.split('\n')[1]

        m=re.search("enabled?=(\w*)",line)

        if not m:
            m=re.search("enable?=(\w*)",line)


        if m:
            Logging_Enabled = m.group(1)=="yes"
            if not (Logging_Enabled  == DB.Logging_Enabled):
                Logging_Valid=False;
                Message+="Logging is " + str(Logging_Enabled) + " expected " + str(DB.Logging_Enabled)+"\n";

                logger.debug(DB.Address+":"+str(DB.Port)+ " Logging:: not enabled")
#            print Logging_Enabled

        else:
            logger.warning(DB.Address+":"+str(DB.Port)+ " enabled? could not be found:")
            DB.STATUS.execute("UPDATE STATUS SET Logging_Valid=? where id=?",(False,GNSS_ID))
            DB.conn.commit()
            Message+="Logging enabled could not be found\n";
            return (False,Message)

        m=re.search("schedule=(\w*)",line)
        if m:
            Logging_schedule = m.group(1)
            if not (Logging_schedule == "continuous"):
                Logging_Valid=False;
                Message+="Logging is " + str(Logging_schedule) + " expected continuous\n"
                logger.debug(DB.Address+":"+str(DB.Port)+ " Logging:: not continuous")
#            print Logging_schedule
        else:
            logger.warning(DB.Address+":"+str(DB.Port)+ " schedule could not be found:")
            DB.STATUS.execute("UPDATE STATUS SET Logging_Valid=?  where id=?",(False,GNSS_ID))
            DB.conn.commit()
            Message+="Logging schedule could not be found\n";
            return (False,Message)


        m=re.search("duration=(\w*)",line)
        if not m:
            m=re.search("durationMin=(\w*)",line)
        if m:
            Logging_Duration = int(m.group(1))
            if not ( Logging_Duration == DB.Logging_Duration):
                Logging_Valid=False;
                Message+="Duration is " + str(Logging_Duration) + " expected " + str(DB.Logging_Duration)+ "\n"
                logger.debug(DB.Address+":"+str(DB.Port)+ " Logging:: duration: " + str(Logging_Duration) + " Expected: " + str(DB.Logging_Duration) + " Valid: " + str(Logging_Valid))
#            print Logging_Duration
        else:
            logger.warning(DB.Address+":"+str(DB.Port)+ " duration could not be found:")
            DB.STATUS.execute("UPDATE STATUS SET Logging_Valid=? where id=?",(False,GNSS_ID))
            DB.conn.commit()
            Message+="Logging duration could not be found\n";
            return (False,Message)


        m=re.search("measInterval=([0-9]+\.[0-9]+)",line)
        if m:
            Logging_measInterval = float(m.group(1))
            if not (Logging_measInterval == DB.Logging_Measurement_Interval):
                Logging_Valid=False;
                Message+="Measurement Interval is " + str(Logging_measInterval) + " Expected " + str(DB.Logging_Measurement_Interval)+ "\n"
                logger.debug(DB.Address+":"+str(DB.Port)+ " Logging:: Measurement Interval: " + str(Logging_measInterval) + " Expected: " + str(DB.Logging_Measurement_Interval) + " Valid: " + str(Logging_Valid))
#            print Logging_measInterval
        else:
            logger.warning(DB.Address+":"+str(DB.Port)+ " measInterval could not be found:")
            DB.STATUS.execute("UPDATE STATUS SET Logging_Valid=?  where id=?",(False,GNSS_ID))
            DB.conn.commit()
            Message+="Logging Measurement Interval could not be found\n";
            return (False,Message)


        m=re.search("posInterval=([0-9]+\.[0-9]+)",line)
        if m:
            Logging_posInterval = float(m.group(1))
#            print Logging_posInterval
            if not (Logging_posInterval == DB.Logging_Position_Interval):
                Logging_Valid=False;
                Message+="Position Interval is " + str(Logging_posInterval) + " Expected " + str(DB.Logging_Position_Interval)+ "\n"
                logger.debug(DB.Address+":"+str(DB.Port)+ " Logging:: Position Interval: " + str(Logging_posInterval) + " Expected: " + str(DB.Logging_Position_Interval) + " Valid: " + str(Logging_Valid))
        else:
            logger.warning(DB.Address+":"+str(DB.Port)+ " posInterval could not be found:")
            DB.STATUS.execute("UPDATE STATUS SET Logging_Valid=?  where id=?",(False,GNSS_ID))
            DB.conn.commit()
            Message+="Logging Position Interval could not be found\n";
            return (False,Message)

        m=re.search("smoothRanges=(\w*)",line)
        if m:
            Logging_smoothRanges = m.group(1)
            if not  (Logging_smoothRanges=="no"):
                Logging_Valid=False;
                Message+="Smoothed ranges is " + str(Logging_smoothRanges) + " Expected no\n"
#            print Logging_smoothRanges
        else:
            logger.warning(DB.Address+":"+str(DB.Port)+ " smoothRanges could not be found:")
            DB.STATUS.execute("UPDATE STATUS SET Logging_Valid=? where id=?",(False,GNSS_ID))
            DB.conn.commit()
            Message+="Logging Smoothed ranges could not be found\n";
            return (False,Message)

        m=re.search("smoothPhases=(\w*)",line)
        if m:
            Logging_smoothPhases = m.group(1)
            if not  (Logging_smoothPhases=="no"):
                Logging_Valid=False;
                Message+="Smoothed phase is " + str(Logging_smoothPhases) + " Expected no\n"

#            print Logging_smoothPhases
        else:
            logger.warning(DB.Address+":"+str(DB.Port)+ " smoothPhases could not be found:")
            DB.STATUS.execute("UPDATE STATUS SET Logging_Valid=? where id=?",(False,GNSS_ID))
            DB.conn.commit()
            Message+="Logging Smoothed phases could not be found\n";
            return (False,Message)

        Logging_voltTempInterval=0
        m=re.search("voltTempInterval=(\w*)",line)
        if m:
            Logging_voltTempInterval = m.group(1)
            if Logging_voltTempInterval=="0" :
                Logging_Valid = False
                logging.info(DB.Address+":"+str(DB.Port)+ " voltTempInterval is zero")
                Message+="Logging voltage/temperture is not enabled\n";
            else:
#                logging.debug(DB.Address+":"+str(DB.Port)+ " voltTempInterval is: " + str(Logging_voltTempInterval))
                pass

#            print Logging_smoothPhases
        else:
            logger.info(DB.Address+":"+str(DB.Port)+ " voltTempInterval could not be found:")

        logger.debug(DB.Address+":"+str(DB.Port)+ " Logging:: Enabled: "+ str(Logging_Enabled) + " Duration: " + str(Logging_Duration) + " Measurement: " + str(Logging_measInterval) + " Position: " + str (Logging_posInterval) + " Volt/Temp: " + str(Logging_voltTempInterval) + " Valid: " + str(Logging_Valid))
        DB.STATUS.execute("UPDATE STATUS SET Logging_Enabled=?,Logging_Duration=?,Logging_Measurement_Interval=?,Logging_Position_Interval=?,Logging_Volt_Temp_Interval=?,Logging_Valid=? where id=?",(Logging_Enabled,Logging_Duration,Logging_measInterval,Logging_posInterval,Logging_voltTempInterval,Logging_Valid,GNSS_ID))

    else:
        logger.info(DB.Address+":"+str(DB.Port)+ " No reply from logging request:")
        DB.STATUS.execute("UPDATE STATUS SET Logging_Valid=? where id=?",(Logging_Valid,GNSS_ID))

    return (Logging_Valid,Message)

def check_email(GNSS_ID,DB,HTTP):


    (reply,result)=HTTP.get("/xml/dynamic/email.xml")

#    print reply
    if result !=  200:
        Email_Valid = False
        Message="Could not determine Email\n"
        return(Email_Valid,Message)

    root=ET.fromstring(reply)


    Email_Valid = True
    Message=""
    Email_Enabled=root.find("enable").text=="1"

    if not (Email_Enabled == DB.Email_Enabled):
        Email_Valid=False
        Message+="Email is " + str(Email_Enabled) + " expected " + str(DB.Email_Enabled) + "\n";
        logger.debug(DB.Address+":"+str(DB.Port)+ " Email Enabled: " + str(Email_Enabled) + ", Expected Enabled: " + str(DB.Email_Enabled) + ', Valid: ' + str(Email_Valid))

    if Email_Enabled:
        Email_To=root.find("to").text.lower()
        if not(Email_To == DB.Email_To.lower()):
            Email_Valid=False
            Message+="Email is " + str(Email_To) + " expected " + DB.Email_To + "\n";
            logger.debug(DB.Address+":"+str(DB.Port)+ " Email To: " + str(Email_To) + ", Expected To: " + str(DB.Email_To) + ', Valid: ' + str(Email_Valid))

        for alert in root.findall("alert"):
#            pprint (alert.attrib)
            if alert.attrib['id']=="16":
                if (not 'enabled' in alert.attrib) or (alert.attrib['enabled'] != "1"):
                    Email_Valid=False
                    Message+="Email is enabled without crash reporting\n";
                    logger.info(DB.Address+":"+str(DB.Port)+ " Email enabled but not reporting crashes")
        DB.STATUS.execute("UPDATE STATUS SET Email_Enabled=?, Email_To=?, Email_Valid=? where id=?",(Email_Enabled,Email_To,Email_Valid,GNSS_ID))
        DB.conn.commit()
    else:
        DB.STATUS.execute("UPDATE STATUS SET Email_Enabled=?, Email_Valid=? where id=?",(Email_Enabled,Email_Valid,GNSS_ID))
        DB.conn.commit()

    return(Email_Valid,Message)


def check_errors(GNSS_ID,DB,HTTP):


    (reply,result)=HTTP.get("/xml/dynamic/errLog.xml")

#    print reply
    if result !=  200:
        Errors_Valid = False
        Message="Could not determine errors\n"
        return(Errors_Valid,Message)

    root=ET.fromstring(reply)


    Message=""

    Num_Entries=int(root.find("numEntries").text)
    Num_Errors=0

    for entry in root.findall("entry"):
#        ET.dump(entry)
        flags_node=entry.find("flags")
#        ET.dump(flags_node)
        error = (int(flags_node.text) & 0x3 ) == 0
        if error :
            Num_Errors+=1

    Errors_Valid = Num_Errors==0

    if Errors_Valid == False:
        Message="There are {} Errors and {}  Warnings\n".format(Num_Errors, Num_Entries-Num_Errors)

    return(Errors_Valid,Message)

def check_FTP(GNSS_ID,DB,HTTP):

    FTP_Valid=True
    Message="FTP could not be determined\n"

    (reply,result)=HTTP.get("/xml/dynamic/dataLogger.xml")
    Message="";

    if result !=  200:
        FTP_Valid = False
        Message="Could not determine FTP"
        return(FTP_Valid,Message)

#    print reply
    root=ET.fromstring(reply)

#    logger_active = session.find('enabled').text=="1"
    try:
        FTP_Enabled = root.find('ftpPushEnabled').text=="1"
        session=root.find("session")
        FTP_Enabled = session.find('ftpPushServer').text=="1"
    except:
        session=root.find("session")
        if session == None:
            FTP_Enabled = False
        else:
            FTP_Enabled_Node = session.find('ftpPush')
            if FTP_Enabled_Node == None:
                FTP_Enabled = False
            else:
                FTP_Enabled = FTP_Enabled_Node.text=="1"

#    print logging_active`<
#    print ftppush_active

    if not (FTP_Enabled == DB.FTP_Enabled):
        FTP_Valid=False
        Message+="FTP Enabled is " + str(FTP_Enabled) + " Expected  " + str(DB.FTP_Enabled) + "\n";
        logger.debug(DB.Address+":"+str(DB.Port)+ " FTP Enabled: " + str(FTP_Enabled) + ", Expected Enabled: " + str(DB.FTP_Enabled) + ', Valid: ' + str(FTP_Valid))

    if FTP_Enabled:
        (reply,result)=HTTP.get("/xml/dynamic/ftpPush.xml")

#        print reply

        root=ET.fromstring(reply)
        try:
            FTP_To = root.find('server').find("dir").text.lower()
        except:
            try:
                FTP_To = root.find("dir").text.lower()
            except:
                FTP_To=""

        if not (FTP_To == DB.FTP_To.lower()):
            FTP_Valid=False
            Message+="FTP To is " + str(FTP_To) + " Expected " + str(DB.FTP_To) + "\n"
            logger.debug(DB.Address+":"+str(DB.Port)+ " FTP To: " + str(FTP_To) + ", Expected To: " + str(DB.FTP_To) + ', Valid: ' + str(FTP_Valid))

        DB.STATUS.execute("UPDATE STATUS SET FTP_Enabled=?, FTP_To=?, FTP_Valid=? where id=?",(FTP_Enabled,FTP_To,FTP_Valid,GNSS_ID))
        DB.conn.commit()
    else:
        DB.STATUS.execute("UPDATE STATUS SET FTP_Enabled=?, FTP_Valid=? where id=?",(FTP_Enabled,FTP_Valid,GNSS_ID))
        DB.conn.commit()
    return(FTP_Valid,Message)

def check_Power(GNSS_ID,DB,HTTP):

    Power_Valid=False
    Message="Power could not be determined"


    (reply,result)=HTTP.get("/xml/dynamic/powerData.xml")

#    print reply
    if result !=  200:
        return(Power_Valid,Message)



    if reply <> "":
       root=ET.fromstring(reply)
       B1=root.find("B1")
    else:
        B1 = None

    if B1 != None:
        Message=""
        battery_active = B1.find("active") != None
        if not battery_active:
            Power_Valid=True
        else:
            Power_Valid=False
            Message="Running on Battery"
            logger.debug(DB.Address+":"+str(DB.Port)+ " Battery in use: " + str(Power_Valid))
    else:
        logger.info(DB.Address+":"+str(DB.Port)+ " Reciever does not have a battery" )
        Power_Valid= True
#    print logging_active
#    print ftppush_active

    DB.STATUS.execute("UPDATE STATUS SET Power_Valid=? where id=?",(Power_Valid,GNSS_ID))
    DB.conn.commit()
    return (Power_Valid,Message)


def check_Uptime(GNSS_ID,DB,HTTP):

    Message="Could not determine uptime\n"

    (reply,result)=HTTP.get("/xml/dynamic/powerData.xml")
#    print reply

    root=ET.fromstring(reply)

    uptime = root.find("uptime")
    hours = int(uptime.find("hour").text,10)
    days  =  int(uptime.find("day").text,10)
    total_hours=days*24 + hours


    logger.debug(DB.Address+":"+str(DB.Port)+ " Uptime (hours): " + str(total_hours))
    DB.STATUS.execute("UPDATE STATUS SET Uptime=? where id=?",(total_hours,GNSS_ID))
    DB.conn.commit()
    if total_hours <1:
        return (False,"Unit has uptime of less than 1 hour")
    else:
        return (True,"")


def check_clock(GNSS_ID,DB,HTTP):

    Clock_Valid=False
    Message="Clock Steering could not be determined\n"
    (reply,result)=HTTP.get("/prog/show?clockSteering")
#    print reply
    if reply:
        m=re.search('ClockSteering enable=(.*)',reply)
        if m:
            Clock_Valid=Clock = m.group(1) == "yes"
            Clock_Valid=True
            if not Clock_Valid:
                Message="Clock Steering is not enabled\n"
                logger.debug(DB.Address+":"+str(DB.Port)+ " Clock:: Current: " + str(Clock) + ", Clock Valid: " + str(Clock_Valid))
            else :
                Message=""
            DB.STATUS.execute("UPDATE STATUS SET Clock=?, Clock_Valid=? where id=?",(Clock,Clock_Valid,GNSS_ID))
            DB.conn.commit()
    return (Clock_Valid,Message)

def check_UPS(GNSS_ID,DB,HTTP):

    Message=""
    UPS_Valid=False
    UPS=False
    (reply,result)=HTTP.get("/prog/show?UPS")
#    print reply
    if reply:
        m=re.search('UPS enable=(.*)',reply)
        if m:
            UPS = UPS_Valid = m.group(1) == "yes"
            if UPS_Valid:
                Message=""
            else:
                Message="UPS is not enabled\n"
                logger.debug(DB.Address+":"+str(DB.Port)+ " UPS:: Current: " + str(UPS) + ", UPS Valid: " + str(UPS_Valid))
        else:
            logger.debug(DB.Address+":"+str(DB.Port)+ " UPS:: Not supported")
            Message=""
            UPS_Valid=True
            UPS=False
    DB.STATUS.execute("UPDATE STATUS SET UPS=?, UPS_Valid=? where id=?",(UPS,UPS_Valid,GNSS_ID))
    DB.conn.commit()
    return (UPS_Valid,Message)

def check_PDOP(GNSS_ID,DB,HTTP):

    PDOP_Valid=False
    Message="PDOP Could not be determined"
    (reply,result)=HTTP.get("/prog/show?pdopMask")
#    print reply
    if reply:
        m=re.search('PdopMask mask=(.*)',reply)
        if m:
            PDOP = int(m.group(1),10)
            PDOP_Valid=PDOP==DB.PDOP
            if not PDOP_Valid:
                Message="PDOP is " + str(PDOP) +  " Expected: " + str(DB.PDOP) + "\n";
                logger.debug(DB.Address+":"+str(DB.Port)+ " PDOP:: Current: " + str(PDOP) +  ", Expected: " + str(DB.PDOP) + ", PDOP Valid: " + str(PDOP_Valid))
            DB.STATUS.execute("UPDATE STATUS SET PDOP=?, PDOP_Valid=? where id=?",(PDOP,PDOP_Valid,GNSS_ID))
            DB.conn.commit()
    return(PDOP_Valid,Message)

def check_Elev(GNSS_ID,DB,HTTP):

    Elev_Mask_Valid=False
    Message="Elevation Mask could not be determined"
    (reply,result)=HTTP.get("/prog/show?elevationMask")
#    print reply
    if reply:
        m=re.search('ElevationMask mask=(.*)',reply)
        if m:
            Elev_Mask = int(m.group(1),10)
            Elev_Mask_Valid=Elev_Mask==DB.Elev_Mask
            if not Elev_Mask_Valid:
                Message="Elev mask is " + str(Elev_Mask) +  " Expected: " + str(DB.Elev_Mask) + "\n"
                logger.debug(DB.Address+":"+str(DB.Port)+ " Elev:: Current: " + str(Elev_Mask) +  ", Expected: " + str(DB.Elev_Mask) + ", PDOP Valid: " + str(Elev_Mask_Valid))

            DB.STATUS.execute("UPDATE STATUS SET Elev_Mask=?, Elev_Mask_Valid=? where id=?",(Elev_Mask,Elev_Mask_Valid,GNSS_ID))
            DB.conn.commit()
    return(Elev_Mask_Valid,Message)

def get_Temperature(GNSS_ID,DB,HTTP):

    (reply,result)=HTTP.get("/prog/show?temperature")
#    print reply
    if reply:
        m=re.search('Temperature temp=(.*)',reply)
        if m:
            Temperature = float(m.group(1))
            logger.debug(DB.Address+":"+str(DB.Port)+ " Temp:: Current: " + str(Temperature))
            DB.STATUS.execute("UPDATE STATUS SET Temperature=? where id=?",(Temperature,GNSS_ID))
            DB.conn.commit()


def get_Warranty(GNSS_ID,DB,HTTP):

    (reply,result)=HTTP.get("/prog/show?firmwareWarranty")
#    print reply
    if reply:
        m=re.search('FirmwareWarranty date=(.*)',reply)
        if m:
            Warranty = m.group(1)
            logger.debug(DB.Address+":"+str(DB.Port)+ " Warranty:: Current: " + str(Warranty))
            DB.STATUS.execute("UPDATE STATUS SET Warranty=? where id=?",(Warranty,GNSS_ID))
            DB.conn.commit()

def get_SystemName(GNSS_ID,DB,HTTP):

    (reply,result)=HTTP.get("/prog/show?SystemName")
#    print reply
    if reply:
        m=re.search('SystemName name=(.*)',reply)
        if m:
            SystemName = m.group(1)
            logger.debug(DB.Address+":"+str(DB.Port)+ " System Name:: Current: " + str(SystemName))
            DB.STATUS.execute("UPDATE STATUS SET SystemName=? where id=?",(SystemName,GNSS_ID))
            DB.conn.commit()

def check_MultipathReject(GNSS_ID,DB,HTTP):

    Message="Could not determine Multipath Rejection\n"
    MultipathReject_Valid=False
    (reply,result)=HTTP.get("/prog/show?MultipathReject")
#    print reply
    if reply:
        m=re.search('MultipathReject enable=(.*)',reply)
        if m:
            MultipathReject = m.group(1) == "yes"
            if not MultipathReject:
                MultipathReject_Valid=False
                Message="Multipath Rejection is not enabled\n"
                logger.debug(DB.Address+":"+str(DB.Port)+ " Multipath Reject:: Current: " + str(MultipathReject))
            else:
                MultipathReject_Valid=True;
                Message=""

            DB.STATUS.execute("UPDATE STATUS SET MultipathReject=?,MultipathReject_Valid=? where id=?",(MultipathReject,MultipathReject_Valid,GNSS_ID))
            DB.conn.commit()
    return(MultipathReject_Valid,Message)

def check_testMode(GNSS_ID,DB,HTTP):

    Message="Could not determine test mode\n"
    testMode_Valid=False
    (reply,result)=HTTP.get("/prog/show?TestMode")
#    print reply
    if reply:
        m=re.search('testMode enable=(.*)',reply)
        if m:
            testMode = m.group(1) == "yes"
            testMode_Valid=not testMode
#            testMode_Valid=False
            testMode_Valid=(not testMode) or (DB.Auth=="yes")

            if testMode_Valid:
                Message=""
            else:
                Message="Test mode is enabled and auth is not yes. Turning off\n"
                logger.debug(DB.Address+":"+str(DB.Port)+ " testMode :: Current: " + str(testMode))
                (reply,result)=HTTP.get("/prog/set?testmode&enable=no")

            DB.STATUS.execute("UPDATE STATUS SET testMode=?,testMode_Valid=? where id=?",(testMode,testMode_Valid,GNSS_ID))
            DB.conn.commit()
    return(testMode_Valid,Message)

def check_Auth(GNSS_ID,DB,HTTP):

    Ses = requests.Session()
    Host=HTTP.Host
    Port=HTTP.Port
    TimeOut=HTTP.TimeOut
    Auth_Valid=False
    Auth="Unknown"
    Message=""

#    logging.debug(Host+":"+str(Port)+ " Checking Auth: ")
    Auth="Unknown"
    try:
#            print "http://" + self.Host + ":" + str(self.Port) + url_part
#            pprint (self.Ses)
        Response=Ses.get("http://" + Host + ":" + str(Port) + "/prog/show?pdopMask",timeout=TimeOut)

#        print Response.status_code
        if Response.status_code==401:
#            Auth Enabled
            Auth="Yes"
        else :
#            print "Not 401"
            m=re.search('PdopMask mask=(.*)',Response.text)
            if m:
                PDOP = int(m.group(1),10)
#                print "http://" + Host + ":" + str(Port) + "/prog/set?PdopMask&mask="+str(PDOP)

                Response=Ses.get("http://" + Host + ":" + str(Port) + "/prog/set?PdopMask&mask="+str(PDOP),timeout=TimeOut)

                m=re.search('^ERROR',Response.text)
                if m:
                    logger.debug(DB.Address+":"+str(DB.Port)+ " Auth:: Anonymous")
                    Auth="Anonymous"
                else:
                    logger.debug(DB.Address+":"+str(DB.Port)+ " Auth:: Disabled")
                    Auth="no"
    except:
        pass


    Auth_Valid=Auth.lower()==DB.Auth.lower()

    if not Auth_Valid :
        Message="Auth is " + str(Auth) + " Expected: " + DB.Auth + "\n"
        logger.debug(DB.Address+":"+str(DB.Port)+ " Auth:: Current: " + str(Auth) +  ", Expected: " + str(DB.Auth) + ", Auth Valid: " + str(Auth_Valid))
    DB.STATUS.execute("UPDATE STATUS SET Auth=?, Auth_Valid=? where id=?",(Auth,Auth_Valid,GNSS_ID))
    DB.conn.commit()

    return(Auth_Valid,Message)


def decdeg2dms(dd):
    negative = dd < 0
    dd = abs (dd)
    minutes,sec = divmod(dd*3600,60)
    degrees,minutes = divmod(minutes,60)
    if negative:
        if degrees > 0:
            degrees = -degrees
        elif minutes > 0:
            minutes = -minutes
        else:
            seconds = -seconds
    return int(degrees),int(minutes),sec


degree_sign= u'\N{DEGREE SIGN}'

def DMSstr(decimal):
    deg,mnt,sec=decdeg2dms(decimal)
    S=str(deg)+degree_sign+str(mnt)+"'"+"{:.5f}".format(sec)+'"'
    return S


def check_Ref(GNSS_ID,DB,HTTP):

    Ref_Valid=False
    Message="Ref information could not be determined\n"
    (reply,result)=HTTP.get("/prog/show?RefStation")
#    print reply
    if reply:
        m=re.search("RefStation lat=(.*) lon=(.*) height=(.*) Rtcm2Id=.* Rtcm3Id=.* CmrId=.* Name='(.*)' Code='(.*)'$",reply)
        if m:
            Message=""
            Ref_Valid=True
            Ref_Lat = float(m.group(1))
            Ref_Long = float(m.group(2))
            Ref_Height = float(m.group(3))
            Ref_Name = m.group(4)
            Ref_Code = m.group(5)

            if Ref_Name:
                Ref_Name=Ref_Name.upper()

            if Ref_Code:
                Ref_Code=Ref_Code.upper()

            if not (Ref_Lat == DB.Ref_Lat):
                Ref_Valid=False
                Message+="Latitude is " + str(Ref_Lat) + " (" + DMSstr(Ref_Lat)+ ") Expected " + str(DB.Ref_Lat)+ " (" + DMSstr(DB.Ref_Lat)+ ")\n"

            if not (Ref_Long == DB.Ref_Long):
                Ref_Valid=False
                Message+="Longitude is " + str(Ref_Long) + " (" + DMSstr(Ref_Long)+ ") Expected " + str(DB.Ref_Long)+ " (" + DMSstr(DB.Ref_Long)+ ")\n"

            if not (Ref_Height == DB.Ref_Height):
                Ref_Valid=False
                Message+="Height is " + str(Ref_Height) + " Expected " + str(DB.Ref_Height)+"\n"

            if not (Ref_Name == DB.Ref_Name):
                Ref_Valid=False
                Message+="Ref Name is '" + str(Ref_Name) + "' Expected " + str(DB.Ref_Name)+"\n"

            if not (Ref_Code == DB.Ref_Code):
                Ref_Valid=False
                Message+="Ref Code is '`" + str(Ref_Code) + "' Expected " + str(DB.Ref_Code)+"\n"

            logger.debug(DB.Address+":"+str(DB.Port) + " Reference:: Latitude: " + str(Ref_Lat) + " Long: " + str(Ref_Long) +" Height: " + str(Ref_Height) + " Name: " + str(Ref_Name)  + " Code: " + str(Ref_Code)+ " Valid: " + str(Ref_Valid))
            DB.STATUS.execute("UPDATE STATUS SET Ref_Lat=?, Ref_Long=?, Ref_Height=?, Ref_Name=?, Ref_Code=?,Ref_Valid=? where id=?",(Ref_Lat,Ref_Long,Ref_Height,Ref_Name,Ref_Code,Ref_Valid,GNSS_ID))
            DB.conn.commit()
    return(Ref_Valid,Message)


def check_Tracking(GNSS_ID,DB,HTTP):
    Message=""
    (reply,result)=HTTP.get("/prog/show?Tracking")
    if reply:
#        print reply

        m=re.search("^ERROR",reply)
        if m:
            logger.warning(DB.Address+":"+str(DB.Port) + " Does not support tracking checking")
            DB.STATUS.execute("UPDATE STATUS SET GPS_Valid=0, GLN_Valid=0, GAL_Valid=0, BDS_Valid=0, QZSS_Valid=0, SBAS_Valid=0, Frequencies_Valid=0 where id=" + str(GNSS_ID))
            DB.conn.commit()
            return (True,""); # This is not a failure for Nagios


# Tracking GpsL1CA=on GpsL2=on GpsL2CS=CM+CL GpsL5=off Sbas=L1CA GlonassL1C=on GlonassL1P=on GlonassL2C=on GlonassL2P=off GlonassL3=off GalileoE1=off GalileoE5A=off GalileoE5B=off GalileoE5AltBoc=off BeidouB1=on BeidouB2=on BeidouB3=offTracking QzssL1CA=on QzssL1SAIF=off QzssL1C=off QzssL2CS=CM+CL QzssL5=I+Q QzssLEX=off
# Tracking GpsL1CA=on GpsL2=on GpsL2CS=CM+CL GpsL5=I+Q Sbas=L1CA GlonassL1C=on GlonassL1P=off GlonassL2C=on GlonassL2P=off GlonassL3=Data+PilotTracking QzssL1CA=off QzssL1SAIF=off QzssL2CS=off QzssL5=off QzssLEX=off
        Frequencies_Valid=True
        Frequencies=0

        m=re.search("GpsL1CA=on",reply)
        if m:
            GPS=1
            Frequencies=max(Frequencies,1)
        else :
            GPS=0
            if DB.GPS:
               logger.info(DB.Address+":"+str(DB.Port) + " Tracking:: GPS L1 Disabled")

#        print  "GPS " + str(DB.GPS)
        GPS_Valid=DB.GPS==GPS;

        if not GPS_Valid:
            Message+="GPS Not enabled\n";


        if DB.GPS:

            if DB.Frequencies> 1:
                m=re.search("GpsL2=on",reply)
                if not m:
                    m=re.search("GpsL2=L2CSfallback",reply)

                if  m :
                    Frequencies=max(Frequencies,2)
                    GPS=2
                else:
                    GPS_Valid=False
                    Frequencies_Valid=False
                    logger.info(DB.Address+":"+str(DB.Port) + " Tracking:: GPS L2 Disabled")
                    Message+="GPS L2 Not Enabled\n";

            if DB.Frequencies> 2:
                m=re.search("GpsL5=",reply)
                if  m :
                    m=re.search("GpsL5=off",reply)
                    if not m:
                        Frequencies=max(Frequencies,3)
                        GPS=3
                    else:
                        GPS_Valid=False
                        Frequencies_Valid=False
                        logger.info(DB.Address+":"+str(DB.Port) + " Tracking:: GPS L5 Disabled")
                        Message+="GPS L5 Not Enabled\n";
                else:
                    GPS_Valid=False
                    Frequencies_Valid=False
                    logger.info(DB.Address+":"+str(DB.Port) + " Tracking:: GPS L5 Not available")
                    Message+="GPS L5 Not available\n";

        if not GPS_Valid:
            logger.debug(DB.Address+":"+str(DB.Port) + " GPS:: GPS Enabled: " + str(DB.GPS) + " Frequencies: " + str(DB.Frequencies) +" Current GPS: " + str(GPS) +  " Valid: " + str(GPS_Valid) + " Current Freq: " + str(Frequencies))
        DB.STATUS.execute("UPDATE STATUS SET GPS=?, GPS_Valid=? where id=?",(GPS,GPS_Valid,GNSS_ID))


        m=re.search("GlonassL1C=on",reply)

        if m:
            GLN=1
            Frequencies=max(Frequencies,1)
        else :
            GLN=0
            if DB.GLN:
                logger.info(DB.Address+":"+str(DB.Port) + " Tracking:: GLN L1 Disabled")

        GLN_Valid=DB.GLN==GLN;

        if not GLN_Valid:
            if DB.GLN:
                Message+="GLN Not enabled\n"
            else:
                Message+="GLN enabled when it should not be\n"


        if DB.GLN:
            if DB.Frequencies> 1:
                m=re.search("GlonassL2C=on",reply)

                if not m:
                    m=re.search("GlonassL2P=on",reply)

                if  m :
                    Frequencies=max(Frequencies,2)
                    GLN=2
                else:
                    GLN_Valid=False
                    Frequencies_Valid=False
                    logger.info(DB.Address+":"+str(DB.Port) + " Tracking:: GLN L2 Disabled")
                    Message+="GLN L2 Not enabled\n"

            if DB.Frequencies> 2:
                m=re.search("GlonassL3=",reply)
                if m :
                    Frequencies=max(Frequencies,3)
                    m=re.search("GlonassL3=",reply)
                    if m :
                        GLN=3
                        Frequencies=max(Frequencies,3)
                    else:
                        GLN_Valid=False
                        Frequencies_Valid=False
                        logger.info(DB.Address+":"+str(DB.Port) + " Tracking:: GLN L3 Disabled")
                        Message+="GLN L3 Not enabled\n"
                else:
#                    GLN_Valid=False   We do not fail these now for the old receivers can not track this
#                    Frequencies_Valid=False
                    logger.info(DB.Address+":"+str(DB.Port) + " Tracking:: GLN L3 N/A")

        if not GLN_Valid:
            logger.debug(DB.Address+":"+str(DB.Port) + " GLN:: GLN Enabled: " + str(DB.GLN) + " Frequencies: " + str(DB.Frequencies) +" Current GLN: " + str(GLN) +  " Valid: " + str(GLN_Valid) + " Current Freq: " + str(Frequencies))
        DB.STATUS.execute("UPDATE STATUS SET GLN=?, GLN_Valid=? where id=?",(GLN,GLN_Valid,GNSS_ID))



        m=re.search("GalileoE1=",reply)
        if m:
            m=re.search("GalileoE1=off",reply)
            if not m:
                GAL=1
                Frequencies=max(Frequencies,1)
            else :
                GAL=0
                if DB.GAL:
                    logger.info(DB.Address+":"+str(DB.Port) + " Tracking:: GAL E1 Disabled")
        else :
            GAL=0
            if DB.GAL:
                logger.info(DB.Address+":"+str(DB.Port) + " Tracking:: GAL E1 N/A")

        GAL_Valid=DB.GAL==GAL;

        if not GAL_Valid:
            if DB.GAL:
                Message+="GAL Not enabled\n"
            else:
                Message+="GAL enabled when it shoudld not be\n"



        if DB.GAL:
            '''
            if DB.Frequencies> 2:
                m=re.search("GalileoE5A=",reply)
                if m :
                    m=re.search("GalileoE5A=off",reply)
                    if not m :
                        Frequencies=max(Frequencies,2)
                        GAL=2
                    else:
                        GAL_Valid=False
                        Frequencies_Valid=False
                        logger.info(DB.Address+":"+str(DB.Port) + " Tracking:: GAL GalileoE5A Disabled")
                        Message+="GAL E5A Not enabled\n"
                else:
                    GAL_Valid=False
                    Frequencies_Valid=False
                    logger.info(DB.Address+":"+str(DB.Port) + " Tracking:: GAL GalileoE5A Not available")
                    Message+="GAL E5A Not available\n"


            if DB.Frequencies> 2:
                m=re.search("GalileoE5B=",reply)
                if m :
                    m=re.search("GalileoE5B=off",reply)
                    if not m :
                        Frequencies=max(Frequencies,2)
                        GAL=2
                    else:
                        GAL_Valid=False
                        Frequencies_Valid=False
                        logger.info(DB.Address+":"+str(DB.Port) + " Tracking:: GAL GalileoE5B Disabled")
                        Message+="GAL E5B Not enabled\n"
                else:
                    GAL_Valid=False
                    Frequencies_Valid=False
                    logger.info(DB.Address+":"+str(DB.Port) + " Tracking:: GAL GalileoE5B N/A")
                    Message+="GAL E5B Not avaialble\n"

            '''

            if DB.Frequencies> 2:
                m=re.search("GalileoE5AltBoc=",reply)
                if m :
                    m=re.search("GalileoE5AltBoc=off",reply)
                    if not m :
                        Frequencies=max(Frequencies,2)
                        GAL=2
                    else:
                        GAL_Valid=False
                        Frequencies_Valid=False
                        logger.info(DB.Address+":"+str(DB.Port) + " Tracking:: GAL GalileoE5AltBoc Disabled")
                        Message+="GAL E5AtlBoc Not enabled\n"
                else:
                    GAL_Valid=False
                    Frequencies_Valid=False
                    logger.info(DB.Address+":"+str(DB.Port) + " Tracking:: GAL GalileoE5AltBoc N/A")
                    Message+="GAL E5AltBoc Not avaialble\n"


        if not GAL_Valid:
            logger.debug(DB.Address+":"+str(DB.Port) + " GAL:: GAL Enabled: " + str(DB.GAL) + " Frequencies: " + str(DB.Frequencies) +" Current GAL: " + str(GAL) +  " Valid: " + str(GAL_Valid) + " Current Freq: " + str(Frequencies))
        DB.STATUS.execute("UPDATE STATUS SET GAL=?, GAL_Valid=? where id=?",(GAL,GAL_Valid,GNSS_ID))



        m=re.search("BeidouB1=on",reply)
        if m:
            BDS=1
            Frequencies=max(Frequencies,1)
        else :
            BDS=0
            if DB.BDS:
                logger.info(DB.Address+":"+str(DB.Port) + " Tracking:: BDS B1 Disabled or N/A")

        BDS_Valid=DB.BDS==BDS;
#        print "BDS: " + str(DB.BDS) + ' :: ' + str(BDS) + ' ::: ' +  str(BDS_Valid)

        if not BDS_Valid:
            if DB.BDS:
                Message+="BDS Not Enabled\n"
            else:
                Message+="BDS Enabled when it shoud not be\n"


        if DB.BDS:
            if DB.Frequencies> 1:
                m=re.search("BeidouB2=on",reply)
                if  m :
                    Frequencies=max(Frequencies,2)
                    BDS=2
                else:
                    BDS_Valid=False
                    Frequencies_Valid=False
                    logger.info(DB.Address+":"+str(DB.Port) + " Tracking:: BDS B2 Disabled or N/A")
                    Message+="BDS B2 Not Enabled or N/A\n"

#            if DB.Frequencies> 2:
#                m=re.search("BeidouB3=on",reply)
#                if m :
#                    Frequencies=max(Frequencies,3)
#                else:
#                    BDS_Valid=False
#                    Frequencies_Valid=False
#                    logger.info(DB.Address+":"+str(DB.Port) + " Tracking:: BDS B3 Disabled")

        if not BDS_Valid:
            logger.debug(DB.Address+":"+str(DB.Port) + " BDS:: BDS Enabled: " + str(DB.BDS) + " Frequencies: " + str(DB.Frequencies) +" Current BDS: " + str(BDS) +  " Valid: " + str(BDS_Valid) + " Current Freq: " + str(Frequencies))
        DB.STATUS.execute("UPDATE STATUS SET BDS=?, BDS_Valid=? where id=?",(BDS,BDS_Valid,GNSS_ID))



        m=re.search("QzssL1CA=on",reply)

        if m:
            QZSS=1
            Frequencies=max(Frequencies,1)
        else :
            QZSS=0
            if DB.QZSS:
                logger.info(DB.Address+":"+str(DB.Port) + " Tracking:: QZSS L1 Disabled")

        QZSS_Valid=DB.QZSS==QZSS;

        if not QZSS_Valid:
            if DB.QZSS:
                Message+="QZSS Not Enabled\n"
            else:
                Message+="QZSS Enabled when shouldn't be\n"


        if DB.QZSS:
            if DB.Frequencies> 1:
                m=re.search("QzssL2CS=",reply)
                if  m :
                    m=re.search("QzssL2CS=off",reply) # make sure we have the field and then confirm it is off
                    if not m:
                        Frequencies=max(Frequencies,2)
                        QZSS=2
                    else:
                        QZSS_Valid=False
                        Frequencies_Valid=False
                        logger.info(DB.Address+":"+str(DB.Port) + " Tracking:: QZSS L2 Disabled")
                        Message+="QZSS L2 Disabled\n"
                else:
                    QZSS_Valid=False
                    Frequencies_Valid=False
                    logger.info(DB.Address+":"+str(DB.Port) + " Tracking:: QZSS L2 not available")
                    Message+="QZSS L2 N/A\n"

            if DB.Frequencies> 2:
                m=re.search("QzssL5=",reply)
                if  m :
                    m=re.search("QzssL5=off",reply) # make sure we have the field and then confirm it is off
                    if not m:
                        Frequencies=max(Frequencies,2)
                        QZSS=3
                    else:
                        QZSS=False
                        Frequencies_Valid=False
                        logger.info(DB.Address+":"+str(DB.Port) + " Tracking:: QZSS L5 Disabled")
                        Message+="QZSS L5 Disabled\n"
                else:
                    QZSS=False
                    Frequencies_Valid=False
                    logger.info(DB.Address+":"+str(DB.Port) + " Tracking:: QZSS L5 not available")
                    Message+="QZSS L5 N/A\n"

        if not QZSS_Valid:
            logger.debug(DB.Address+":"+str(DB.Port) + " QZSS:: QZSS Enabled: " + str(DB.QZSS) + " Frequencies: " + str(DB.Frequencies) +" Current QZSS: " + str(QZSS) +  " Valid: " + str(QZSS_Valid) + " Current Freq: " + str(Frequencies))

        DB.STATUS.execute("UPDATE STATUS SET QZSS=?, QZSS_Valid=? where id=?",(QZSS,QZSS_Valid,GNSS_ID))



        m=re.search("Sbas=",reply)
        if  m :
            m=re.search("Sbas=off",reply) # make sure we have the field and then confirm it is off
            if not m:
                Frequencies=max(Frequencies,1)
                SBAS=1
            else:
                SBAS=0
                Frequencies_Valid&= not DB.SBAS #IF SBAS is meant to be on then make Freq's valid false
                logger.info(DB.Address+":"+str(DB.Port) + " Tracking:: SBAS L1 Disabled")
        else:
            SBAS=0
            Frequencies_Valid=False
            logger.info(DB.Address+":"+str(DB.Port) + " Tracking:: SBAS L1 N/A")

        SBAS_Valid=DB.SBAS==SBAS;

        if not SBAS_Valid:
           Message+="SBAS is: " + str(SBAS) + " Should be: " + str(DB.SBAS)+"\n" # Not dealing with L5 at the moment
           logger.debug(DB.Address+":"+str(DB.Port) + " SBAS:: SBAS Enabled: " + str(DB.SBAS) + " Frequencies: " + str(DB.Frequencies) +" Current SBAS: " + str(SBAS) +  " Valid: " + str(SBAS_Valid) + " Current Freq: " + str(Frequencies))

        DB.STATUS.execute("UPDATE STATUS SET SBAS=?, SBAS_Valid=? where id=?",(SBAS,SBAS_Valid,GNSS_ID))

        if not Frequencies_Valid:
            Message+="Frequencies " + str(Frequencies) + " expected " + str(DB.Frequencies)+"\n";
            logger.debug(DB.Address+":"+str(DB.Port) + " Frequencies:: Frequencies: " + str(Frequencies) + " Valid: " + str(Frequencies_Valid))
        DB.STATUS.execute("UPDATE STATUS SET Frequencies=?, Frequencies_Valid=? where id=?",(Frequencies,Frequencies_Valid,GNSS_ID))
        DB.conn.commit()

        OK=GPS_Valid and GLN_Valid and GAL_Valid and BDS_Valid and SBAS_Valid and QZSS_Valid and Frequencies_Valid
        return (OK,Message)
    else:
        return (False,"Could not determine Tracking\n")

def check_timed(GNSS_ID,DB,HTTP):

    def check_receiver_timed_installed(termLicense,installed,message):
        if termLicense == None:
            if installed:
                result=False
                message+="License check FAILED: No Timed License XML when expected\n"
                logging.warning("termLicense_installed check FAILED: No Timed License XML when expected".format())
                return(result,message)
            else:
                result=True
                logging.info("termLicense_installed check PASSED: No Timed License XML when not expected".format())
                return(result,message)

        termLicense_installed=termLicense.find("./installed")
    #    XML.dump(termLicense_installed)
        if termLicense_installed == None:
            if installed:
                result=False
                message+="License check FAILED: No Timed License when expected\n"
                logging.warning("termLicense_installed check FAILED: No Timed License when expected".format())
            else:
                result=True
                logging.info("termLicense_installed check PASSED: No Timed License when not expected".format())
        else:
            logging.debug("termLicense_installed: {}".format(termLicense_installed.text))
            if installed:
                result=termLicense_installed.text=="1"
                if not result :
                    message+="Termed check FAILED: Expected 1 Got {}\n".format(termLicense_installed.text)
            else:
                result=termLicense_installed.text=="0"
                if not result :
                    message+="Termed check FAILED: Expected 0 Got {}\n".format(termLicense_installed.text)

            if result :
                logging.info("termLicense_installed check: {}".format(result))
            else:
                logging.warning("termLicense_installed check  FAILED: {}".format(result))

        return(result,message)


    def check_receiver_timed_active(termLicense,End_Time_Min,End_Time_Max,message):
        termLicense_active_str=termLicense.find("./extra").text

        if datetime.datetime.utcnow() < End_Time + time_delta:
            result = termLicense_active_str == "Active"
            if result:
                logging.info("termLicense_expired active check: {}".format(termLicense_active_str))
            else:
                message+="Term License active check FAILED: {}\n".format(termLicense_active_str)
                logging.warning("termLicense_expired active check  FAILED: {}".format(termLicense_active_str))
        else:
            result = termLicense_active_str != "Active"
            if result:
                    logging.info("termLicense_expired expired check: {}".format(termLicense_active_str))
            else:
                    logging.warning("termLicense_expired expired check  FAILED: {}".format(termLicense_active_str))

        return(result)

    def check_receiver_timed_range(termLicense,Min_Delta,Max_Delta,message):
        current_time=datetime.datetime.utcnow()
        date_min = current_time + datetime.timedelta(minutes = Min_Delta)
        date_max = current_time + datetime.timedelta(minutes = Max_Delta)

        termLicense_end_date_str=termLicense.find("./status").text
#        print(termLicense_end_date_str)
        try:
            termLicense_end_date=datetime.datetime.strptime(termLicense_end_date_str,"%Y-%m-%d %H:%M")
        except:
            termLicense_end_date=datetime.datetime.strptime(termLicense_end_date_str,"%Y-%m-%d")

        result=True
        if termLicense_end_date < date_min :
            message+="Timed_range min FAILED: Got {} Expected less than {}\n".format(termLicense_end_date, date_min)
            logging.warning("check_receiver_timed_range min FAILED: Got {} Expected more than {}".format(termLicense_end_date, date_min))
            result=False

        if termLicense_end_date > date_max :
            message+="Timed_range max FAILED: Got {} Expected more than {}\n".format(termLicense_end_date, date_max)
            logging.warning("check_receiver_timed_range max FAILED: Got {} Expected less than {}".format(termLicense_end_date, date_min))
            result=False

        return(result,message)

    timed_message=""
    (reply,result)=HTTP.get("/xml/dynamic/merge.xml?config=")
    config = ET.fromstring(reply)
    timed_xml=config.find("./config/termLicense")

#    pprint(timed_xml)
#    pprint(DB.Timed_Active)
#    pprint(timed_message)

    (result,timed_message)=check_receiver_timed_installed(timed_xml,DB.Timed_Active,timed_message)

    if DB.Timed_Active and result:
        (result, timed_message)=check_receiver_timed_range(timed_xml,DB.Timed_Delta_Min,DB.Timed_Delta_Max,timed_message)

    DB.STATUS.execute("UPDATE STATUS SET TIMED_Valid=? where id=?",(result,GNSS_ID))
    DB.conn.commit()

    return(result,timed_message)




DB=DB_Class()
DB.open()
firmware_Versions=DB.read_Firmware_configuration()
DB.read_GNSS_configuration(args.GNSS_ID)


STATUS_Update_Check (DB,args.GNSS_ID,DB.Enabled)

#Here we always have a record for the GNSS receiver we are updating, with null's for the unchecked items.


if not DB.Enabled:
    print "OK: Host Disabled"
    quit(0)

HTTP=HTTP_Class(DB.Address,DB.Port,DB.User_Name,DB.Password,10)
#DB.Password


if not check_firmware_and_password(args.GNSS_ID,DB,HTTP):
    logger.warning(DB.Address+":"+str(DB.Port)+ " Is down or wrong password")
    print "ERROR: Down or wrong password"
    quit(2)
else:
    logger.info(DB.Address+":"+str(DB.Port)+ " Is up")

OK=True
Result_String=""

(Success,Message)=check_firmware(args.GNSS_ID,firmware_Versions,DB,HTTP)
if not Success:
    Result_String+=Message
OK=OK and Success


(Success,Message)=check_Auth(args.GNSS_ID,DB,HTTP)

if not Success:
    Result_String+=Message

OK=OK and Success


(Success,Message)=check_Tracking(args.GNSS_ID,DB,HTTP)

if not Success:
    Result_String+=Message

logger.debug(DB.Address+":"+str(DB.Port)+ " After Tracking: " + str(Success) + ":::" + str(OK)+ " :: " + Message)

OK=OK and Success

(Success,Message)=check_serial_and_type(args.GNSS_ID,DB,HTTP)

if not Success:
    Result_String+=Message

OK=OK and Success

logger.debug(DB.Address+":"+str(DB.Port)+ " After Serial: " + str(Success) + ":::" + str(OK)+ " :: " + Message)

(Success,Message)=check_UPS(args.GNSS_ID,DB,HTTP)

if not Success:
    Result_String+=Message

OK=OK and Success


logger.debug(DB.Address+":"+str(DB.Port)+ " After UPS: " + str(Success) + ":::" + str(OK)+ " :: " + Message)

(Success,Message)=check_Ref(args.GNSS_ID,DB,HTTP)
if not Success:
    Result_String+=Message

OK=OK and Success

(Success,Message)=check_position_type(args.GNSS_ID,DB,HTTP)
if not Success:
    Result_String+=Message

OK=OK and Success

logger.debug(DB.Address+":"+str(DB.Port)+ " After POSITION: " + str(Success) + ":::" + str(OK)+ " :: " + Message)



(Success,Message)=check_motion_type(args.GNSS_ID,DB,HTTP)
if not Success:
    Result_String+=Message

OK=OK and Success

logger.debug(DB.Address+":"+str(DB.Port)+ " After MOTION: " + str(Success) + ":::" + str(OK)+ " :: " + Message)


(Success,Message)=check_antenna(args.GNSS_ID,DB,HTTP)
if not Success:
    Result_String+=Message

OK=OK and Success

logger.debug(DB.Address+":"+str(DB.Port)+ " After ANTENNA: " + str(Success) + ":::" + str(OK)+ " :: " + Message)

(Success,Message)=check_logging(args.GNSS_ID,DB,HTTP)
if not Success:
    Result_String+=Message

OK=OK and Success

(Success,Message)=check_email(args.GNSS_ID,DB,HTTP)
if not Success:
    Result_String+=Message

OK=OK and Success


(Success,Message)=check_clock(args.GNSS_ID,DB,HTTP)
if not Success:
    Result_String+=Message

OK=OK and Success

(Success,Message)=check_PDOP(args.GNSS_ID,DB,HTTP)
if not Success:
    Result_String+=Message

OK=OK and Success

logger.debug(DB.Address+":"+str(DB.Port)+ " After PDOP: " + str(Success) + ":::" + str(OK)+ " :: " + Message)

(Success,Message)=check_Elev(args.GNSS_ID,DB,HTTP)
if not Success:
    Result_String+=Message

OK=OK and Success


(Success,Message)=check_FTP(args.GNSS_ID,DB,HTTP)
if not Success:
    Result_String+=Message

OK=OK and Success

(Success,Message)=check_Power(args.GNSS_ID,DB,HTTP)
if not Success:
    Result_String+=Message

OK=OK and Success

logger.debug(DB.Address+":"+str(DB.Port)+ " After POWER: " + str(Success) + ":::" + str(OK)+ " :: " + Message)

get_Temperature(args.GNSS_ID,DB,HTTP)

get_Warranty(args.GNSS_ID,DB,HTTP)

get_SystemName(args.GNSS_ID,DB,HTTP)

(Success,Message)=check_MultipathReject(args.GNSS_ID,DB,HTTP)
if not Success:
    Result_String+=Message

OK=OK and Success

(Success,Message)=check_testMode(args.GNSS_ID,DB,HTTP)

if not Success:
    Result_String+=Message

logger.debug(DB.Address+":"+str(DB.Port)+ " After TESTMODE: " + str(Success) + ":::" + str(OK)+ " :: " + Message)

OK=OK and Success

if DB.Firmware != "Unmanaged" :
    (Success,Message)=check_errors(args.GNSS_ID,DB,HTTP)

    if not Success:
        Result_String+=Message

    logger.debug(DB.Address+":"+str(DB.Port)+ " After Check Errors: " + str(Success) + ":::" + str(OK)+ " :: " + Message)

    OK=OK and Success


(Success,Message)=check_timed(args.GNSS_ID,DB,HTTP)

if not Success:
    Result_String+=Message

logger.debug(DB.Address+":"+str(DB.Port)+ " After Timed: " + str(Success) + ":::" + str(OK)+ " :: " + Message)

OK=OK and Success



logger.debug(DB.Address+":"+str(DB.Port)+ " After Check Errors: " + str(Success) + ":::" + str(OK)+ " :: " + Message)

if OK:
    (Success,Message)=check_Uptime(args.GNSS_ID,DB,HTTP)
    if Success:
        logger.info(DB.Address+":"+str(DB.Port)+" OK")
        print "OK : " + DB.Address+":"+str(DB.Port)
        quit(0)
    else:
        logger.info(DB.Address+":"+str(DB.Port)+" "+Message)
        print "WARNING : " + DB.Address+":"+str(DB.Port)+" " + Message
        quit(1)
else:
    logger.info(DB.Address+":"+str(DB.Port)+" ERROR: " +Result_String)
    print "ERROR: " + Result_String.encode('utf-8');
    quit(2)

