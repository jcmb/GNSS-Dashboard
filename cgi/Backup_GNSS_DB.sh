#!/bin/bash
cd /usr/lib/cgi-bin/Dashboard
rm GNSS.mime
mpack -s "GNSS.db backup" -o GNSS.mime GNSS.db
cat email_to GNSS.mime | msmtp Geoffrey_Kirk+GNSS_Backup@Trimble.com
