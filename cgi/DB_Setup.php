<?php
   error_reporting(E_ALL);
   include 'error.php.inc';
   include 'db.inc.php';
  // open the db file (test.db) if it exists, or create it if it doesn't

  $db = new SQLite3($databaseFile);
  echo "Datbase file " , $databaseFile, " opened<br/>";
  // create a new table in the file
  $db->exec('CREATE TABLE IF NOT EXISTS  GNSS (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      Enabled BOOLEAN,
      User_ID INTEGER,
      name TEXT,
      Firmware TEXT,
      Loc_Group TEXT,
      Address TEXT,
      Port INTEGER,
      Reciever_Type TEXT,
      Password TEXT,
      Pos_Type TEXT,
      Static BOOLEAN,
      LowLatency BOOLEAN,
      Elev_Mask NUMERIC,
      PDOP NUMERIC,
      Logging_Enabled BOOLEAN,
      Logging_Duration NUMERIC,
      Logging_Measurement_Interval NUMERIC,
      Logging_Position_Interval NUMERIC,
      FTP_Enabled BOOLEAN,
      FTP_To TEXT,
      Antenna NUMERIC,
      Ant_Height NUMERIC,
      Measurement_Method TEXT,
      Ref_Name TEXT,
      Ref_Code TEXT,
      Ref_Lat NUMERIC,
      Ref_Long NUMERIC,
      Ref_Height NUMERIC,
      Email_Enabled BOOLEAN,
      Email_To TEXT,
      Auth NUMERIC,
      NTRIP_Enabled NUMERIC,
      NTRIP_1_Mount TEXT,
      NTRIP_1_Type TEXT,
      NTRIP_2_Mount TEXT,
      NTRIP_2_Type TEXT,
      NTRIP_3_Mount TEXT,
      NTRIP_3_Type TEXT,
      IBSS_Enabled BOOLEAN,
      IBSS_Org TEXT,
      IBSS_Test_User TEXT,
      IBSS_Test_Password TEXT,
      IBSS_1_Mount TEXT,
      IBSS_1_Type TEXT,
      Frequencies NUMERIC,
      GPS BOOLEAN,
      GLN BOOLEAN,
      GAL BOOLEAN,
      BDS BOOLEAN,
      QZSS BOOLEAN,
      NAGIOS BOOLEAN,
      TIMED_ACTIVE BOOLEAN,
      TIMED_MIN_DELTA NUMERIC,
      TIMED_MAX_DELTA NUMERIC,
      TRACKING_MASK NUMERIC,
      RadioEnabled BOOLEAN,
      RadioOnOffState BOOLEAN,
      RadioMode TEXT

      )');


  $db->exec('CREATE TABLE IF NOT EXISTS Firmware (
      Type TEXT,
      Version TEXT,
      GamelFile TEXT,
      RockyFile TEXT,
      BrewsterFile TEXT,
      TennisBallFile TEXT,
      ZeppelinFile TEXT
      )');

  $db->exec('INSERT INTO Firmware VALUES("Released","0.0","","","","","")');
  $db->exec('INSERT INTO Firmware VALUES("Beta","0.1","","","","","")');
  $db->exec('INSERT INTO Firmware VALUES("Branch","0.2","","","","","")');
  $db->exec('INSERT INTO Firmware VALUES("Trunk","0.3","","","","","")');

  $db->exec('CREATE TABLE IF NOT EXISTS Users (
      ID INTEGER PRIMARY KEY AUTOINCREMENT  ,
      Name TEXT,
      Salt BLOB,
      PWHash BLOB,
      Email TEXT)');


?>
