#!/usr/bin/env python3

import sys
import requests
import argparse
import time
from lxml import etree
from pprint import pprint
from zipfile import ZipFile
import os
import re
from tempfile import gettempdir


def get_args():

   parser = argparse.ArgumentParser(fromfile_prefix_chars="@",description='Log raw TCP Data to a file with ', epilog="V1.0 (c) JCMBsoft 2022", formatter_class=argparse.ArgumentDefaultsHelpFormatter);
   parser.add_argument("host", help="Remote Host",)
   parser.add_argument("port", help="Remote Port",type=int)
   parser.add_argument("user", help="User Name",)
   parser.add_argument("password", help="User Password",)
   parser.add_argument("baseName", help="Base FileName for the log files")
   parser.add_argument("--Clear", help="clear the error log", action="store_true")
   parser.add_argument("--Clone", help="Download the clone", action="store_true")
   parser.add_argument("--Tell", "-T", help="Tell Settings",action="store_true")
   parser.add_argument("--Date", "-D", help="Include Date in name",action="store_true")
   parser.add_argument("--Verbose","-v", help="Verbose",action="store_true")
   parser.add_argument("--View", help="View error log",action="store_true")

   parser.add_argument("--Zip","-Z", help="Zipped the files",action="store_true")


   parser = parser.parse_args()




   if parser.Tell :
      sys.stderr.write("Host: {}\n".format(parser.host))
      sys.stderr.write("Port: {}\n".format(parser.port))
      sys.stderr.write("User: {}\n".format(parser.user))
      sys.stderr.write("Password: {}\n".format(parser.password))
      sys.stderr.write("baseName: {}\n".format(parser.baseName))
      sys.stderr.write("Clear: {}\n".format(parser.Clear))
      sys.stderr.write("Date: {}\n".format(parser.Date))
      sys.stderr.write("Verbose: {}\n".format(parser.Verbose))
   return (vars(parser))



def SendHttpPost(IPAddr,cmdstr,user,password, timeout=10):
  url_str = "http://" + IPAddr + cmdstr
  r = requests.post(url_str, auth=(user,password), timeout=timeout)
  r.raise_for_status()
  return r.text

def SendAndCheckHttpPost(IPAddr,cmd,user,password,check_response="<OK>1</OK>"):
  response = SendHttpPost(IPAddr,cmd,user,password)
  if check_response not in response:
    raise RuntimeError("Web interface returned an error: %s" % response)

def SendHttpGet(IPAddr,loc,user,password, verbose=False ,proxies={}, timeout=10, secure=False):
    """Get a URL from the receiver through HTTP GET http://IPAddr + loc
    If proxies={}, use the automatically-detected proxy info (e.g.,
      http_proxy environment variable).
    If proxies={'http':None}, disable HTTP proxy use.
    """

    if(secure == False):
      url_str = "http://" + IPAddr + loc
    else:
      url_str = "https://" + IPAddr + loc
      # As the certificate from our receivers can't be authenticated we're going to turn
      # off validating it. However, this causes a warning so make sure we suppress that.
      requests.packages.urllib3.disable_warnings()

    if(verbose):
      print(url_str)

    if(secure == False):
      r = requests.get(url_str, auth=(user,password), proxies=proxies, timeout=timeout)
    else:
      # HTTPS request (without validating the certificate)
      r = requests.get(url_str, auth=(user,password), proxies=proxies, timeout=timeout, verify=False)

    r.raise_for_status()
    return r.text


def IsTestModeEnabled(IPAddr,user,password):
  """Check if test mode is enabled on receiver"""
  txt = SendHttpGet(IPAddr,"/xml/dynamic/sysData.xml",user,password)
  d = etree.fromstring( txt )
  testMode = d.find('testMode')
  if testMode is not None and testMode.text == 'TRUE':
    return True
  return False

