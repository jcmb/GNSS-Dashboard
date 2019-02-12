#! /bin/bash

echo -e "Content-type: text/html\r\n\r\n"
echo -e "<html><head><title>Upgrade Start</title></head><body>"

Dir=`dirname $0`;
pushd . &>/dev/null
normalDir=`cd "${Dir}";pwd`
#echo $PATH                                                                                                                                                          
PATH=${normalDir}:$PATH
version=`echo "$QUERY_STRING" | sed -n 's/^.*version=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"`
#version=490_024

if [ -z $version ]
then
  echo "You must provide the version number to upgrade to"
  exit;
fi

Sunnyvale=`echo "$QUERY_STRING" | sed -n 's/^.*GNSS=\(Sunnyvale\).*$/\1/p' | sed "s/%20/ /g"`
Westminster=`echo "$QUERY_STRING" | sed -n 's/^.*GNSS=\(Westminster\).*$/\1/p' | sed "s/%20/ /g"`

WCOALL=`echo "$QUERY_STRING" | sed -n 's/^.*GNSS=\(WCOALL\).*$/\1/p' | sed "s/%20/ /g"`
Choke=`echo "$QUERY_STRING" | sed -n 's/^.*GNSS=\(Choke\).*$/\1/p' | sed "s/%20/ /g"`
ZG2=`echo "$QUERY_STRING" | sed -n 's/^.*GNSS=\(ZG2\).*$/\1/p' | sed "s/%20/ /g"`
Multi=`echo "$QUERY_STRING" | sed -n 's/^.*GNSS=\(Multi\).*$/\1/p' | sed "s/%20/ /g"`
Lab=`echo "$QUERY_STRING" | sed -n 's/^.*GNSS=\(Lab\).*$/\1/p' | sed "s/%20/ /g"`
Lab_Base=`echo "$QUERY_STRING" | sed -n 's/^.*GNSS=\(Lab_Base\).*$/\1/p' | sed "s/%20/ /g"`
xFill=`echo "$QUERY_STRING" | sed -n 's/^.*GNSS=\(xFill\).*$/\1/p' | sed "s/%20/ /g"`
Blade=`echo "$QUERY_STRING" | sed -n 's/^.*GNSS=\(Blade\).*$/\1/p' | sed "s/%20/ /g"`

TESTALL=`echo "$QUERY_STRING" | sed -n 's/^.*GNSS=\(TESTALL\).*$/\1/p' | sed "s/%20/ /g"`
Ag=`echo "$QUERY_STRING" | sed -n 's/^.*GNSS=\(Ag\).*$/\1/p' | sed "s/%20/ /g"`
HCE450=`echo "$QUERY_STRING" | sed -n 's/^.*GNSS=\(HCE450\).*$/\1/p' | sed "s/%20/ /g"`
HCE900=`echo "$QUERY_STRING" | sed -n 's/^.*GNSS=\(HCE900\).*$/\1/p' | sed "s/%20/ /g"`
TEST0=`echo "$QUERY_STRING" | sed -n 's/^.*GNSS=\(TEST0\).*$/\1/p' | sed "s/%20/ /g"`
TEST1=`echo "$QUERY_STRING" | sed -n 's/^.*GNSS=\(TEST1\).*$/\1/p' | sed "s/%20/ /g"`
TEST2=`echo "$QUERY_STRING" | sed -n 's/^.*GNSS=\(TEST2\).*$/\1/p' | sed "s/%20/ /g"`
TEST3=`echo "$QUERY_STRING" | sed -n 's/^.*GNSS=\(TEST3\).*$/\1/p' | sed "s/%20/ /g"`
TEST4=`echo "$QUERY_STRING" | sed -n 's/^.*GNSS=\(TEST4\).*$/\1/p' | sed "s/%20/ /g"`
TEST5=`echo "$QUERY_STRING" | sed -n 's/^.*GNSS=\(TEST5\).*$/\1/p' | sed "s/%20/ /g"`

