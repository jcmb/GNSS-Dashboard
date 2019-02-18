#! /usr/bin/env python

import sys
import time
import argparse
import os
import requests
import time
import datetime


from xml.etree.ElementTree import parse, dump, fromstring
from pprint import pprint

import logging
logging.basicConfig(level=logging.WARNING)
# Replacement for the upgrade with Clone script. 
# 
# Better understandability, logging, status and error reporting are the primary goals of the rewrite
"""
Usage () {
  echo $*
  echo ""
  echo "Usage: ${0##*/} [-h] [-p user:passwd] [-c clone_file] -i IP -f local_file [-z]"
  echo "Backup the configuration of the receiver, upgrade and restore a reciever at 'IP' with 'local_file'"
  echo "  -h = get help"
  echo "  -p user:passwd = don't use default user=admin,passwd=password"
  echo "  -i IP = receiver IP"
  echo "  -f filename = local filename for firmware"
  echo "  -c filename = local filename for clone file. Required if more than one copy of upgrade_with_clone is running"
  echo "  -z upload through the proxy"
  echo "  -n Do not upgrade the receiver, just get the current settings"
  echo "  -u Upgrade the receiver only do not resend current settings"
  exit 1
}

"""

def create_arg_parser():
    usage="Check_Total_Connections.py [options] [server] [port] "
    parser=argparse.ArgumentParser()


    parser.add_argument("-i", "--IP", type=str, required=True,help="IP Address of the GNSS receiver")
    parser.add_argument("-p", "--user", type=str,default="admin:password", help="Username:Password Default: %(default)s" )

    parser.add_argument("-v", "--verbose", action="count", dest="verbose", default=False, help="Verbose")
    parser.add_argument("-T", "--tell",action="store_true", dest="tell", default=False, help="Tell the settings for the run")

    parser.add_argument("-c", "--clone", type=str, default="JCMB", help="Clone file to save settings on the receiver.  8 characters or less")
    parser.add_argument("-D", "--clonedate", action="store_true", help="Add the current date time to the Clone files that are saved")
    parser.add_argument("-d", "--clonedir", type=str, help="Directory to save settings files to. Without the \\. Clone files are not saved otherwise")
    parser.add_argument("-f", "--firmware", type=str, help="Firmware file to upload, required unless --n is used")

    parser.add_argument("-n", "--no_upgrade", action="store_true", help="Do not upgrade the firmware, just get the settings")
    parser.add_argument("-u", "--upgrade_only",action="store_true", help="Only upload the firmware, do not resend the configuration")

    parser.add_argument("-z", "--proxy", action="store_true", dest="proxy", default=False, help="Ignored")

    return (parser)

def process_arguments ():
    parser=create_arg_parser()
    options = parser.parse_args()
#    print options
    IP=options.IP
    USER=options.user      
    VERBOSE=options.verbose
    CLONE_FILE=options.clone.upper()
# Must be in upper case, yes really
# Technically it can be in any case to create, will be in upper to download  
    CLONE_DATE=options.clonedate
    CLONE_DIR=options.clonedir

    FIRMWARE_FILE=options.firmware
    NO_UPGRADE=options.no_upgrade
    UPGRADE_ONLY=options.upgrade_only
    
    if FIRMWARE_FILE==None and not NO_UPGRADE:
      sys.exit("Firmware file not provided when upgrading, aborting")
      
    if UPGRADE_ONLY and NO_UPGRADE:
      sys.exit("Can not have No Upgrade and Upgrade only at the same time")
      

    if options.tell:
        print "Server: " + IP
        print "User: " + USER
        print "Clone: %r" % CLONE_FILE
        print "Clone Directory: %r" % CLONE_DIR
        print "Firmware: %r" % FIRMWARE_FILE
        print "No upgrade: %r" % NO_UPGRADE
        print "Upgrade Only: %r" % UPGRADE_ONLY
        print "Verbose: %r" % VERBOSE
        print
    
    return (IP,USER,VERBOSE,CLONE_FILE,CLONE_DIR,CLONE_DATE,FIRMWARE_FILE,NO_UPGRADE,UPGRADE_ONLY)



