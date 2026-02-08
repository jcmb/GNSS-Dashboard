<html>
<head>
</head>
<body>

<?php
error_reporting(E_ALL);
include 'error.php.inc';
include 'db.inc.php';

echo "Firmware Uploading:<br/>";

// Get maximum size and meassurement unit
$max = ini_get('post_max_size');
$unit = substr($max, -1);

if (!is_numeric($unit)) {
   $max = substr($max, 0, -1);
   }

// Convert to bytes
switch (strtoupper($unit)) {
case 'G':
  $max *= 1024;
case 'M':
  $max *= 1024;
case 'K':
  $max *= 1024;
}

// Get maximum size and meassurement unit
$filemax = ini_get('upload_max_filesize');
$unit = substr($filemax, -1);
if (!is_numeric($unit)) {
   $filemax = substr($filemax, 0, -1);
   }

// Convert to bytes
switch (strtoupper($unit)) {
case 'G':
  $filemax *= 1024;
case 'M':
  $filemax *= 1024;
case 'K':
  $filemax *= 1024;
}

if (30000000 > $filemax) {
   echo "The firmware files are to large to upload. It must be possible to upload at least 30Mb files";
   echo "<br/>Contact your admin";
   phpinfo();
   exit(100);
   }


#print $max;
#echo "<br/>";
#echo $_SERVER['CONTENT_LENGTH'];

if ($_SERVER['CONTENT_LENGTH'] > $max) {
   echo "The combined firmware files are to large to upload. If the files are valid then contact your admin to adjust the server settings";
   phpinfo();
   exit(100);
   }


$arr = get_defined_vars();
#print_r($arr);


#echo "<br>";
#print_r($_FILES);

#print_r($_FILES["GamelUpload"]);


$User_ID=$_REQUEST["User_ID"];
if ($User_ID=="") {
    exit ("Internal Error: No User ID");
    }

$Firmware=$_REQUEST["Firmware"];
$Firmware=clean($Firmware,strlen($Firmware));
if ($Firmware=="") {
    exit ("Internal Error: Firmware Type not provided");
    }

$Version=$_REQUEST["version"];
$Version=clean($Version,strlen($Version));
if ($Version=="") {
    echo "Firmware Version must not be blank";
    quit(100);
    }

$TitianVersion=$_REQUEST["Titianversion"];
$TitianVersion=clean($TitianVersion,strlen($TitianVersion));
if ($TitianVersion=="") {
    echo "Titan Firmware Version must not be blank";
    quit(100);
    }

if ($_FILES['AlloyUpload'] ) {
   echo "Alloy File: " , $_FILES['AlloyUpload']['name'] , ", ";
   }
else {
    exit ("Internal Error: No Alloy File");
    }

if ($error == UPLOAD_ERR_OK) {
   $tmp_name =  $_FILES['AlloyUpload']["tmp_name"];
   $BCudaName = $_FILES['AlloyUpload']["name"];
   move_uploaded_file($tmp_name, "$firmwareLocation/$AlloyName");
   echo "uploaded";
   }
else {
   echo "Upload Error";
   quit(101);
   }

echo "<br/>\n";

if ($_FILES['BarracudaUpload'] ) {
   echo "Barra File: " , $_FILES['BarracudaUpload']['name'] , ", ";
   }
else {
    exit ("Internal Error: No Barra File");
    }

if ($error == UPLOAD_ERR_OK) {
   $tmp_name =  $_FILES['BarracudaUpload']["tmp_name"];
   $BCudaName = $_FILES['BarracudaUpload']["name"];
   move_uploaded_file($tmp_name, "$firmwareLocation/$BCudaName");
   echo "uploaded";
   }
else {
   echo "Upload Error";
   quit(101);
   }

echo "<br/>\n";


if ($_FILES['ChinstrapUpload'] ) {
   echo "SPS986 File: " , $_FILES['ChinstrapUpload']['name'] , ", ";
   }
else {
    exit ("Internal Error: No SPS986 File");
    }

if ($error == UPLOAD_ERR_OK) {
   $tmp_name = $_FILES["ChinstrapUpload"]["tmp_name"];
   $ChinstrapName = $_FILES["ChinstrapUpload"]["name"];
   move_uploaded_file($tmp_name, "$firmwareLocation/$ChinstrapName");
   echo "uploaded";
   }
else {
   echo "Upload Error";
   quit(101);
   }

echo "<br/>\n";

if ($_FILES['ClarkUpload'] ) {
   echo "R780-2 File: " , $_FILES['ClarkUpload']['name'] , ", ";
   }
