#!/usr/bin/perl
use strict;
use constant VERSION => "0.1.0";
use constant URL => "http://jcmbsoft.dyndns.info";
use constant BLURB => "Tools montitoring Trimble SPS receivers, will with any modern high precision GNSS receiver with web interface with\
 the programatic interface enabled";
use constant EXTRA => "Extra";
#use WWW::Mechanize;
use File::Basename;
use Data::Dumper;
#use XML::Simple;
use Getopt::Long;
use LWP::Simple;

sub help() {
    print STDERR "SPS_Dashboard_Antenna.pl -host <host> [-password <password>] [-port <port>] [-APC|-ARP] [-height <height>] [-type <ant_number>] -User [User_ID] -GNSS [GNSS_ID] \n";
    print STDERR "\n";
    print STDERR "If password is not provided, password is used\n";
    print STDERR "If port is not provided, 80 is used\n";
    print STDERR "ARP|APC are optional, if provided the measurement method will be checked to be this\n";
    print STDERR "Height is optional, if provided the antenna height will be checked to be this\n";
    print STDERR "Type is optional, if provided the antenna number will be checked to be this\n";
    exit(100);
    }



my $host = '';# option variable with default value (false)
my $static="";
my $roving="";
my $port="80";
my $password="password";

my $ant_type="";
my $ant_height=-1;
my $ant_method_APC="";
my $ant_method_ARP="";
my $ant_method="";
my $ant_method_short="";
my $user="";
my $gnss="";

GetOptions ('host=s' => \$host,"port=s"=>\$port,"password=s"=>\$password,"type=s"=>\$ant_type,"height=f"=>\$ant_height,"ARP"=>\$ant_method_ARP,"APC"=>\$ant_method_APC,"user=s"=>\$user,"GNSS=s"=>\$gnss);

if ($ant_method_ARP) {
   $ant_method="BottomOfAntennaMount";
   $ant_method_short="ARP";
   }

if ($ant_method_APC) {
   if ($ant_method) {
      die ("Can not have APC and ARP for the same antenna");
      }
   $ant_method="APC";
   $ant_method_short="APC";
   }

#print "Host: $host";
if (!$host) {help();}
if ($host =="1") {help();}

my $URI="http://".$host.":".$port."/prog/show?antenna";
#my $xs = XML::Simple->new();

# define user agent
my $ua = LWP::UserAgent->new();
# make request
my $request = HTTP::Request->new(GET => $URI);
# And before you go making any requests:
$ua->env_proxy;

# authenticate
$request->authorization_basic("admin", $password);

# except response
my $response = $ua->request($request);
die("Incorrect password") if $response->code == 401;

# get content of response
my $content = $response->content();
if ($content =~ /Antenna type=(.*) name=\"(.*)\" height=(.*) measMethod=(.*) serial="(.*)"/ ) {
   my $current_ant_type=$1;
   my $current_ant_name=$2;
   my $current_ant_height=$3;
   my $current_method=$4;
   my $current_correct=1;
   my $fix_command="";

   if ($ant_type) {
      if ($ant_type != $current_ant_type ) {
         $current_correct=0;
         if ($fix_command) {
            $fix_command.="type=".$ant_type;
            }
         else {
            $fix_command="type=".$ant_type;
            }
         }
      }

   if (($ant_height != -1) && ($ant_height != $current_ant_height)) {
         $current_correct=0;
         if ($fix_command) {
            $fix_command.="%26height=".$ant_height;
            }
         else {
            $fix_command="height=".$ant_height;
            }
         }

   if ($current_method != $ant_method) {
         $current_correct=0;
         if ($fix_command) {
            $fix_command.="%26measMethod=".$ant_method;
            }
         else {
            $fix_command="measMethod=".$ant_method;
            }
         }

    if ($current_correct) {
       print $current_ant_name." ".$current_ant_height."m ".$ant_method_short
       }
    else  {
       print '<a href="/cgi-bin/Dashboard/Do_GNSS_Prog?U='.$user.'&G='.$gnss.'&C=antenna&P=' . $fix_command . '">' .$current_ant_name." ".$current_ant_height."m ".$ant_method."</a>"
       }

   }
