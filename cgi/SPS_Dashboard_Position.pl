#!/usr/bin/perl -w
use strict;
use Data::Dumper;
use Getopt::Long;
use LWP::Simple;

sub help() {
    print STDERR "SPS_Dashboard_Position.pl -host <host> [-password <password>] [-port <port>] [-position <type>]\n";
    print STDERR "\n";
    print STDERR "If password is not provided, password is used\n";
    print STDERR "If port is not provided, 80 is used\n";
    print STDERR "Position is optional, if provided the value will be checked to be this\n";
    exit(100);
    }



my $host = '';# option variable with default value (false)                                                    
my $position=undef;
my $port="80";
my $password="password";

GetOptions ('host=s' => \$host,"port=s"=>\$port,"password=s"=>\$password,"position=s"=>\$position);

#print "Host: $host";        
if (!$host) {help();}
if ($host eq 1) {help();}


my $URI="http://".$host.":".$port."/prog/show?position";

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

for my $line ($content) {
   if ($line =~ /Qualifiers *(.*)/) {
      if (defined $position) {
#         print index($1,$position);
         if (index($1,$position) == -1) {
            print "<strong>$1</strong>"
            }
         else {                     
            print "$1"
            }
         }
      }
   }
