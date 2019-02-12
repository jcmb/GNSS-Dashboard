#! /bin/bash

Dir=`dirname $0`;
pushd . &>/dev/null
normalDir=`cd "${Dir}";pwd`
PATH=${normalDir}:$PATH
#echo $PATH                                                                                                                                                         
set -o posix 
#set -x 
mkdir /var/www/clones/`date  "+%Y-%m-%d"`
cd /var/www/clones/`date  "+%Y-%m-%d"`

   echo "Backing-Up Sunnyvale"
   upgrade_with_clone.sh -z -i sunnyvale.sps855.com -p admin:jcmsps850 -c 855_COM -n > 855_COM.txt&
   disown

   echo "Backing-up Westminster"
   upgrade_with_clone.sh -z -i Base.Trimble-Wco.com -p admin:jcmsps850 -c WCO -n >WCO.txt&
   disown

   echo "Backing Up Choke"
   upgrade_with_clone.sh -z -i Choke.Trimble-Wco.com -p admin:jcmsps850 -c CHOKE -n >Choke.txt&
   disown

   echo "Backing Up ZG2"
   upgrade_with_clone.sh -z -i ZG2.Trimble-Wco.com -p admin:jcmsps850 -c ZG2 -n >ZG2.txt&
   disown

   echo "Backing Up Multi"
   upgrade_with_clone.sh -z -i Multi.Trimble-Wco.com -p admin:jcmsps850 -c MULTI -n >Multi.txt&
   disown

   echo "Backing Up Lab"
   upgrade_with_clone.sh -z -i Lab.Trimble-Wco.com -p admin:jcmsps850 -c LAB -n >Lab.txt&
   disown

   echo "Backing Up Lab Base"
   upgrade_with_clone.sh -z -i Lab-Base.Trimble-Wco.com -p admin:password -c LABBASE -n >Lab_Base.txt&
   disown

#   echo "Backing Up xFill"
#   upgrade_with_clone.sh -z -i xFill.Trimble-Wco.com -p admin:jcmsps850 -c XFILL -n >xFill.txt&
#   disown

#   echo "Backing Up Blade"
#   upgrade_with_clone.sh -z -i Blade.Trimble-Wco.com -p admin:jcmsps850 -c BLADE -n >Blade.txt&
#   disown

#   echo "Backing Up AG"
#   upgrade_with_clone.sh -z -i site.co-test-site.com:2100 -p admin:testsite -c AG -n >Ag.txt&
#   disown

   echo "Backing Up HCC450"
   upgrade_with_clone.sh -z -i site.co-test-site.com:2106 -p admin:testsite -c HCE450 -n >HCE450.txt&
   disown

   echo "Backing Up HCE900"
   upgrade_with_clone.sh -z -i site.co-test-site.com:2105 -p admin:testsite -c HCE900 -n >HCE900.txt&
   disown

   echo "Backing Up TEST0"
   upgrade_with_clone.sh -z -i site.co-test-site.com:28000 -p admin:testsite -c TEST0 -n >TEST0.txt&
   disown

   echo "Backing Up TEST1"
   upgrade_with_clone.sh -z -i site.co-test-site.com:28001 -p admin:testsite -c TEST1 -n >TEST1.txt&
   disown

   echo "Backing Up TEST2"
   upgrade_with_clone.sh -z -i site.co-test-site.com:28002 -p admin:testsite -c TEST2 -n >TEST2.txt&
   disown

   echo "Backing Up TEST3"
   upgrade_with_clone.sh -z -i site.co-test-site.com:28003 -p admin:testsite -c TEST3 -n >TEST3.txt&
   disown

   echo "Backing Up TEST4"
   upgrade_with_clone.sh -z -i site.co-test-site.com:28004 -p admin:testsite -c TEST4 -n >TEST4.txt&
   disown

   echo "Backing Up TEST5"
   upgrade_with_clone.sh -z -i site.co-test-site.com:28005 -p admin:testsite -c TEST5 -n >TEST5.txt&
   disown

   echo "Backing Up TEST6"
   upgrade_with_clone.sh -z -i site.co-test-site.com:28006 -p admin:testsite -c TEST6 -n >TEST7.txt&
   disown

   echo "Backing Up TEST7"
   upgrade_with_clone.sh -z -i site.co-test-site.com:28007 -p admin:testsite -c TEST7 -n >TEST7.txt&
   disown

   echo "Backing Up TEST8"
   upgrade_with_clone.sh -z -i site.co-test-site.com:28008 -p admin:testsite -c TEST8 -n >TEST8.txt&
   disown

   echo "Backing Up TEST9"
   upgrade_with_clone.sh -z -i site.co-test-site.com:28009 -p admin:testsite -c TEST9 -n >TEST9.txt&
   disown

   echo "Backing Up TEST10"
   upgrade_with_clone.sh -z -i site.co-test-site.com:28010 -p admin:testsite -c TEST10 -n >TEST10.txt&
   disown

   echo "Backing Up TEST11"
   upgrade_with_clone.sh -z -i site.co-test-site.com:28011 -p admin:testsite -c TEST11 -n >TEST11.txt&
   disown

   echo "Backing Up TEST12"
   upgrade_with_clone.sh -z -i site.co-test-site.com:28012 -p admin:testsite -c TEST12 -n >TEST12.txt&
   disown

   echo "Backing Up TEST13"
   upgrade_with_clone.sh -z -i site.co-test-site.com:28013 -p admin:testsite -c TEST13 -n >TEST13.txt&
   disown

   echo "Backing Up TEST5"
   upgrade_with_clone.sh -z -i site.co-test-site.com:28005 -p admin:testsite -c TEST5 -n >TEST5.txt&
   disown

   echo "Backing Up GRK_940"
   upgrade_with_clone.sh -z -i kirk.dyndns.info:8081 -p admin:jcmsps850 -c GRK_940 -n >GRK_940.txt&
   disown

   echo "Backing Up GRK1"
   upgrade_with_clone.sh -z -i kirk.dyndns.info:81 -p admin:jcmsps850 -c GRK1 -n >GRK1.txt&
   disown

   echo "Backing Up GRK2"
   upgrade_with_clone.sh -z -i kirk.dyndns.info:82 -p admin:jcmsps850 -c GRK2 -n >GRK2.txt&
   disown

   echo "Backing Up GRK3"
   upgrade_with_clone.sh -z -i kirk.dyndns.info:83 -p admin:jcmsps850 -c GRK3 -n >GRK3.txt&
   disown

   echo "Backing Up GRK4"
   upgrade_with_clone.sh -z -i kirk.dyndns.info:84 -p admin:jcmsps850 -c GRK4 -n >GRK4.txt&
   disown

   echo "Backing Up Claude"
   upgrade_with_clone.sh -z -i claude.dyndns.info -p admin:password -c CLAUDE -n >Claude.txt&
   disown

   echo "Backing Up SNM940"
   upgrade_with_clone.sh -z -i SNM940.com:81 -p admin:testsite -c SNM940 -n >SNM940.txt&
   disown

#printenv
