#!/bin/bash -x

WWW=/var/www/html/Dashboard
CGI=/usr/lib/cgi-bin/Dashboard
WWW_USER=www-data
NAGIOS_USER=nagios


mkdir -p $WWW || exit Error could not make directory $WWW
chown www-data $WWW
chgrp nagios $WWW
mkdir -p $WWW/Firmware || exit Error could not make directory $WWW/Firmware
mkdir -p $WWW/Clones || exit Error could not make directory $WWW/Clones
mkdir -p $WWW/PI || exit Error could not make directory $WWW/Clones

mkdir -p $CGI || exit Error could not make directory $CGI
mkdir -p $CGI/User || exit Error could not make directory $CGI/User

cp  www/* $WWW
cp  cgi/* $CGI
cp  User/* $CGI/User

cd $CGI
chown $WWW_USER $WWW/*
chown $WWW_USER $CGI/*
chmod +x $CGI/*.py $CGI/Do_* $CGI/View_Error $CGI/Download_* $CGI/Delete_Errors 2>/dev/null || true

if [ ! -f $CGI/secret_key ]; then
    python3 -c "import secrets; print(secrets.token_urlsafe(32))" > $CGI/secret_key
    chmod 600 $CGI/secret_key
    chown $WWW_USER $CGI/secret_key
fi

if command -v pip3 >/dev/null; then
    pip3 install -r "$(dirname "$0")/requirements.txt" || true
fi



chown $WWW_USER $WWW $WWW/Firmware $WWW/Clones $CGI

cd $CGI

sudo php ./DB_Setup.php

if [ ! -f GNSS.db ]
then
    echo "Error: GNSS.db not created. PHP installed?"
    exit 1
fi

chown $WWW_USER GNSS.db
chgrp $NAGIOS_USER GNSS.db
chmod 0770 GNSS.db

