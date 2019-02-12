#!/usr/bin/perl -w
use strict;
use Data::Dumper;
use Getopt::Long;
use LWP::Simple;

sub help() {
    print STDERR "SPS_Dashboard_Serial.pl -host <host> [-password <password>] [-port <port>] [-pdop <pdop>]\n";
    print STDERR "\n";
    print STDERR "If password is not provided, password is used\n";
    print STDERR "If port is not provided, 80 is used\n";
    print STDERR "PDOP is optional, if provided the value will be checked to be this\n";
    exit(100);
    }



my $host = '';# option variable with default value (false)                                                    
my $pdop=undef;
my $port="80";
my $password="password";

GetOptions ('host=s' => \$host,"port=s"=>\$port,"password=s"=>\$password,"pdop=f"=>\$pdop);

#print "Host: $host";        
if (!$host) {help();}
if ($host eq 1) {help();}


my $URI="http://".$host.":".$port."/prog/show?SerialNumber";

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

my $content = $response->content();

if ($content =~ /SerialNumber/) {
    if ($content =~ /SerialNumber sn=(.*) *rxType=(.*)/) {
       print "$1"
       }
    else {
       if ($content =~ /SerialNumber sn=(.*)/) {
	       print "$1"
          }
       }
    }
   