def DisableTestMode(IPAddr,user,password):
  """Disable test mode on receiver."""
  # Sending any password (other than the testmode PW) will turn off
  # testmode
  SendHttpGet(IPAddr,"/cgi-bin/testMode.xml?Password=Anything",user,password)

def EnableTestMode(IPAddr,user,password):
  """Enable test mode on receiver.  Some commands below only work in test mode..."""
  test_password_list = ["TURING","EUCLIDEAN","EUCLID","FARADAY"]
  for test_pw in test_password_list:
    if IsTestModeEnabled(IPAddr,user,password):
      break
    SendHttpGet(IPAddr,"/cgi-bin/testMode.xml?Password=%s"%test_pw,user,password)


def ClearErrorLog(IPAddr,user,password):
  ClearLog = "/cgi-bin/eraseErrorLog.xml"
  SendAndCheckHttpPost(IPAddr,ClearLog,user,password)


# Download the system error log to 'filename'
def DownloadSystemErrlog(IPAddr,user,password,filename,date_str, timeout=10.0):
  # Some firmware versions hang when trying to download an errlog
  # with nothing in it, so check for that first...
  filename=filename+date_str
#  pprint(timeout)

  url = "http://%s:%s@%s/xml/dynamic/errLog.xml" % (user,password,IPAddr)
  r = requests.get( url, timeout=timeout )
  r.raise_for_status()
  if 'numEntries>0<' in r.text:
#    open(f'{filename}.bin', 'wb').close()

    return (False)

  with open(f'{filename}.bin','wb') as f:
    url = "http://%s:%s@%s/xml/dynamic/SysLog.bin" % (user,password,IPAddr)
    r = requests.get( url, timeout=timeout )
    r.raise_for_status()
    f.write( r.content )

  url = "http://%s:%s@%s/xml/dynamic/errorLog.txt" % (user,password,IPAddr)
  r = requests.get( url, timeout=timeout )
  r.raise_for_status()

  with open(f'{filename}.xml','w') as f:
    f.write( r.text )

  return (True)


def CheckCloneStatus(IPAddr,user,password):
  """Clone operations can take a second or two and the status is stored in a global
  variable.  Check the status of any clone file operation.
  Returns (True, status_xml_string) if everything went OK.
  Returns (False, status_xml_string) if there was an error.
  """
  count = 0
  while True:
    raw = SendHttpGet(IPAddr,'/xml/dynamic/cloneFileStatus.xml',user,password)
#    pprint(raw)
    d = etree.fromstring( raw )
    status = int(d.find('cloneOperationStatus').text)
    if status == 1: # Clone_Op_InProgWait
      time.sleep(1)
      count = count + 1
      if count > 30:
        return (False, raw)
      continue
    elif status == 0: # Clone_Op_OK
      return (True, raw)
    else:
      return (False, raw)



# Clone all the receiver's configuration
def CloneAllConfig(IPAddr,user,password,filename):
  filename = filename.strip('.xml')
  filename = filename.upper() # force to upper case

  CloneCommand = (   '/cgi-bin/app_fileUpdate.xml?operation=8&newCloneFileName=' + filename
                   + '&cloneTcpUdpPortEnable=on'
                   + '&cloneEtherBootEnable=on'
                   + '&cloneHttpEnable=on'
                   + '&cloneEmailFtpNtpEnable=on'
                   + '&cloneDataLoggerEnable=on'
                   + '&clonePositionEnable=on'
                   + '&cloneAlmEnable=on'
                   + '&cloneMiscellaneousEnable=on'
                   + '&cloneAllAppfilesEnable=on')

#  pprint(CloneCommand)

  SendAndCheckHttpPost(IPAddr,CloneCommand,user,password)
  result = CheckCloneStatus(IPAddr,user,password)
#  pprint(result) 
  if result[0] == False:
    raise RuntimeError("Couldn't CloneAllConfig: {}".format(result[1]))


# Download the cloned GNSS configuration
def DownloadClone(IPAddr,user,password,basename,filename,date_str, timeout=10.0):

