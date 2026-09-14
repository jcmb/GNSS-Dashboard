<?php
   $databaseFile = "/usr/lib/cgi-bin/Dashboard/GNSS.db";
   $firmwareLocation = "/var/www/html/Dashboard/Firmware";
   $sysLogLocation = "/var/www/html/Dashboard/SysLog";

   function gnss_open_db($path = null)
   {
      global $databaseFile;
      if ($path === null) {
         $path = $databaseFile;
      }
      try {
         $db = new SQLite3($path);
      } catch (Exception $e) {
         return false;
      }
      if (!$db) {
         return false;
      }
      $db->busyTimeout(10000);
      // WAL needs a writable directory for GNSS.db-wal / GNSS.db-shm.
      @$db->exec('PRAGMA journal_mode=WAL');
      return $db;
   }

   function clean($input, $maxlength)
   {
      $input = substr($input, 0, $maxlength);
      $input = EscapeShellCmd($input);
      return ($input);
   }
?>
