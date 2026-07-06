<?php
   $databaseFile = "/usr/lib/cgi-bin/Dashboard/GNSS.db";
   $firmwareLocation = "/var/www/html/Dashboard/Firmware";

   function gnss_open_db($path = null)
   {
      global $databaseFile;
      if ($path === null) {
         $path = $databaseFile;
      }
      $db = new SQLite3($path);
      if (!$db) {
         return false;
      }
      $db->busyTimeout(10000);
      $db->exec('PRAGMA journal_mode=WAL');
      return $db;
   }

   function clean($input, $maxlength)
   {
      $input = substr($input, 0, $maxlength);
      $input = EscapeShellCmd($input);
      return ($input);
   }
?>
