#!/usr/bin/env perl
use strict;
use warnings;

my $v = "0.0.1";
my $man = 'Copyright (c) 2024 Ray Mentose.
Get the latest version on Github at: https://github.com/ryt/runapp.git

Command line helper for gunicorn app processes/daemons.

Instructions:

1. Make this script executable & create a symbolic link to it in the app directory:
- chmod +x runapp.pl
- ln -s ../runapp.pl runapp

2. Configure app settings in runapp.conf file.
- vi runapp.conf
- { appname => hello } etc...

3. Create a "pids" directory:
- mkdir pids

Usage:

./runapp start
./runapp stop
./runapp restart
./runapp reload
./runapp list
./runapp

';


# Specific app settings for gunicorn:

my $config = do("./runapp.conf");

my $appname = $config->{appname}; # e.g. hellopy
my $appcall = $config->{appcall}; # e.g. app:hello
my $appuser = $config->{appuser}; # e.g. ray
my $appgroup = $config->{appgroup}; # e.g. staff
my $workers = $config->{workers}; # 2
my $port = $config->{port}; # 8000
my $run = '';
my $exe = '';
my $cme = '';


# On MacOS (i.e. Darwin) replace long folder names with "...":

my $macos_add = $^O eq 'darwin' ? "--color=always | sed 's/Library.*MacOS/.../g'" : "";

my ($command, $optname) = @ARGV;

if ( not defined $optname ) {
  $optname = $appname;
}

if ( not defined $command ) {
  $command = '';
}


# Main gunicorn and process list commands:

my $cm_start = "gunicorn $appcall -n $appname -p pids/$appname.pid -w $workers -u $appuser -g $appgroup -b :$port -D";
my $cm_stop = "kill -9 `cat pids/$appname.pid` && rm pids/$appname.pid";
my $cm_list = "ps aux | grep '[". substr($appname, 0, 1) . "]" . substr($appname, 1) . "' $macos_add";


# Command line options for this perl script: 
# -> start, stop, restart, reload, list

if ( $command eq 'start' ) {
  $cme = 'start';
  $run = $cm_start;
} elsif ( $command eq 'stop' ) {
  $cme = 'stop';
  $run = $cm_stop;
} elsif ( $command eq 'restart' or $command eq 'reload' ) {
  $cme = 'restart';
  $run = "$cm_stop && $cm_start";
} elsif ( $command eq 'help' or $command eq '--help' or $command eq '-h' or $command eq 'man' ) {
  print $man; exit;
} elsif ( $command eq 'version' or $command eq '--version' or $command eq '-v' ) {
  print "Version $v\n"; exit;
} else {
  $cme = 'list';
  $run = $cm_list;
}


# For start, restart, & reload show the process list after running the app.

if ( $command eq 'start' or $command eq 'restart' or $command eq 'reload' ) {
  $exe = readpipe($run) . readpipe($cm_list);
} else {
  $exe = readpipe($run);
}

print 'Running "' . $cme . '": ' . "\n" . "  " . $run . "\n" . $exe . "\n";