def Get_Version (IP,USER):
   Version=None
   r=None
   try:
      r = requests.get('http://{}@{}/xml/dynamic/merge.xml?sysData='.format(USER,IP))
   except:
      pass
      
   if r == None:
      logging.warning("Could not connect to receiver at {}".format(IP))
      sys.exit("Could not connect to receiver at {}".format(IP))

   if r.status_code <> 200:
      logging.warning("Error Connecting to receiver at {} Error Code: {}".format(IP,r.status_code))
      sys.exit("Error Connecting to receiver at {} Error Code: {}".format(IP,r.status_code))

   xml_reply = fromstring(r.text)
#   dump(xml_reply)
   logging.info("GNSS Receiver: {}".format(IP))
   logging.info("Serial: {}".format(xml_reply.find("sysData/serial").text))
   Version=float((xml_reply.find("sysData/ProductFwVer").text))
   logging.debug("FW Version: {}".format(Version))
   logging.debug("FW Extended Version: {}".format(xml_reply.find("sysData/FWVersion").text))
   logging.debug("Current Firmware Date: {}".format( xml_reply.find("sysData/FWDate").text))
   logging.debug("Warranty Date: {}".format( xml_reply.find("sysData/WarrantyDate").text))
   logging.debug("Min Firmware Date: {}".format( xml_reply.find("sysData/MinFWDate").text))
   logging.debug("Downgrade limit: {}".format( xml_reply.find("sysData/DowngradeLimit").text))
   logging.debug("Hardware Type: {}".format( xml_reply.find("sysData/hardware").text))
   logging.debug("Hardware Family: {}".format( xml_reply.find("sysData/family").text))
   logging.debug("Hardware Build Type: {}".format( xml_reply.find("sysData/build").text))
   logging.debug("Monitor Verision: {}".format( xml_reply.find("sysData/MonVersion").text))
   logging.debug("Receiver Name: {}".format( xml_reply.find("sysData/RXName").text))
   logging.debug("RTK Version: {}".format( xml_reply.find("sysData/RTKversion").text))
   if xml_reply.find("sysData/RTXversion") is not None:
       logging.debug("RTX Version: {}".format( xml_reply.find("sysData/RTXversion").text))
   if xml_reply.find("sysData/T01Ver") is not None:
       logging.debug("T0x Version: {}".format( xml_reply.find("sysData/T01Ver").text))
   if xml_reply.find("sysData/RTXversion") is not None :
       logging.debug("Antenna.ini Version: {}".format( xml_reply.find("sysData/antennaINI").text))

   logging.info("Option Key: {}".format( xml_reply.find("sysData/FullOptionKey").text))
   
   return (Version)

def Create_Clone(IP,USER,Version,Clone_Short_Name):
   r=None
   try:
#  http://sps855.com/CACHEDIR2212516474/cgi-bin/app_fileUpdate.xml?operation=8&fileNumber=3&cloneFileName=WCO.xml&csibFileName=17021201.T02&Year=2016&Month=1&Day=1&Hour=0&Minute=0&RepeatMin=0&newAppFileName=&newCloneFileName=Test&cloneSecurityEnable=on&cloneTcpUdpPortEnable=on&cloneEtherBootEnable=on&cloneHttpEnable=on&cloneEmailFtpNtpEnable=on&cloneDataLoggerEnable=on&clonePositionEnable=on&cloneAlmEnable=on&cloneMiscellaneousEnable=on&cloneAllAppfilesEnable=on
#  http://sps855.com/CACHEDIR2212516474/cgi-bin/app_fileUpdate.xml?operation=8&fileNumber=3&cloneFileName=TEST3.xml&csibFileName=17021201.T02&Year=2016&Month=1&Day=1&Hour=0&Minute=0&RepeatMin=0&newAppFileName=&newCloneFileName=TEST4&cloneSecurityEnable=on&cloneTcpUdpPortEnable=on&cloneEtherBootEnable=on&cloneHttpEnable=on&cloneEmailFtpNtpEnable=on&cloneDataLoggerEnable=on&clonePositionEnable=on&cloneAlmEnable=on&cloneMiscellaneousEnable=on
#  GET              /CACHEDIR2212516474/cgi-bin/app_fileUpdate.xml?operation=8&fileNumber=3&csibFileName=17021203.T0B&Year=2016&Month=1&Day=1&Hour=0&Minute=0&RepeatMin=0&newAppFileName=&newCloneFileName=WEB_TEST&cloneSecurityEnable=on&cloneTcpUdpPortEnable=on&cloneEtherBootEnable=on&cloneHttpEnable=on&cloneEmailFtpNtpEnable=on&cloneDataLoggerEnable=on&clonePositionEnable=on&cloneAlmEnable=on&cloneMiscellaneousEnable=on HTTP/1.1   
      r = requests.get('http://{0}@{1}/cgi-bin/app_fileUpdate.xml?operation=8&fileNumber=1&cloneFileName={2}.xml&Year=2010&Month=1&Day=1&Hour=0&Minute=0&RepeatMin=0&newAppFileName=&newCloneFileName={2}&cloneSecurityEnable=on&cloneTcpUdpPortEnable=on&cloneEtherBootEnable=on&cloneHttpEnable=on&cloneEmailFtpNtpEnable=on&cloneDataLoggerEnable=on&clonePositionEnable=on&cloneMiscellaneousEnable=on'.
         format(USER,IP,Clone_Short_Name))
   except:
      pass
      
   if r == None:
      logging.warning("Could not connect to receiver at {} to make clone".format(IP))
      sys.exit("Could not connect to receiver at {}  to make clone".format(IP))

   if r.status_code <> 200:
      logging.warning("Error Connecting to receiver at {} Error Code: {} making clone ".format(IP,r.status_code))
      sys.exit("Error Connecting to receiver at {} Error Code: {} making clone".format(IP,r.status_code))


   Clone_In_Process=True
   Count=0
   
   while Clone_In_Process:
      r = requests.get('http://{}@{}/xml/dynamic/cloneFileStatus.xml'.
            format(USER,IP))
   
      if (r.status_code == 200) :
