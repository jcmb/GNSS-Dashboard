#!/usr/bin/perl -w
use strict;
#use WWW::Mechanize;
use Data::Dumper;
use Getopt::Long;
use LWP::Simple;

sub help() {
    print STDERR "SPS_Dashboard_Clock.pl -host <host> [-password <password>] [-port <port>] [-Elev <Elev>]\n";
    print STDERR "\n";
    print STDERR "If password is not provided, password is used\n";
    print STDERR "If port is not provided, 80 is used\n";
    print STDERR "Elevation is optional, if provided the value will be checked to be this\n";
    exit(100);
    }



my $host = '';# option variable with default value (false)
my $elev=undef;
my $port="80";
my $password="password";
my $user="";
my $gnss="";

GetOptions ('host=s' => \$host,"port=s"=>\$port,"password=s"=>\$password,"elev=i"=>\$elev,"user=s"=>\$user,"GNSS=s"=>\$gnss);

#print "Host: $host";
if (!$host) {help();}
if ($host eq "1") {help();}


my $URI="http://".$host.":".$port."/prog/show?elevationMask";
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

if ($content =~ /ElevationMask mask=(.*)/) {
   if (defined $elev) {
      if ($elev==$1) {
         print "$1"
         }
      else {
         print '<a href="/cgi-bin/Dashboard/Do_GNSS_Prog?U='.$user.'&G='.$gnss.'&C=ElevationMask&P=mask='.$elev.'">'.$1."</a>";
         }
      }
   else {
      print "$1"
      }
   }