GRKALL=`echo "$QUERY_STRING" | sed -n 's/^.*GNSS=\(GRKALL\).*$/\1/p' | sed "s/%20/ /g"`
GRK0=`echo "$QUERY_STRING" | sed -n 's/^.*GNSS=\(GRK0\).*$/\1/p' | sed "s/%20/ /g"`
GRK1=`echo "$QUERY_STRING" | sed -n 's/^.*GNSS=\(GRK1\).*$/\1/p' | sed "s/%20/ /g"`
GRK2=`echo "$QUERY_STRING" | sed -n 's/^.*GNSS=\(GRK2\).*$/\1/p' | sed "s/%20/ /g"`
GRK3=`echo "$QUERY_STRING" | sed -n 's/^.*GNSS=\(GRK3\).*$/\1/p' | sed "s/%20/ /g"`
GRK4=`echo "$QUERY_STRING" | sed -n 's/^.*GNSS=\(GRK4\).*$/\1/p' | sed "s/%20/ /g"`

Claude=`echo "$QUERY_STRING" | sed -n 's/^.*GNSS=\(Claude\).*$/\1/p' | sed "s/%20/ /g"`
SNM940=`echo "$QUERY_STRING" | sed -n 's/^.*GNSS=\(SNM940\).*$/\1/p' | sed "s/%20/ /g"`

set -o posix 
#set -x 

cd /var/www/upgrades
WAMEL=/var/firmware/wamel_V$version.timg
GAMEL=/var/firmware/gamel_V$version.timg
ROCKY=/var/firmware/rockhopper_V$version.timg

echo "Version: $version<br/>"
if [ ! -f $WAMEL ]
then
   echo "SPS850/851 Firmware $WAMEL Does not exist<br/>"
fi

if [ ! -f $GAMEL ]
then
   echo "SPS852/855 Firmware $GAMEL Does not exist<br/>"
fi

if [ ! -f $ROCKY ]
then
   echo "SPS985 Firmware $WAMEL Does not exist<br/>"
fi

#set

if [ -n "$Sunnyvale" ] 
then
   echo "Upgrading Sunnyvale<br/>"
   upgrade_with_clone.sh -z -i sps855.com -p admin:jcmsps850 -c 855_COM -f $WAMEL > 855_COM.txt&
   disown
fi 

if [ -n "$Westminster" ] 
then
   echo "Upgrading Westminster<br/>"
   upgrade_with_clone.sh -z -i Base.Trimble-Wco.com -p admin:jcmsps850 -c WCO -f $WAMEL >WCO.txt&
   disown
fi 


if [ -n "$WCOALL$Choke" ]
then
   echo "Upgrading Choke<br/>"
   upgrade_with_clone.sh -z -i Choke.Trimble-Wco.com -p admin:jcmsps850 -c Choke -f $WAMEL >Choke.txt&
   disown
fi

if [ -n "$WCOALL$ZG2" ]
then
   echo "Upgrading ZG2<br/>"
   upgrade_with_clone.sh -z -i ZG2.Trimble-Wco.com -p admin:jcmsps850 -c ZG2 -f $WAMEL >ZG2.txt&
   disown
fi

if [ -n "$WCOALL$Multi" ]
then
   echo "Upgrading Multi<br/>"
   upgrade_with_clone.sh -z -i Multi.Trimble-Wco.com -p admin:jcmsps850 -c Multi -f $WAMEL >Multi.txt&
   disown
fi

if [ -n "$WCOALL$Lab" ]
then
   echo "Upgrading Lab<br/>"
   upgrade_with_clone.sh -z -i Lab.Trimble-Wco.com -p admin:jcmsps850 -c Lab -f $WAMEL >Lab.txt&
   disown
fi

if [ -n "$WCOALL$Lab_Base" ]
then
   echo "Upgrading Lab Base<br/>"
   upgrade_with_clone.sh -z -i Lab-Base.Trimble-Wco.com -p admin:jcmsps850 -c LabBase -f $WAMEL >Lab_Base.txt&
   disown
fi

if [ -n "$WCOALL$xFill" ]
then
   echo "Upgrading xFill<br/>"
   upgrade_with_clone.sh -z -i xFill.Trimble-Wco.com -p admin:jcmsps850 -c xFill -f $ROCKY >xFill.txt&
   disown
fi

if [ -n "$WCOALL$Blade" ]
then
   echo "Upgrading Blade<br/>"
   upgrade_with_clone.sh -z -i Blade.Trimble-Wco.com -p admin:jcmsps850 -c Blade -f $GAMEL >Blade.txt&
   disown
fi


if [ -n "$TESTALL$Ag" ]
then
   echo "Upgrading AG<br/>"
   upgrade_with_clone.sh -z -i site.co-test-site.com:2100 -p admin:testsite -c Ag -f $WAMEL >Ag.txt&
   disown