#        print r.text 
        xml_reply = fromstring(r.text)
#        dump(xml_reply)
        State=xml_reply.find("cloneOperationStatus").text
        if State=="0":
         Clone_In_Process=False
         logging.debug("Clone Created")
        else:
         Count+=1
         if Count <= 60:
            time.sleep(2) 
         else:
            logging.error("Clone was not Created in 2 minutes on receiver {}".format(IP))
            sys.exit("Clone was not Created in 2 minutes on receiver {}".format(IP))
         
      else:
         logging.warning("Error checking clone stations {} Error Code: {} making clone ".format(IP,r.status_code))
         sys.exit("Error checking clone stations {} Error Code: {} making clone".format(IP,r.status_code))
   return (True)

def Get_Clone(IP,USER,Clone_Short_Name,Clone_Dir,Clone_Date):
   r=None
   try:
      r = requests.get('http://{0}@{1}/clone_file/{2}.xml?gzipFlag=false'.
         format(USER,IP,Clone_Short_Name))
   except:
      pass
      
   if r == None:
      logging.error("Could not connect to receiver at {} to get clone".format(IP))
      sys.exit("Could not connect to receiver at {}  to get clone".format(IP))

   if r.status_code <> 200:
      logging.error("Error Connecting to receiver at {} Error Code: {} getting clone {}".format(IP,r.status_code,Clone_Short_Name))
      sys.exit("Error Connecting to receiver at {} Error Code: {} getting clone {} ".format(IP,r.status_code,Clone_Short_Name))

   if r.text =="<FAIL>1</FAIL>":
      logging.error("Failed to download clone from receiver at {}, Check password".format(IP))
      sys.exit("Failed to download clone from receiver at {}, Check password".format(IP))
   
   xml_reply=None
   try:
      xml_reply = fromstring(r.text)
      if Clone_Dir!=None:
         if Clone_Date:
            Clone_Filename=Clone_Dir+'/'+Clone_Short_Name+"-"+datetime.datetime.now().strftime("%Y-%m-%d")+".xml"
         else:
            Clone_Filename=Clone_Dir+'/'+Clone_Short_Name+".xml"
         logging.info("Creating clone file: " + Clone_Filename)
         clone_file=open(Clone_Filename,"w")
         clone_file.write(r.text)
         clone_file.close()
   except:
      pass
      
   return (r.text)


