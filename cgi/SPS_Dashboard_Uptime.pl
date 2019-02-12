#! /usr/bin/perl
# nagios: -epn

use strict;

use WWW::Mechanize;
use File::Basename;
use Data::Dumper;
use XML::Simple;
use Getopt::Long;

my $xs = XML::Simple->new();

my $host = '';# option variable with default value (false)
my $port="80";
my $password="password";

my $host = '';# option variable with default value (false)
GetOptions ('host=s' => \$host,"port=s"=>\$port,"password=s"=>\$password);
#print "Host: $host";
die ("ERROR: You must provide a host name parameter") unless $host;
die ("ERROR: You must provide a host name") if $host =="1";



my $np = WWW::Mechanize->new();
$np->env_proxy();

$np->timeout(10);

if (open (PROXY, 'proxy.perl')) {

   if (my $proxy = <PROXY>) {
      chomp($proxy);
      $np->proxy(['http', 'ftp'], $proxy);
      }
   close PROXY;
}


$np->get("http://admin:".$password."@".$host.":".$port."/xml/dynamic/powerData.xml");
my $ref = $xs->XMLin($np->content);
#  print Dumper($ref);
my $hours = $ref->{'uptime'}->{'hour'} + $ref->{'uptime'}->{'day'}*24;
#   print Dumper($battery_active);
#   print $battery_active;
print "$hours";
