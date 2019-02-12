#! /bin/bash
echo ""
# Copyright 2005 Trimble

# Usage
# Print usage and exit script
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

Dir=`dirname $0`;
pushd . &>/dev/null
normalDir=`cd "${Dir}";pwd`
PATH=${normalDir}:$PATH
export PATH

 # Tests for curl executable
if ! type curl &> /dev/null ; then
   echo "${0##*/} Required curl executable not found in $PATH" >&2
   exit 2
fi

if ! type firmware_upgrade.sh &> /dev/null ; then
   echo "${0##*/} Required firmware_upgrade.sh not found in $PATH" >&2
   exit 2
fi

if ! type get_clone.sh &> /dev/null ; then
   echo "${0##*/} Required get_clone.sh not found in $PATH" >&2
   exit 2
fi

if ! type send_clone.sh &> /dev/null ; then
   echo "${0##*/} Required send_clone.sh not found in $PATH" >&2
   exit 2
fi

if ! type receiver_version.pl &> /dev/null ; then
   echo "${0##*/} Required receiver_version.pl not found in $PATH" >&2
   exit 2
fi

if ! type Receiver_Firmware_Status.pl &> /dev/null ; then
   echo "${0##*/} Required Receiver_Firmware_Status.pl not found in $PATH" >&2
   exit 2
fi



userpass="admin:password";
failsafe="yes";
clone="";
proxy="";
run="1";
resend="";

while getopts "p:i:c:f:s:zn" options; do
   case $options in
       p ) userpass=$OPTARG;;
       i ) ip=$OPTARG;;
       c ) clone=$OPTARG;;
       f ) file=$OPTARG;;
       z ) proxy="-z";;
       n ) run="";resend="no";;
       u ) resend="no";;
       * ) Usage;;
   esac
done

if [ -z "$ip" ]; then
    echo "Need IP address";
    Usage;
fi

if [ ! -z "$file" ]; then
   if [ ! -e "$file" ]; then
      echo "Firmware file does not exist";
      Usage;
   fi;
fi

if  ((${#clone} > 7))
then
   echo "Clone file name must be 7 characters or less"
   exit 2
fi

#echo "$ip"

#ping -c 3 $ip >/dev/null
echo "Getting Receiver Version for $ip"
curl --silent -o "Version_$$.xml" "http://$userpass@$ip/xml/dynamic/merge.xml?sysData="

if [ -e "Version_$$.xml" ]
then
#   cat "Version_$$.xml"
   receiver_version.pl "Version_$$.xml"
   rm "Version_$$.xml"
   if [ -n "$clone" ]
       then
       echo "Getting Current Settings for $ip"
       get_clone.sh -i $ip -c $clone -p $userpass  $proxy || (echo "Getting Clone File Failed"; exit 2)
       fi
else
   echo "Could not communicate with the receiver at $ip. Upgrade aborted"
   exit 1
fi


if [ -n "$run"  ]; then
    if [ ! -e $file ]; then
    echo "Need local file name";
    Usage;
    fi

#    echo "Upgrading firmware for $ip"
    firmware_upgrade.sh  -i $ip -f $file -p $userpass $proxy&
#    echo Wait for receiver to reboot and format, which can take upto 5 minutes
    Receiver_Firmware_Status.pl $userpass@$ip
    echo "Receiver $ip upgraded"
fi

if [ -z $resend ]
then
   echo "Waiting for receiver $ip to reboot."
   sleep 60
   echo "Sending Clone file to $ip"
   send_clone.sh -i $ip -c $clone -p $userpass $proxy
   echo "Rebooting receiver $ip to apply clone file"
#   sleep 60
#   echo "Receiver $ip settings restored"
fi

#Do not send the clone file until the receiver has rebooted
