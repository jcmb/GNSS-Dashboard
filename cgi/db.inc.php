<?php
   $databaseFile = "/usr/lib/cgi-bin/Dashboard/GNSS.db";
   $firmwareLocation = "/var/www/html/Dashboard/Firmware";

   function clean($input, $maxlength)
   {
      $input = substr($input, 0, $maxlength);
      $input = EscapeShellCmd($input);
      return ($input);
   }
?>
