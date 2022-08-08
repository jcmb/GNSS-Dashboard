# GNSS-Dashboard
## GNSS Dashboard and upgrade system

The GNSS-Dashboard system is desgined for users who have a large number of Trimble GNSS receivers that you
want to make sure that the settings are configured correctly and will get an alert if they are not configured correctly.

The system uses Nagios to schedule the checks and the reporting of prolbems.

Also inclused is a system for upgrading firmware for the receivers.

Installation

  Clearly need a nice installer, today just copy the www folder into a folder in a location in your web server pages location.
  cgi goes to the Dashboard subfolder in the cgi-bin folder for that site.

  Make the folder /usr/Firmware. Change the owner to be www-data

sqlite3 and the php version of it needs to be installed

apt-get install sqlite3 php-sqlite3

make sure that php is enabled for the web server

create the database

cgi-bin/Dashboard/DB_Setup.php from the command line

change the owner of all of the files
sudo chown www-data *
sudo chgrp nagios GNSS.db
sudo chmod g+w GNSS.db

change the rights on the files

sudo chgrp nagios db.inc.*
sudo chmod g+x  db.inc.*
sudo chgrp nagios Dashboard/
sudo chmod g+w Dashboard/

Change to the cgi-bin/Dashboard directory.
make everything 
 chmod +x *.php *.sh *.pl *.py

You probably have to change the ownership of the cc directory as well.

You need to create /usr/lib/cgi-bin/Dashboard/User directory.
change the owner of all of the User folder. This will be used by Nagios

To be able to support the loading of firmware the default PHP settings need to be changed to allow a post_max_size of 20m

/etc/php/7.0/apache2/php.ini
upload_max_filesize = 25M
post_max_size = 100M