def Upgrade_Firmware(IP,USER,FIRMWARE_FILE):

   r=None
   logging.info("Starting upgrade of receivers at {}".format(IP))

   try:
      files = {'myfile': open(FIRMWARE_FILE, 'rb')}
      r = requests.post("http://{0}@{1}/prog/Upload?FirmwareFile&failsafe=yes".format(USER,IP), files=files)
      
   except:
      pass
      
   if r == None:
      logging.error("Could not connect to receiver at {} to upload firmware. Wrong Firmware Image or password?".format(IP))
      sys.exit("Could not connect to receiver at {}  to upload firmware. Wrong Firmware Image or password?".format(IP))

   if r.status_code <> 200:
      logging.error("Error Connecting to receiver at {} Error Code: {} uploading firmware {}".format(IP,r.status_code,Clone_Short_Name))
      sys.exit("Error Connecting to receiver at {} Error Code: {} uploading firmware {} ".format(IP,r.status_code,Clone_Short_Name))

   
   
   Upgrade_In_Process=True
   Count=0
   Last_State=None
   while Upgrade_In_Process:
      r = requests.get("http://{0}@{1}/xml/dynamic/merge.xml?firmware_status=".
            format(USER,IP))
   
      if (r.status_code == 200) :
#        print r.text 
        xml_reply = fromstring(r.text)
#        dump(xml_reply)
        State=xml_reply.find("fw_status/status/mode").text
#        print State
        if State != Last_State:
          Count=0
          Last_State=State
          logging.debug("Firmware Upgrade in state: {}".format(State))
        else:
         Count +=1

        if State=="FIRMWARE_DONE" or State=="FIRMWARE_INTERRUPTED":
           Upgrade_In_Process=False
           continue
            
        if State=="FIRMWARE_IDLE" and Count>5:
          logging.error("Firmware Upgrade did not start for: {}".format(IP))
          sys.exit("Firmware Upgrade did not start for: {}".format(IP))
            
        if Count<=120:
          time.sleep(2)
        else:
          logging.error("Firmware Upgrade stayed in state {] for more than 4 minutes for receiver {}".format(State,IP))
          sys.exit("Firmware Upgrade stayed in state {] for more than 4 minutes for receiver {}".format(State,IP))
   return (State=="FIRMWARE_DONE")

def Send_Clone(IP,USER,Clone_Short_Name,Clone_Data):
   r=None
   files = {'myfile': (Clone_Short_Name+'.xml', Clone_Data)}
   
   r = requests.post("http://{0}@{1}/cgi-bin/clone_fileUpload.html?cloneUploadName=&installCloneFile=true&installStaticIpAddr=false&clearBeforeInstallCloneFile=true".format(USER,IP), files=files)
   try:
      pass      
   except:
      pass
      
   if r == None:
      logging.error("Could not connect to receiver at {} to send clone".format(IP))
      sys.exit("Could not connect to receiver at {}  to send clone".format(IP))

   if r.status_code <> 200:
      logging.error("Error Connecting to receiver at {} Error Code: {} sending clone {}".format(IP,r.status_code,Clone_Short_Name))
      sys.exit("Error Connecting to receiver at {} Error Code: {} sending clone {} ".format(IP,r.status_code,Clone_Short_Name))

   r = requests.get("http://{0}@{1}/cgi-bin/resetPage.xml?doReset=1".format(USER,IP))


(IP,USER,VERBOSE,CLONE_FILE,CLONE_DIR,CLONE_DATE,FIRMWARE_FILE,NO_UPGRADE,UPGRADE_ONLY) = process_arguments()

if VERBOSE:
   logging.basicConfig(level=logging.DEBUG)

if not NO_UPGRADE:
   if not os.path.isfile(FIRMWARE_FILE):
      sys.exit("The firmware file {} does not exist".format(FIRMWARE_FILE))


logging.info("Getting Receiver Version for "+ IP)


Version=Get_Version(IP,USER)

if Create_Clone(IP,USER,Version,CLONE_FILE):
   Clone=Get_Clone(IP,USER,CLONE_FILE,CLONE_DIR,CLONE_DATE)
   if Clone == None:
     logging.error("Could not get clone from receiver at  {}".format(IP))
     sys.exit("Could not get clone from receiver at  {}".format(IP))


if NO_UPGRADE:
    print CLONE_FILE + " Created"
else:
   if Upgrade_Firmware(IP,USER,FIRMWARE_FILE):
      if not UPGRADE_ONLY:
         logging.info("Waiting 2 minutes for unit to reboot after GNSS upgrade {}".format(IP))
         time.sleep(120)
         Send_Clone(IP,USER,CLONE_FILE,Clone)

