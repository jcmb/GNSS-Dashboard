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
    print STDERR "SPS_Dashboard_Motion.pl -host <host> -User [User_ID] -GNSS [GNSS_ID] [-password <password>] [-port <port>] [-static|-roving]\n";
    print STDERR "\n";
    print STDERR "If password is not provided, password is used\n";
    print STDERR "If port is not provided, 80 is used\n";
    print STDERR "static|roving are optional, if provided the value will be checked to be this\n";
    exit(100);
    }



my $host = '';# option variable with default value (false)
my $static="";
my $roving="";
my $port="80";
my $password="password";
my $user="";
my $gnss="";

GetOptions ('host=s' => \$host,"port=s"=>\$port,"password=s"=>\$password,"static"=>\$static,"roving"=>\$roving,"user=s"=>\$user,"GNSS=s"=>\$gnss);

#print "Host: $host";
if (!$host) {help();}
if ($host eq "1") {help();}

my $URI="http://".$host.":".$port."/prog/show?rtkControls";
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
#print $content;

#print $host, $port, $password;

if ($content =~ /RtkControls mode=(.*) motion=(.*)/) {
   my $motion=$2;

   if ($static) {
      if ($motion eq "static"){
         print $motion;
         }
      else {
         print '<a href="/cgi-bin/Dashboard/Do_GNSS_Prog?U='.$user."&G=".$gnss.'?rtkControls&motion=static">'.$motion."</a>";
         }
      }
    elsif ($roving)
       {
       if ($motion eq "kinematic"){
           print $motion;
          }
       else {
          print '<a href="/cgi-bin/Dashboard/Do_GNSS_Prog?U='.$user."&G=".$gnss.'&C=rtkControls&P=motion=kinematic">'.$motion."</a>";
#          print '<a href="http://'.$host.":".$port.'/prog/set?rtkControls&motion=kinematic">'.$motion."</a>";
          }
       }
    else {
       print $motion
       }
   }

#my $s="";
#
#while ($content) {
#    chomp;
#    $s=$_;
#    }
#
#}


=begin comment
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

=end comment
