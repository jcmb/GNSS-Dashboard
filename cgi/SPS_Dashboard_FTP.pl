#! /usr/bin/perl
# nagios: -epn

use strict;

#use WWW::Mechanize;
use File::Basename;
use Data::Dumper;
use XML::Simple;
use Getopt::Long;
use LWP::Simple;

sub help() {
    print STDERR "SPS_Dashboard_FTP.pl -host <host> [-password <password>] [-port <port>] [-yes|-no] [-dir <to>]\n";
    print STDERR "\n";
    print STDERR "If password is not provided, password is used\n";
    print STDERR "If port is not provided, 80 is used\n";
    print STDERR "";
    print STDERR "yes|no are optional, if provided the value will be checked to be this.\n";
    print STDERR "if yes then data logging must be active\n";
    print STDERR "dir is optional, if provided the value will be checked to be this, only valid when checking for yes.\n";
    print STDERR "  diretories default to the prefix of /pub/to_tac/gkirk/";
    exit(100);
    }

use constant VERSION => "0.1.0";
use constant URL => "http://jcmbsoft.dyndns.info";
use constant EXTRA => "Extra";

my $xs = XML::Simple->new();

my $host = '';# option variable with default value (false)
my $port="80";
my $password="password";
my $expected_dir="";
my $On="";
my $Off="";

GetOptions ('host=s' => \$host,"port=s"=>\$port,"password=s"=>\$password,"yes"=>\$On,"no"=>\$Off,"dir=s"=>\$expected_dir);

#print "Host: $host";
if (!$host) {help();}
if ($host =="1") {help();}

my $ftp="";
if ($On) {
   $ftp=1;
   }

if ($Off) {
   if ($ftp) {
      die ("Can not have ftp yes and no at the same time");
      }
   $ftp=0;
   }


if (index($expected_dir,"/pub/to_tac/gkirk/") != -1)
    {
    $expected_dir=substr($expected_dir, length("/pub/to_tac/gkirk/"));
    } # End remove /pub/to_tac/gkirk/

# define user agent
my $ua = LWP::UserAgent->new();
# make request

my $URI="http://".$host.":".$port."/xml/dynamic/dataLogger.xml";
my $request = HTTP::Request->new(GET => $URI);
# And before you go making any requests:
$ua->env_proxy;

# authenticate
$request->authorization_basic("admin", $password);
# except response
my $response = $ua->request($request);
#print Dumper($response);
# get content of response
die("Incorrect password") if $response->code == 401;

my $content = $response->content();
#print $content;
#print $host, $port, $password;
my $ref = $xs->XMLin($content);
#  print Dumper($ref);

my $logging_active = $ref->{'session'}->{'enabled'};
my $ftppush_active = $ref->{'ftpPushEnabled'};
#print Dumper($logging_active);
#print Dumper($ftppush_active);

$URI="http://".$host.":".$port."/xml/dynamic/ftpPush.xml";
$request = HTTP::Request->new(GET => $URI);
$request->authorization_basic("admin", $password);
# except response
$response = $ua->request($request);
#print Dumper($response);
# get content of response
die("Incorrect password") if $response->code == 401;

$content = $response->content();

$ref = $xs->XMLin($content);


my $dir = $ref->{'server'}->{'dir'};

#print Dumper($content);
#print Dumper($dir);
#print ref ($dir);


if (!(defined($logging_active) && ($logging_active eq '1'))) {
    if ($ftp == 1) {
        print "<strong>Logging Disabled</strong>";
        }
    else {
        print "Logging Disabled";
        }
    }
else
   {
   if (!(defined($ftppush_active) && ($ftppush_active eq '1'))) {
      if ($ftp != 1) {
         print "ftppush Disabled";
         }
      else {
         print "<strong>ftppush Disabled</strong>";
         }
      }
   else {
      if (ref($dir)) {
         print "<strong>blank dir</strong>";
         }
      else
         {
         if (index($dir,"/pub/to_tac/gkirk/") != -1)
            {
            $dir=substr($dir, length("/pub/to_tac/gkirk/"));
            } # End remove /pub/to_tac/gkirk/
         if ($expected_dir eq "") {
            if ($ftp == 0)
               {
               print $dir
               }
            else
               {
               print "<strong>".$dir."</strong>"
               }
            }
         else
            {
            if (uc($expected_dir) eq uc($dir)) {
               print $dir
               }
            else {
               print "<strong>".$dir."</strong>"
               }
            } # End Else expected_dir blank
         }
      }
   }
#      print "failed";
#  print "Battery";
#}
#else {
#      print "worked";
#  print "AC"
#
