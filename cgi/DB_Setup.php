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
      GLN BOOLEAN,
      GAL BOOLEAN,
      BDS BOOLEAN,
      QZSS BOOLEAN,
      NAGIOS BOOLEAN,
      FIRMWARE_Version TEXT
      )');

  $db->exec('CREATE TABLE IF NOT EXISTS STATUS (
      id INTEGER PRIMARY KEY,
      Checked BOOLEAN,
      Last_Check DATETIME,
      Firmware_Version STRING,
      Firmware_Date SRING,
      Alive BOOLEAN,
      Reciever_Type TEXT,
      Reciever_Type_Valid BOOLEAN,
      Pos_Type TEXT,
      Pos_Type_Valid BOOLEAN,
      Static BOOLEAN,
      Staitc_Valid BOOLEAN,
      Elev_Mask NUMERIC,
      Elev_Mask_Valid BOOLEAN,
      PDOP NUMERIC,
      PDOP_Valid BOOLEAN,
      Logging_Enabled BOOLEAN,
      Logging_Duration NUMERIC,
      Logging_Measurement_Interval NUMERIC,
      Logging_Position_Interval NUMERIC,
      Logging_Valid BOOLEAN,
      FTP_Enabled BOOLEAN,
      FTP_To TEXT,
      FTP_Valid BOOLEAN,
      Antenna NUMERIC,
      Ant_Height NUMERIC,
      Measurement_Method TEXT,
      Antenna_Valid BOOLEAN,
      Email_Enabled BOOLEAN,
      Email_To TEXT,
      Email_Valid BOOLEAN,
      Auth NUMERIC,
      Auth_Valid BOOLEAN,
      NTRIP_Enabled NUMERIC,
      NTRIP_1_Mount TEXT,
      NTRIP_1_Type TEXT,
      NTRIP_1_Valid BOOLEAN,
      NTRIP_2_Mount TEXT,
      NTRIP_2_Type TEXT,
      NTRIP_2_Valid BOOLEAN,
      NTRIP_3_Mount TEXT,
      NTRIP_3_Type TEXT,
      NTRIP_3_Valid BOOLEAN,
      IBSS_Enabled BOOLEAN,
      IBSS_Org TEXT,
      IBSS_Test_User TEXT,
      IBSS_Test_Password TEXT,
      IBSS_1_Mount TEXT,
      IBSS_1_Type TEXT,
      IBSS_Valid BOOLEAN,
      GLN BOOLEAN,
      GLN_Valid BOOLEAN,
      GAL BOOLEAN,
      GAL_Valid BOOLEAN,
      BDS BOOLEAN,
      BDS_Valid BOOLEAN,
      QZSS BOOLEAN,
      QZSS_Valid BOOLEAN,
      FIRMWARE_Valid BOOLEAN

      )');

  $db->exec('CREATE TABLE IF NOT EXISTS Firmware (
      Type TEXT,
      Version TEXT,
      Titian_Version TEXT,
      GamelFile TEXT,
      RockyFile TEXT,
      BrewsterFile TEXT,
      ZeppelinFile TEXT,
      TennisBallFile TEXT,
      ChinstrapFile TEXT,
      BCudaFile  TEXT
      )');

  $db->exec('INSERT INTO Firmware VALUES("Released","0.0","","","","","","","","")');
  $db->exec('INSERT INTO Firmware VALUES("Beta","0.1","","","","","","","","")');
  $db->exec('INSERT INTO Firmware VALUES("Branch","0.2","","","","","","","","")');
  $db->exec('INSERT INTO Firmware VALUES("Trunk","0.3","","","","","","","","")');

  $db->exec('CREATE TABLE IF NOT EXISTS Users (
      ID INTEGER PRIMARY KEY AUTOINCREMENT  ,
      Name TEXT,
      Salt BLOB,
      PWHash BLOB,
      Email TEXT)');


?>
