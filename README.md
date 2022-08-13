# GNSS-Dashboard
## GNSS Dashboard and upgrade system

The GNSS-Dashboard system is desgined for users who have a large number of Trimble GNSS receivers that you
want to make sure that the settings are configured correctly and will get an alert if they are not configured correctly.

The system uses Nagios to schedule the checks and the reporting of prolbems.

Also inclused is a system for upgrading firmware for the receivers.

Installation

  Clearly need a nice installer, today just copy the www folder into a folder in a Dashboard directory in your web server pages root.
  cgi goes to the Dashboard subfolder in the cgi-bin folder for that site.

  Make the folder /usr/Firmware. Change the owner to be www-data

sqlite3 and the php version of it needs to be installed

    apt-get install sqlite3 php-sqlite3

python 2 needs to be installed, currently.
    apt-get install python2

make sure that php is enabled for the web server

create the database

    cd /usr/lib/cgi-bin/Dashboard
    sudo php ./DB_Setup.php


change the owner of all of the files
    sudo chown www-data /usr/lib/cgi-bin/Dashboard
    cd /usr/lib/cgi-bin/Dashboard/
    sudo chown www-data *
    sudo chgrp www-data GNSS.db
    sudo chmod g+w GNSS.db
    sudo chgrp www-data db.inc.*
    sudo chmod g+x  db.inc.*
    sudo chmod +x *.php *.sh *.pl *.py

Note that if the cgi files are not installed in /usr/lib/cgi-bin/ you have to edit the db.inc files

change the rights on the HTML files.

    cd /var/www/
    sudo chgrp www-data Dashboard/
    sudo chmod g+w Dashboard/


You need to create /usr/lib/cgi-bin/Dashboard/User directory. This will be used by Nagios

    sudo mkdir /usr/lib/cgi-bin/Dashboard/User
    sudo chown www-data /usr/lib/cgi-bin/Dashboard/User


To be able to support the loading of firmware the default PHP settings need to be changed to allow a post_max_size of 20m

    sudo nano /etc/php/7.4/apache2/php.ini
    upload_max_filesize = 25M
    post_max_size = 100M