fi

if [ -n "$TESTALL$HCE450" ]
then
   echo "Upgrading HCC450<br/>"
   upgrade_with_clone.sh -z -i site.co-test-site.com:2106 -p admin:testsite -c HCE450 -f $GAMEL >HCE450.txt&
   disown
fi

if [ -n "$TESTALL$HCE900" ]
then
   echo "Upgrading HCE900<br/>"
   upgrade_with_clone.sh -z -i site.co-test-site.com:2105 -p admin:testsite -c HCE900 -f $WAMEL >HCE900.txt&
   disown
fi

if [ -n "$TESTALL$TEST0" ]
then
   echo "Upgrading TEST0<br/>"
   upgrade_with_clone.sh -z -i site.co-test-site.com:28000 -p admin:testsite -c TEST0 -f $WAMEL >TEST0.txt&
   disown
fi

if [ -n "$TESTALL$TEST1" ]
then
   echo "Upgrading TEST1<br/>"
   upgrade_with_clone.sh -z -i site.co-test-site.com:28001 -p admin:testsite -c TEST1 -f $WAMEL >TEST1.txt&
   disown
fi

if [ -n "$TESTALL$TEST2" ]
then
   echo "Upgrading TEST2<br/>"
   upgrade_with_clone.sh -z -i site.co-test-site.com:28002 -p admin:testsite -c TEST2 -f $GAMEL >TEST2.txt&
   disown
fi

if [ -n "$TESTALL$TEST3" ]
then
   echo "Upgrading TEST3<br/>"
   upgrade_with_clone.sh -z -i site.co-test-site.com:28003 -p admin:testsite -c TEST3 -f $WAMEL >TEST3.txt&
   disown
fi

if [ -n "$TESTALL$TEST4" ]
then
   echo "Upgrading TEST4<br/>"
   upgrade_with_clone.sh -z -i site.co-test-site.com:28004 -p admin:testsite -c TEST4 -f $WAMEL >TEST4.txt&
   disown
fi

if [ -n "$TESTALL$TEST5" ]
then
   echo "Upgrading TEST5<br/>"
   upgrade_with_clone.sh -z -i site.co-test-site.com:28005 -p admin:testsite -c TEST5 -f $WAMEL >TEST5.txt&
   disown
fi


if [ -n "$GRKALL$RAINBASE" ]
then
   echo "Upgrading Rain<br/>"
   upgrade_with_clone.sh -z -i kirk.dyndns.info:2100 -p admin:jcmsps850 -c RAIN -f $WAMEL >Rain.txt&
   disown
fi

if [ -n "$GRKALL$GRK1" ]
then
   echo "Upgrading GRK1<br/>"
   upgrade_with_clone.sh -z -i kirk.dyndns.info:28000 -p admin:jcmsps850 -c GRK1 -f $WAMEL >GRK1.txt&
   disown
fi

if [ -n "$GRKALL$GRK2" ]
then
   echo "Upgrading GRK2<br/>"
   upgrade_with_clone.sh -z -i kirk.dyndns.info:28005 -p admin:jcmsps850 -c GRK2 -f $WAMEL >GRK2.txt&
   disown
fi

if [ -n "$GRKALL$GRK3" ]
then
   echo "Upgrading GRK3<br/>"
   upgrade_with_clone.sh -z -i kirk.dyndns.info:28010 -p admin:jcmsps850 -c GRK3 -f $WAMEL >GRK3.txt&
   disown
fi

if [ -n "$GRKALL$GRK4" ]
then
   echo "Upgrading GRK4<br/>"
   upgrade_with_clone.sh -z -i kirk.dyndns.info:28020 -p admin:jcmsps850 -c GRK4 -f $GAMEL >GRK4.txt&
   disown
fi

if [ -n "$Claude" ]
then
   echo "Upgrading Claude<br/>"
   upgrade_with_clone.sh -z -i claude.dyndns.info -p admin:jcmsps850 -c Claude -f $GAMEL >Claude.txt&
   disown
fi

if [ -n "$SNM940" ]
then
   echo "Upgrading SNM940<br/>"
   upgrade_with_clone.sh -z -i SNM940.com:81 -p admin:testsite -c SNM940 -f $WAMEL >SNM940.txt&
   disown
fi


echo "See <a href=\"/upgrades?C=M;O=D\">upgrades</a> for downloaded clone files and results of upgrading<p/>"

#printenv