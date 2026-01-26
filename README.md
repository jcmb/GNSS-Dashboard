# GNSS-Dashboard
## GNSS Dashboard and upgrade system

The GNSS-Dashboard system is desgined for users who have a large number of Trimble GNSS receivers that you
want to make sure that the settings are configured correctly and will get an alert if they are not configured correctly.

The system uses Nagios to schedule the checks and the reporting of prolbems.

Also inclused is a system for upgrading firmware for the receivers.

Installation

sqlite3 and the php version of it needs to be installed

    apt-get install sqlite3 php-sqlite3

python 3 needs to be installed, currently with the legacy-cgi module

    apt-get install python3-legacy-cgi


make sure that php is enabled for the web server.

For apache

    apt install php libapache2-mod-php

run the setup script as root
    sudo setup.sh

  cgi goes to the Dashboard subfolder in the cgi-bin folder for that site.
  www goes to the Dashboard subfolder in the www folder for that site.


Note that if the cgi files are not installed in /usr/lib/cgi-bin/ you have to edit the db.inc files


To be able to support the loading of firmware the default PHP settings need to be changed to allow a post_max_size of 20m

    sudo nano /etc/php/7.4/apache2/php.ini
    upload_max_filesize = 30M
    post_max_size = 150M

** Backup
The Backup options need to be added into CRON

    0 0 * * *       www-data /usr/lib/cgi-bin/Dashboard/Backup_GNSS_DB.sh
    1 0 * * *       www-data /usr/lib/cgi-bin/Dashboard/Backup_GNSS.py


You need to change the to email in Backup_GNSS_DB.sh

The backup using PI Programatic_Backup.py. https://github.com/jcmb/Programmatic needs to be in te cgi/Dashboard directory

** Nagios

Install nagios and nagios-plugin's as normal

The nagios config file is normally located in
    /usr/local/nagios/etc

Add the following line to the nagios.cfg file
    cfg_dir=/usr/lib/cgi-bin/Dashboard/User
