#! /bin/bash

# Copyright 2005 Trimble
# $Id: upgradeFW.sh,v 1.11 2010/10/01 23:47:05 wlentz Exp $

# Usage
# Print usage and exit script
Usage () {
  echo "Usage: ${0##*/} [-h] [-s failsafe] [-p user:passwd] -i IP -f local_file [-z]"
  echo "Upgrade of receiver at 'IP' with 'local_file'"
  echo "  -h = get help"
  echo "  -p user:passwd = don't use default user=admin,passwd=password"
  echo "  -i IP = receiver IP"
  echo "  -f filename = local filename"
  echo "  -z Upgrade through the proxy"
  exit 1
}

 # Tests for curl executable
if ! type curl &> /dev/null ; then
   echo "Required curl executable not found in $PATH" >&2
   exit 2
fi

userpass="admin:password";
failsafe="yes";
proxy="disable";
while getopts "p:i:f:s:z" options; do
   case $options in
       p ) userpass=$OPTARG;;
       i ) ip=$OPTARG;;
       f ) file=$OPTARG;;
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

if [ $proxy != "enable" ]; then
    unset http_proxy
fi

echo "Upgrading Firmware for $ip"
#echo curl --silent  -F myfile=@$file "http://$userpass@$ip/prog/Upload?FirmwareFile&failsafe=$failsafe"
curl --silent  -F myfile=@$file "http://$userpass@$ip/prog/Upload?FirmwareFile&failsafe=$failsafe"

