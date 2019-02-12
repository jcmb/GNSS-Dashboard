#! /usr/bin/perl -w
# $Rev: 11 $
# $Author: artem $
# $Date: 2009-05-23 23:09:47 -0700 (Sat, 23 May 2009) $
$|=1; 
use strict;

use XML::Simple;
use Data::Dumper;

my $clone_name=$ARGV[0];

if ( !defined $clone_name ) {
    print "Usage: <clone file name>\n";
    exit;
   }

#print "Checking: $clone_name\n";

my $clone = eval { XMLin ($clone_name)};
die "Invalid XML File" if ($@);

#print Dumper( $clone );
die "Invalid Clone File" unless defined ( $clone-> { APP_RECORD });
#$State=$FW_Status-> { fw_status } -> { status } -> { mode } ;
print "\n"; 