#<  pprint(timeout) 

  remote_filename = basename.upper() + '.xml' # force to upper case

  url = "http://%s:%s@%s/clone_file/%s?gzipFlag=false" % (user,password,IPAddr,remote_filename)
#  print(url)
  r = requests.get( url, timeout=timeout )
  r.raise_for_status()
#  print(r.text)

#  print(r.text.split()[0])
  if len(r.text) != 0 and r.text.split()[0].startswith('<FAIL'):
    raise RuntimeError("Tried to download clone but got bad response: %s" % r.text)

  clone_filename=filename+date_str+".clone.xml"

  with open(clone_filename,'wb') as f:
    f.write( r.content )


def CreateAndDownloadClone(IPAddr,user,password,baseName,filename,date_str):
    CloneAllConfig(IPAddr,user,password,baseName)
    DownloadClone (IPAddr,user,password,baseName,filename,date_str)


def Display_Error_Log(filename):
    with open(filename) as f:
        errors = etree.parse( f )
        print("{:3} {:7} {:30} {:10} {:6} {:20} {:20}".format("ID","Type","FW","UpTime","Task#","Task Name","Type"))
        Err_pattern = re.compile("Err:(.*?) tsk:(.*?):(.*?) t:.*:.* up:(.*) flags:.*\nRx:.* fw:(.*)\n")
        Warn_pattern = re.compile("Warn:(.*?) tsk:(.*?):(.*?) t:.*:.* up:(.*) flags:.*\nRx:.* fw:(.*)\n")

        for error in errors.iter('log'):
#            pprint(error.text.strip())l
            match=(Err_pattern.search(error.text.strip()))
            if match:
                print("{:3} {:7} {:30} {:10} {:6} {:20} {:20}".format(error.attrib["index"], "Error" ,match.group(5), match.group(4), match.group(2), match.group(3), match.group(1), match.group(0)))
            else:
                match=(Warn_pattern.search(error.text.strip()))
                if match :
                   print("{:3} {:7} {:30} {:10} {:6} {:20} {:20}".format(error.attrib["index"], "Warning", match.group(5), match.group(4), match.group(2), match.group(3), match.group(1),match.group(0)))
                else:
                   print("{:3} {:7} {:30} {:10} {:6} {:20} {:20}".format(error.attrib["index"], "Unknown", match.group(5), match.group(4), match.group(2), match.group(3), match.group(1),match.group(0)))
#        pprint(errors)


def main():
    args=get_args()
    args["host"]=args["host"].replace("http://","")
    args["host"]=args["host"].replace("HTTP://","")
    if args["Date"]:
       date_str="."+ time.strftime("%Y%m%d-%H%M%S")
    else:
       date_str=""

    baseName=os.path.join(gettempdir(),args["baseName"])
#    print(baseName)


    if args["Clone"]:
        CreateAndDownloadClone(args["host"]+":"+str(args["port"]),args["user"],args["password"], args["baseName"], baseName , date_str)


    if not DownloadSystemErrlog(args["host"]+":"+str(args["port"]),args["user"],args["password"] , baseName , date_str):
        sys.stderr.write("No Error Logs on the device\n")
    else:
        if args["View"]:
            Display_Error_Log(baseName+date_str+".xml")

        if args["Clear"]:
            ClearErrorLog(args["host"]+":"+str(args["port"]),args["user"],args["password"])

        if args["Zip"]:
            os.chdir(gettempdir())
            with ZipFile(baseName + date_str+".zip", 'w') as myzip:
                myzip.write(args["baseName"] + date_str+".xml")
                myzip.write(args["baseName"] + date_str+".bin")

                if args["Clone"]:
                    myzip.write(args["baseName"]+date_str+".clone.xml")

            os.remove(baseName+date_str+".xml")
            os.remove(baseName+date_str+".bin")
            if args["Clone"]:
                os.remove(baseName+date_str+".clone.xml")



if __name__ == '__main__':
    main()

