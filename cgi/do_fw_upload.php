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
   exit(100);
   }


#print $max;
#echo "<br/>";
#echo $_SERVER['CONTENT_LENGTH'];

if ($_SERVER['CONTENT_LENGTH'] > $max) {
   echo "The combined firmware files are to large to upload. If the files are valid then contact your admin to adjust the server settings";
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

$userCheckDb = new SQLite3($databaseFile);
$userStmt = $userCheckDb->prepare('SELECT id FROM Users WHERE id=?');
$userStmt->bindValue(1, (int)$User_ID, SQLITE3_INTEGER);
$userResult = $userStmt->execute();
if (!$userResult || !$userResult->fetchArray()) {
    exit("Invalid User ID");
    }
$userCheckDb->close();

function sanitize_firmware_filename($name) {
   $name = basename($name);
   if (!preg_match('/^[A-Za-z0-9._-]+\.(timg|img)$/', $name)) {
      exit("Invalid firmware filename");
      }
   return $name;
   }

$Firmware=$_REQUEST["Firmware"];
$Firmware=clean($Firmware,strlen($Firmware));
if ($Firmware=="") {
    exit ("Internal Error: Firmware Type not provided");
    }

$TitanVersion=$_REQUEST["Titanversion"];
$TitanVersion=clean($TitanVersion,strlen($TitanVersion));
if ($TitanVersion=="") {
    echo "Titan Firmware Version must not be blank";
    quit(100);
    }

$allowMissing = !empty($_REQUEST['AllowMissing']);

$uploadFields = array(
   array('field' => 'AlloyUpload', 'nameVar' => 'AlloyName', 'label' => 'Alloy', 'errorLabel' => 'Alloy', 'dbCol' => 'AlloyFile'),
   array('field' => 'BarracudaUpload', 'nameVar' => 'BCudaName', 'label' => 'Barra', 'errorLabel' => 'Barra', 'dbCol' => 'BarracudaFile'),
   array('field' => 'ChinstrapUpload', 'nameVar' => 'ChinstrapName', 'label' => 'SPS986', 'errorLabel' => 'SPS986', 'dbCol' => 'ChinstrapFile'),
   array('field' => 'ClarkUpload', 'nameVar' => 'ClarkName', 'label' => 'R780-2', 'errorLabel' => 'R780-2', 'dbCol' => 'ClarkFile'),
   array('field' => 'LancetUpload', 'nameVar' => 'LancetName', 'label' => 'Lancet', 'errorLabel' => 'Lancet', 'dbCol' => 'LancetFile'),
   array('field' => 'KryptonUpload', 'nameVar' => 'KryptonName', 'label' => 'BD992', 'errorLabel' => 'BD992', 'dbCol' => 'KryptonFile'),
);

$AlloyName = '';
$BCudaName = '';
$ChinstrapName = '';
$ClarkName = '';
$LancetName = '';
$KryptonName = '';

$db = new SQLite3($databaseFile);
$db->exec("PRAGMA busy_timeout=5000");

if ($allowMissing) {
   echo "Partial upload: missing platform files will keep existing filenames.<br/>\n";
   $result = $db->query("SELECT AlloyFile, BarracudaFile, ChinstrapFile, ClarkFile, LancetFile, KryptonFile FROM Firmware WHERE Type=\"$Firmware\"");
   $existing = $result->fetchArray(SQLITE3_ASSOC);
   if ($existing) {
      $AlloyName = $existing['AlloyFile'];
      $BCudaName = $existing['BarracudaFile'];
      $ChinstrapName = $existing['ChinstrapFile'];
      $ClarkName = $existing['ClarkFile'];
      $LancetName = $existing['LancetFile'];
      $KryptonName = $existing['KryptonFile'];
      }
   }

foreach ($uploadFields as $upload) {
   $field = $upload['field'];
   $nameVar = $upload['nameVar'];

   if (isset($_FILES[$field]) && $_FILES[$field]['error'] != UPLOAD_ERR_NO_FILE && $_FILES[$field]['name'] != '') {
      echo $upload['label'] , " File: " , $_FILES[$field]['name'] , ", ";
      $error = $_FILES[$field]['error'];
      if ($error == UPLOAD_ERR_OK) {
         $tmp_name = $_FILES[$field]['tmp_name'];
         $$nameVar = sanitize_firmware_filename($_FILES[$field]['name']);
         move_uploaded_file($tmp_name, "$firmwareLocation/" . $$nameVar);
         echo "uploaded";
         }
      else {
         echo "Upload Error";
         quit(101);
         }
      }
   elseif ($allowMissing) {
      echo $upload['label'] , ": not provided, keeping existing file";
      }
   else {
      exit ("Internal Error: No " . $upload['errorLabel'] . " File");
      }

   echo "<br/>\n";
   }

#echo "Datbase file " , $databaseFile, " opened<br/>";

#  echo "UPDATE Firmware SET Version=\"$Version\",    Titan_Version=\"$TitanVersion\", BCudaFile=\"$BCudaName\", BrewsterFile=\"$BrewsterName\", ChinstrapFile=\"$ChinstrapName\", GamelFile=\"$GamelName\", RockyFile=\"$RockyName\",  TennisBallFile=\"$TennisBallName\", ZeppelinFile=\"$ZeppelinName\" WHERE Type=\"$Firmware\"";

echo "UPDATE Firmware SET    Titan_Version=\"$TitanVersion\",    AlloyFile=\"$AlloyName\",   BarracudaFile=\"$BCudaName\",   ClarkFile=\"$ClarkName\",   ChinstrapFile=\"$ChinstrapName\",   LancetFile=\"$LancetName\",   KryptonFile=\"$KryptonName\" WHERE Type=\"$Firmware\"";




$db->exec("UPDATE Firmware SET
   Titan_Version=\"$TitanVersion\",
   AlloyFile=\"$AlloyName\",
   BarracudaFile=\"$BCudaName\",
   ClarkFile=\"$ClarkName\",
   ChinstrapFile=\"$ChinstrapName\",
   LancetFile=\"$LancetName\",
   KryptonFile=\"$KryptonName\" WHERE Type=\"$Firmware\"");

if ( $Firmware == "Beta" or $Firmware == "Released" ) {
   $db->exec("UPDATE Firmware SET
      Titan_Version=\"$TitanVersion\",
      AlloyFile=\"$AlloyName\",
      BarracudaFile=\"$BCudaName\",
      ClarkFile=\"$ClarkName\",
      ChinstrapFile=\"$ChinstrapName\",
      LancetFile=\"$LancetName\",
      KryptonFile=\"$KryptonName\" WHERE Type=\"Branch\"");
   }

if ( $Firmware == "Released" ) {
   $db->exec("UPDATE Firmware SET
      Titan_Version=\"$TitanVersion\",
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
