#! /usr/bin/perl -w
# $Rev: 11 $
# $Author: artem $
# $Date: 2009-05-23 23:09:47 -0700 (Sat, 23 May 2009) $
$|=1;
use strict;

use WWW::Mechanize;
use XML::Simple;
use Data::Dumper;

use MIME::Base64;

my $receiver=$ARGV[0];

if ( !defined $receiver ) {
    print "Usage: Receiver_Firmware_Status receiver_IP\n";
    exit;
   }


printf "Monitoring firmware upgrade status for $receiver\n";
my $browser = WWW::Mechanize->new(autocheck => 1);
$browser->env_proxy();

if ($ARGV[1]) {
    $browser->default_header( Authorization => 'Basic ' . encode_base64($ARGV[1]));
#   print "User $ARGV[1]\n"
}




#$browser->timeout (5);
#$browser->show_progress(1);
my $FW_Status = "";
my $Working = 1;
my $content = '';
my $Last_State="";
my $State="";
my $Status="";
my $Count=0;
#printf "Monitoring firmware upgrade status for $receiver\n";
while ( $Working ) {
   #printf "Monitoring firmware upgrade status for $receiver\n";
   #print "Before Get";
   $browser->get ("http://$receiver/xml/dynamic/merge.xml?firmware_status=");
   #print "After Get";
   $Status= $browser->status;
   #print $Status;
   if ($Status == 200) {
       $content = $browser->content();
       $FW_Status = XMLin($content);
#      print Dumper ($FW_Status);

       $State=$FW_Status-> { fw_status } -> { status } -> { mode } ;
#      print $State;
       if ($State ne $Last_State) {
#      print "5";
          print "\n". $receiver. "->" .$State;
          $Last_State=$State;
          $Count=0;
          }
       else {
#          print ".";
          $Count++;

          if ($State eq "FIRMWARE_DONE") {
                $Working = 0;
                }

          if ($State eq "FIRMWARE_WRONG_PLATFORM") {
                $Working = 0;
                }

          if ($State eq "FIRMWARE_WARRANTY_EXPIRED") {
                $Working = 0;
                }

          if ($State eq "FIRMWARE_IDLE") {
             if ($Count >= 5) {
                 $Working = 0;
                 }
             }
          }
    }
    else {
        print "\nGet Failed for $receiver with error code: ";
        print $Status . "\n";
        }
#    print "2";
   sleep(2);
}
print "\n". $receiver. "->" .$State;
print "\n";
