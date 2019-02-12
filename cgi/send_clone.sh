#! /bin/bash

# Copyright 2005 Trimble

# Usage
# Print usage and exit script
Usage () {
  echo "Usage: ${0##*/} [-h] [-p user:passwd] -i IP -c local_file [-z]"
  echo "Send a clone file to a reciever at 'IP' with 'local_file'"
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

toUpper() {
echo $1 | tr  "[:lower:]" "[:upper:]"
}

file=`toUpper $file`

if [ ! -e $file ]; then
    if [ ! -e $file.xml ]; then
    echo "Need local file name";
    Usage;
    else
    file=$file.xml
    fi
fi

if [ $proxy != "enable" ]; then
    unset http_proxy
fi


#curl --silent  -F myfile=@$file "http://$userpass@$ip/cgi-bin/clone_fileUpload.xml?installCloneFile=true&installStaticIpAddr=false&cloneUploadName=" >/dev/null
curl -H 'Cookie: LoggedIn=yes'  -F myfile=@$file -u $userpass "http://$ip/cgi-bin/clone_fileUpload.html?installCloneFile=true&installStaticIpAddr=false&clearBeforeInstallCloneFile=false"

curl --silent "http://$userpass@$ip/cgi-bin/resetPage.xml?doReset=1" >/dev/null
