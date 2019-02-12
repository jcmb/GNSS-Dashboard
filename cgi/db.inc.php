<?php
   $databaseFile = "/usr/lib/cgi-bin/Dashboard/GNSS.db";
   $firmwareLocation = "/usr/Firmware";

   function clean($input, $maxlength)
   {
      $input = substr($input, 0, $maxlength);
      $input = EscapeShellCmd($input);
      return ($input);
   }
?>