else {
    exit ("Internal Error: No R780-2 File");
    }

if ($error == UPLOAD_ERR_OK) {
   $tmp_name = $_FILES["ClarkUpload"]["tmp_name"];
   $ClarkName = $_FILES["ClarkUpload"]["name"];
   move_uploaded_file($tmp_name, "$firmwareLocation/$ClarkName");
   echo "uploaded";
   }
else {
   echo "Upload Error";
   quit(101);
   }

echo "<br/>\n";

if ($_FILES['LancetUpload'] ) {
   echo "Lancet File: " , $_FILES['LancetUpload']['name'] , ", ";
   }
else {
    exit ("Internal Error: No Lancet File");
    }

$error=$_FILES["LancetUpload"]["error"];
if ($error == UPLOAD_ERR_OK) {
   $tmp_name = $_FILES["LancetUpload"]["tmp_name"];
   $LancetName = $_FILES["LancetUpload"]["name"];
   move_uploaded_file($tmp_name, "$firmwareLocation/$LancetName");
   echo "uploaded";
   }
else {
   echo "Upload Error";
   quit(101);
   }

echo "<br/>\n";

if ($_FILES['KryptonUpload'] ) {
   echo "BD992 File: " , $_FILES['KryptonUpload']['name'] , ", ";
   }
else {
    exit ("Internal Error: No BD992 File");
    }

if ($error == UPLOAD_ERR_OK) {
   $tmp_name = $_FILES["KryptonUpload"]["tmp_name"];
   $KryptonName = $_FILES["KryptonUpload"]["name"];
   move_uploaded_file($tmp_name, "$firmwareLocation/$KryptonName");
   echo "uploaded";
   }
else {
   echo "Upload Error";
   quit(101);
   }

echo "<br/>\n";

$db = new SQLite3($databaseFile);
$db->exec("PRAGMA busy_timeout=5000");

#echo "Datbase file " , $databaseFile, " opened<br/>";

#  echo "UPDATE Firmware SET Version=\"$Version\",    Titian_Version=\"$TitianVersion\", BCudaFile=\"$BCudaName\", BrewsterFile=\"$BrewsterName\", ChinstrapFile=\"$ChinstrapName\", GamelFile=\"$GamelName\", RockyFile=\"$RockyName\",  TennisBallFile=\"$TennisBallName\", ZeppelinFile=\"$ZeppelinName\" WHERE Type=\"$Firmware\"";



$db->exec("UPDATE Firmware SET
   Titian_Version=\"$TitianVersion\",
   AlloyFile=\"$AlloyName\",
   BarracudaFile=\"$BCudaName\",
   ClarkFile=\"$ClarkName\",
   ChinstrapFile=\"$ChinstrapName\",
   LancetFile=\"$LancetName\",
   KryptonFile=\"$KryptonName\" WHERE Type=\"$Firmware\"");

if ( $Firmware == "Beta" or $Firmware == "Released" ) {
   $db->exec("UPDATE Firmware SET
      Titian_Version=\"$TitianVersion\",
      AlloyFile=\"$AlloyName\",
      BarracudaFile=\"$BCudaName\",
      ClarkFile=\"$ClarkName\",
      ChinstrapFile=\"$ChinstrapName\",
      LancetFile=\"$LancetName\",
      KryptonFile=\"$KryptonName\" WHERE Type=\"Branch\"");
   }

if ( $Firmware == "Released" ) {
   $db->exec("UPDATE Firmware SET
      Titian_Version=\"$TitianVersion\",
      AlloyFile=\"$AlloyName\",
      BarracudaFile=\"$BCudaName\",
      ClarkFile=\"$ClarkName\",
      ChinstrapFile=\"$ChinstrapName\",
      LancetFile=\"$LancetName\",
      KryptonFile=\"$KryptonName\" WHERE Type=\"Beta\"");
   }

// Close the connection
$db->close();

print "<p/>You can now:<ul>";
echo '<li><a href="/Dashboard/Receiver_List.php?User_ID=',$User_ID,'">View and edit receivers</a>';
echo '<li><a href="/Dashboard/Receiver_Upgrade.php?User_ID=',$User_ID,'">Update Reciever Firmware</a>';
echo '<li><a href="/Dashboard/fw_upload.php?User_ID=',$User_ID,'">Upload more firmware</a>';
echo '<li><a href="/Dashboard/Edit_User.php?User_ID=',$User_ID,'">Edit your user details</a>';

?>
</body>
</html>
