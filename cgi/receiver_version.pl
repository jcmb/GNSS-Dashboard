#! /usr/bin/perl -w
use strict;
use warnings;

use XML::Simple;
use Data::Dumper;

#print $ARGV[0];
my $Recv_Ver = XMLin($ARGV[0]);

print  $Recv_Ver -> { sysData } -> { mDnsName } if defined  $Recv_Ver -> { sysData } -> { mDnsName };
print  " (".$Recv_Ver -> { sysData } -> { ownerString1 }.") ";
print ": ";
print  $Recv_Ver -> { sysData } -> { RXName };
print ": ";
print  $Recv_Ver -> { sysData } -> { FWVersion };
print "\n";
