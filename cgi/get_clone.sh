#! /bin/bash

Dir=`dirname $0`;
pushd . &>/dev/null
normalDir=`cd "${Dir}";pwd`
PATH=${normalDir}:$PATH
export PATH

# Copyright 2005 Trimble

# Usage
# Print usage and exit script
Usage () {
  echo "Usage: ${0##*/} [-h] [-p user:passwd] -i IP -c local_file [-z]"
  echo "Download the current settings, in clone format,  of a receiver at 'IP' saved to 'local_file'"
  echo "  -h = get help"
  echo "  -p user:passwd = don't use default user=admin,passwd=password"
  echo "  -i IP = receiver IP"
  echo "  -c filename = local filename"
  echo "  -z Download through the proxy"
  exit 1
}

 # Tests for curl executable
if ! type curl &> /dev/null ; then
   echo "Required curl executable not found in $PATH" >&2
   exit 2
fi

if ! type Check_Clone_Valid.pl  &> /dev/null ; then
   echo "Required Check_Clone_Valid.pl $file.xml executable not found in $PATH" >&2
   exit 2
fi

if ! type Receiver_Clone_Status.pl  &> /dev/null ; then
   echo "Required Receiver_Clone_Status.pl  executable not found in $PATH" >&2
   exit 2
fi



userpass="admin:password";
failsafe="no";
proxy="disable";
while getopts "p:i:c:s:z" options; do
   case $options in
       p ) userpass=$OPTARG;;
       i ) ip=$OPTARG;;
       c ) file=$OPTARG;;
       z ) proxy="enable";;
       * ) Usage;;
   esac
done

if [ -z $ip ]; then
    echo "Need IP address";
    Usage;
fi

if [ -z $file ]; then
    echo "Need local file name";
    Usage;
fi

toUpper() {
echo $1 | tr  "[:lower:]" "[:upper:]"
}

file=`toUpper $file`

if [ $proxy != "enable" ]; then
    unset http_proxy
fi


echo "Creating clone file for $ip"
curl --silent -o /dev/null --cookie "LoggedIn=yes"  "http://$userpass@$ip/cgi-bin/app_fileUpdate.xml?operation=8&fileNumber=1&cloneFileName=$file.xml&Year=2010&Month=1&Day=1&Hour=0&Minute=0&RepeatMin=0&newAppFileName=&newCloneFileName=$file&cloneSecurityEnable=on&cloneTcpUdpPortEnable=on&cloneEtherBootEnable=on&cloneHttpEnable=on&cloneEmailFtpNtpEnable=on&cloneDataLoggerEnable=on&clonePositionEnable=on&cloneMiscellaneousEnable=on"

#echo sleeping 10 seconds
sleep 1
Receiver_Clone_Status.pl $ip $userpass $ip

echo "Downloading clone file from $ip $file.xml"
curl --silent --cookie "LoggedIn=yes"  -o $file.xml  "http://$userpass@$ip/clone_file/$file.xml?gzipFlag=false"
Check_Clone_Valid.pl $file.xml 2> /dev/null
#echo $?
exit $?
