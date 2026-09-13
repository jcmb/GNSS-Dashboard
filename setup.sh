#!/bin/bash

if [ "$(id -u)" -ne 0 ]; then
   echo "This script must be run as root (e.g. sudo setup.sh)" >&2
   exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
RUN_INSTALL=0

if [ "${1:-}" = "--install" ]; then
    RUN_INSTALL=1
elif [ "${1:-}" = "--help" ] || [ "${1:-}" = "-h" ]; then
    echo "Usage: $0 [--install]"
    echo "  (default)   Copy Dashboard files only"
    echo "  --install   Copy files and run install/setup steps"
    exit 0
elif [ -n "${1:-}" ]; then
    echo "Unknown option: $1" >&2
    echo "Usage: $0 [--install]" >&2
    exit 1
fi

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

# SQLite WAL creates GNSS.db-wal / GNSS.db-shm beside the DB. The CGI
# directory and those sidecars must be writable by www-data and nagios.
fix_db_permissions() {
    chown "$WWW_USER:$NAGIOS_USER" "$CGI" "$CGI/User" 2>/dev/null || true
    chmod 2775 "$CGI" "$CGI/User" 2>/dev/null || true
    if [ -f "$CGI/GNSS.db" ]; then
        chown "$WWW_USER:$NAGIOS_USER" "$CGI"/GNSS.db "$CGI"/GNSS.db-wal "$CGI"/GNSS.db-shm 2>/dev/null || true
        chmod 0660 "$CGI"/GNSS.db 2>/dev/null || true
        chmod 0660 "$CGI"/GNSS.db-wal "$CGI"/GNSS.db-shm 2>/dev/null || true
    fi
}

if [ "$RUN_INSTALL" -eq 1 ]; then
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
        REQ="$SCRIPT_DIR/requirements.txt"
        if [ ! -f "$REQ" ]; then
            echo "Warning: requirements file not found: $REQ" >&2
        else
            PIP3=(pip3 install -r "$REQ")
            if pip3 install --help 2>&1 | grep -q break-system-packages; then
                PIP3=(pip3 install --break-system-packages -r "$REQ")
            fi
            "${PIP3[@]}" || true
        fi
    fi

    chown $WWW_USER $WWW $WWW/Firmware $WWW/Clones $CGI

    cd $CGI

    sudo php ./DB_Setup.php

    if [ ! -f GNSS.db ]
    then
        echo "Error: GNSS.db not created. PHP installed?"
        exit 1
    fi
fi

fix_db_permissions

echo "Dashboard files copied."
if [ "$RUN_INSTALL" -eq 0 ]; then
    echo "Install steps skipped (default). Run '$0 --install' to run full setup."
fi
echo "DB permissions: $CGI should be writable by $WWW_USER and group $NAGIOS_USER (WAL sidecars)."

