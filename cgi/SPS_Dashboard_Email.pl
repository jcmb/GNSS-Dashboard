#! /usr/bin/perl -w
# nagios: -epn

use strict;

#use WWW::Mechanize;
use File::Basename;
use Data::Dumper;
use XML::Simple;
use Getopt::Long;
use LWP::Simple;

sub help() {
    print STDERR "SPS_Dashboard_Email.pl -host <host> [-password <password>] [-port <port>] [-yes|-no] [-email <to>]\n";
    print STDERR "\n";
    print STDERR "If password is not provided, password is used\n";
    print STDERR "If port is not provided, 80 is used\n";
    print STDERR "";
    print STDERR "yes|no are optional, if provided the value will be checked to be this\n";
    print STDERR "email is optional, if provided the value will be checked to be this, only valid when checking for yes\n";
    exit(100);
    }



my $xs = XML::Simple->new();

my $host = '';# option variable with default value (false)
my $port="80";
my $password="password";
my $email_user="";
my $On="";
my $Off="";

GetOptions ('host=s' => \$host,"port=s"=>\$port,"password=s"=>\$password,"yes"=>\$On,"no"=>\$Off,"email=s"=>\$email_user);

#print "Host: $host";
if (!$host) {help();}
if ($host eq "1") {help();}

my $email="";
if ($On) {
   $email=1;
   }

if ($Off) {
   if ($email) {
      die ("Can not have email yes and no at the same time");
      }
   $email=0;
   }

# define user agent
my $ua = LWP::UserAgent->new();
# make request

my $URI="http://admin:".$password."@".$host.":".$port."/xml/dynamic/email.xml";

my $request = HTTP::Request->new(GET => $URI);
# And before you go making any requests:
$ua->env_proxy();

# authenticate
$request->authorization_basic("admin", $password);
# except response
my $response = $ua->request($request);
#print STDERR Dumper($response);
# get content of response
die("Incorrect password") if $response->code == 401;

my $content = $response->content();
#print STDERR $content;

#print $host, $port, $password;


my $ref = $xs->XMLin($content);
#print Dumper($ref);
my $alerts_active = $ref->{'enable'};
my $alerts_to = $ref->{'to'};

if (defined($alerts_active) && ($alerts_active eq '1')) {
#      print "failed";
   if ($email ne "") {
      if ($email) {
         if ($email_user) {
#            print uc($email_user);
#            print uc($alerts_to);
            if (uc($email_user) eq uc($alerts_to)) {
               print $alerts_to;
               }
            else {
               print "<strong>".$alerts_to."</strong>";
               }
            }
         else {
            print $alerts_to;
            }
         }
      else {
         print "<strong>".$alerts_to."</strong>";
         }
      }
   else {
      print $alerts_to;
      }
   }

else {
#      print "worked";
   if ($email ne "") {
      if ($email) {
         print "<strong>Disabled</strong>";
         }
      else {
         print "Disabled"
         }
      }
   else {
      print "Disabled"
      }
}
