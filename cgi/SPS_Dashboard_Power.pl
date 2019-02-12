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

my $AC="";
my $Battery="";

GetOptions ('hostname=s' => \$host,'ac'=>\$AC,'battery'=>\$Battery,"port=s"=>\$port,"password=s"=>\$password);

#print "Host: $host";
die ("ERROR: You must provide a host name parameter") unless $host;
die ("ERROR: You must provide a host name") if $host eq "1";

die ("ERROR: You can not have battery and AC at the same time") if ($AC && $Battery);


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
my $battery_active = $ref->{'B1'}->{'active'};
#   print Dumper($battery_active);
#   print $battery_active;
if (defined($battery_active) && ($battery_active eq 'TRUE')) {
#      print "failed";
   if ($AC) {
      print "<strong>Battery<strong>";
      }
   else {
      print "Battery";
      }
}
else {
#      print "worked";
   if ($Battery) {
      print "<strong>AC</strong>"
      }
   else {
      print "AC"
      }
}
