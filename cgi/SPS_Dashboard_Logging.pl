#!/usr/bin/perl
use strict;
use Data::Dumper;
use Getopt::Long;
use LWP::Simple;

sub help() {
    print STDERR "SPS_Dashboard_Logging.pl -host <host> [-password <password>] [-port <port>] [-yes] [-no] [-cont] [-duration minutes] [-meas rate] [-pos rate] [-smooth_phase yes|no] [-smooth_range yes|no]\n";
    print STDERR "\n";
    print STDERR "If password is not provided, password is used\n";
    print STDERR "If port is not provided, 80 is used\n";
    print STDERR "cont is optional, if provided the value will be checked to be this\n";
    print STDERR "duration, in minutes, is optional, if provided the value will be checked to be this\n";
    print STDERR "meaurement rate, and position rate are in seconds";
    exit(100);
    }



my $host = '';# option variable with default value (false)
my $elev=undef;
my $port="80";
my $password="password";
my $On="";
my $Off="";
my $cont="";
my $duration="";
my $meas="";
my $pos="";
my $smooth_phase="";
my $smooth_range="";
my $user="";
my $gnss="";


GetOptions ('help|?'=> sub{help()},'host=s' => \$host,"port=s"=>\$port,"password=s"=>\$password,,"yes"=>\$On,"no"=>\$Off,"cont"=>\$cont,"duration=i"=>\$duration,"meas|measure=f"=>\$meas,"pos|position=f"=>\$pos,"phase|smooth_phase=s"=>\$smooth_phase,"range|smooth_range=s"=>\$smooth_range,"user=s"=>\$user,"GNSS=s"=>\$gnss);

#print $smooth_phase;
#print "Host: $host";
if (!$host) {help();}
if ($host eq "1") {help();}


my $logging="";

if ($On) {
   $logging="yes";
   }

if ($Off) {
   if ($logging) {
      die ("Can not have logging yes and no at the same time");
      }
   $logging="no";
   }

if ($smooth_phase ne "") {
   if ($smooth_phase ne "yes") {
      if ($smooth_phase ne "no") {
         die ("Smooth phase must be yes or no");
         }
      }
   }

if ($smooth_range ne "") {
   if ($smooth_range ne "yes") {
      if ($smooth_range ne "no") {
         die ("Smooth range must be yes or no");
         }
      }
   }



my $URI="http://".$host.":".$port."/prog/show?sessions";
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
my @lines=split ("\n",$content);
#print Dumper(@lines);
#print $lines[1];
#print $host, $port, $password;

if ($lines[1] =~ /^.*enabled=(.*) schedule=(.*) durationMin=(.*) measInterval=(.*) posInterval=(.*) fileSystem=.* smoothRanges=(.*) smoothPhases=(.*) /)
   {
#   print "match";
   my $current_enabled=$1;
   my $current_schedule=$2;
   my $current_duration=$3;
   my $current_meas=$4;
   my $current_pos=$5;
   my $current_Range=$6;
   my $current_Phase=$7;

   my $current_correct=1;

   my $fix_command="";

   if ($logging ne "") {
#      print "\nlogging check $logging $current_enabled";
      if ($current_enabled ne $logging) {
         $current_correct=0;
#         print "Need to fix\n $fix_command";
         if ($fix_command) {
            $fix_command.="%26enabled=".$logging;
            }
         else {
            $fix_command="enabled=".$logging;
            }
         }
#         print "After fix\n $fix_command";
      }

   if ($cont) {
      if ($current_schedule ne "continuous") {
         $current_correct=0;
         if ($fix_command) {
            $fix_command.="%26schedule=continuous";
            }
         else {
            $fix_command="schedule=continuous";
            }
         }
      }

   if ($duration) {
      if ($current_duration != $duration) {
         $current_correct=0;
         if ($fix_command) {
            $fix_command.="%26durationMin=".$duration;
            }
         else {
            $fix_command="durationMin=".$duration;
            }
         }
      }

   if ($meas) {
      if ($meas != $current_meas) {
         $current_correct=0;
         if ($fix_command) {
            $fix_command.="%26measInterval=".$meas;
            }
         else {
            $fix_command="measInterval=".$meas;
            }
         }
      }

   if ($pos) {
      if ($pos != $current_pos) {
         $current_correct=0;
         if ($fix_command) {
            $fix_command.="%26posInterval=".$pos;
            }
         else {
            $fix_command="posInterval=".$pos;
            }
         }
      }

   if ($smooth_range) {
      if ($current_Range ne $smooth_range) {
         $current_correct=0;
         if ($fix_command) {
            $fix_command.="%26smoothRanges=".$smooth_range;
            }
         else {
            $fix_command="smoothRanges=".$smooth_range;
            }
         }
      }

   if ($smooth_phase) {
#      print "Phase:$current_Phase $smooth_phase\n";
      if ($current_Phase ne $smooth_phase) {
         $current_correct=0;
         if ($fix_command) {
            $fix_command.="%26smoothPhases=".$smooth_phase;
            }
         else {
            $fix_command="smoothPhases=".$smooth_phase;
            }
         }
      }
   if ($current_correct) {
      print $current_schedule.", ".$current_duration."m, ".$current_meas.",".$current_pos."s"
      }
   else
      {
      print '<a href="/cgi-bin/Dashboard/Do_GNSS_Prog?U='.$user.'&G='.$gnss.'&C=session&P=' . $fix_command . '">'.$current_schedule . ", ".$current_duration."m, ".$current_meas.",".$current_pos."s</a>"

      }
   }
else {
   die ("Internal error: Did not match logging details");
   }

