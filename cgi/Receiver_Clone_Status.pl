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
my $name=$ARGV[2];
my $verbose=$ARGV[3];

if ( !defined $receiver ) {
    print "Usage: Receiver_Clone_Status receiver_IP User_Pass [Display Name] [Verbose]\n";
    exit;
   }

if ( !defined $name){
   $name=$receiver
}

if ( !defined $verbose) {
    $verbose=0
}

printf "Monitoring Clone File Creation status for $name\n";
my $browser = WWW::Mechanize->new(autocheck => 1);
$browser->env_proxy();

if ($ARGV[1]) {
   $browser->default_header( Authorization => 'Basic ' . encode_base64($ARGV[1]));
#   print "User $ARGV[1]\n"
   }

#$browser->timeout (5);
#$browser->show_progress(1);
my $Clone_Status = "";
my $Working = 1;
my $content = '';
my $Last_State="";
my $State="";
my $Status="";
my $Count=0;
#printf "Monitoring Clone File Creation status for $receiver\n";
while ( $Working ) {
#printf "Monitoring Clone File Creation status for $receiver\n";
#   print "Before Get";
   $browser->get ("http://$receiver/xml/dynamic/cloneFileStatus.xml");
#   print "After Get";
   $Status= $browser->status;
#  print $Status;
   if ($Status == 200) {
       $content = $browser->content();
       $Clone_Status = XMLin($content);
#      print Dumper ($Clone_Status);

       $State=$Clone_Status-> { cloneOperationStatus };
       if ($verbose) {
          print $State;
       }

#      if ($State ne $Last_State) {
#      print "5";
#         print "\n". $State;
#         $Last_State=$State;
#          $Count=0;
#         }
#      else {
           if ($State eq "0") {
              $Working = 0;
          print "Clone File Creation Completed for $receiver\n"
       }
       else {
           if ($Count) {
#           print ".";
               }
           else {
#                   print $State
               }
               $Count++;
           }
    }
    else {
        print "\nGet for $receiver Failed with error code: ";
        print $Status . "\n";
        }
#    print "2";
   sleep(2);
}
print "\n";
