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
    print STDERR "SPS_Dashboard_Clock.pl -host <host> [-password <password>] [-port <port>] [-On|-Off]\n";
    print STDERR "\n";
    print STDERR "If password is not provided, password is used\n";
    print STDERR "If port is not provided, 80 is used\n";
    print STDERR "On|Off are optional, if provided the value will be checked to be this\n";
    exit(100);
    }



my $host = '';# option variable with default value (false)
my $On="";
my $Off="";
my $port="80";
my $password="password";
my $user="";
my $gnss="";


GetOptions ('host=s' => \$host,"port=s"=>\$port,"password=s"=>\$password,"yes"=>\$On,"no"=>\$Off,"user=s"=>\$user,"GNSS=s"=>\$gnss);

#print "Host: $host";
if (!$host) {help();}
if ($host =="1") {help();}

my $clock="";
if ($On) {
   $clock="yes";
   }

if ($Off) {
   if ($clock) {
      die ("Can not have clock steering yes and no at the same time");
      }
   $clock="no";
   }


my $URI="http://".$host.":".$port."/prog/show?clockSteering";
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
#print Dumper($response);
# get content of response
die("Incorrect password") if $response->code == 401;

my $content = $response->content();
#print $content;

#print $host, $port, $password;

if ($content =~ /ClockSteering enable=(.*)/) {
   if ($clock) {
      if ($1 eq $clock) {
         print "$1"
         }
      else {
         print '<a href="/cgi-bin/Dashboard/Do_GNSS_Prog?U='.$user.'&G='.$gnss.'&C=ClockSteering&P=enable='.$clock.'">'.$1."</a>";
         }
      }
   else {
      print "$1"
      }
   }
