#!/usr/bin/perl
use strict;
use Data::Dumper;
use Getopt::Long;
use LWP::Simple;

sub help() {
    print STDERR "SPS_Dashboard_Temp.pl -host <host> [-password <password>] [-port <port>]\n";
    print STDERR "\n";
    print STDERR "If password is not provided, password is used\n";
    print STDERR "If port is not provided, 80 is used\n";
    exit(100);
    }



my $host = '';# option variable with default value (false)                                                    
my $port="80";
my $password="password";

GetOptions ('host=s' => \$host,"port=s"=>\$port,"password=s"=>\$password);

#print "Host: $host";        
if (!$host) {help();}
if ($host eq 1) {help();}


my $URI="http://".$host.":".$port."/prog/show?temperature";

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

if ($content =~ /Temperature temp=(.*)/) {
   print "$1"
   }
