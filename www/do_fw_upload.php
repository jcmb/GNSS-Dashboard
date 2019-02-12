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

if (10000000 > $filemax) {
   echo "The firmware files are to large to upload. It must be possible to upload at least 10Mb files";
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


if ($_FILES['GamelUpload'] ) {
   echo "SPS855 File: " , $_FILES['GamelUpload']['name'] , ", ";
   }
else {
    exit ("Internal Error: No SPS855 File");
    }

$error=$_FILES["GamelUpload"]["error"];
if ($error == UPLOAD_ERR_OK) {
   $tmp_name = $_FILES["GamelUpload"]["tmp_name"];
   $GamelName = $_FILES["GamelUpload"]["name"];
   move_uploaded_file($tmp_name, "$firmwareLocation/$GamelName");
   echo "uploaded";
   }
else {
   echo "Upload Error";
   quit(101);
   }

echo "<br/>";

if ($_FILES['RockyUpload'] ) {
   echo "SPS985 File: " , $_FILES['RockyUpload']['name'] , ", ";
   }
else {
    exit ("Internal Error: No SPS985 File");
    }

if ($error == UPLOAD_ERR_OK) {
   $tmp_name = $_FILES["RockyUpload"]["tmp_name"];
   $RockyName = $_FILES["RockyUpload"]["name"];
   move_uploaded_file($tmp_name, "$firmwareLocation/$RockyName");
   echo "uploaded";
   }
else {
   echo "Upload Error";
   quit(101);
   }

echo "<br/>";

if ($_FILES['MetallicaUpload'] ) {
   echo "SPS356 File: " , $_FILES['MetallicaUpload']['name'] , ", ";
   }
else {
    exit ("Internal Error: No SPS356 File");
    }

if ($error == UPLOAD_ERR_OK) {
   $tmp_name = $_FILES["MetallicaUpload"]["tmp_name"];
   $BrewsterName = $_FILES["MetallicaUpload"]["name"];
   move_uploaded_file($tmp_name, "$firmwareLocation/$MetallicaName");
   echo "uploaded";
   }
else {
   echo "Upload Error";
   quit(101);
   }

echo "<br/>";

if ($_FILES['TennisBallUpload'] ) {
   echo "SPS585 File: " , $_FILES['TennisBallUpload']['name'] , ", ";
   }
else {
    exit ("Internal Error: No SPS585 File");
    }

if ($error == UPLOAD_ERR_OK) {
   $tmp_name = $_FILES["TennisBallUpload"]["tmp_name"];
   $TennisBallName = $_FILES["TennisBallUpload"]["name"];
   move_uploaded_file($tmp_name, "$firmwareLocation/$TennisBallName");
   echo "uploaded";
   }
else {
   echo "Upload Error";
   quit(101);
   }

echo "<br/>";

if ($_FILES['ZeppelinUpload'] ) {
   echo "BD935 File: " , $_FILES['ZeppelinUpload']['name'] , ", ";
   }
else {
    exit ("Internal Error: No BD935 File");
    }

if ($error == UPLOAD_ERR_OK) {
   $tmp_name = $_FILES["ZeppelinUpload"]["tmp_name"];
   $ZeppelinName = $_FILES["ZeppelinUpload"]["name"];
   move_uploaded_file($tmp_name, "$firmwareLocation/$ZeppelinName");
   echo "uploaded";
   }
else {
   echo "Upload Error";
   quit(101);
   }

echo "<br/>";

$db = new SQLite3($databaseFile);   
#echo "Datbase file " , $databaseFile, " opened<br/>";

#echo "UPDATE Firmware SET Version=\"$Version\", GamelFile=\"$GamelName\", RockyFile=\"$RockyName\", BrewsterFile=\"$BrewsterName\", TennisBallFile=\"$TennisBallName\", ZeppelinFile=\"$ZeppelinName\" WHERE Type=\"$Firmware\"";



$db->exec("UPDATE Firmware SET Version=\"$Version\", GamelFile=\"$GamelName\", RockyFile=\"$RockyName\", BrewsterFile=\"$BrewsterName\", TennisBallFile=\"$TennisBallName\", ZeppelinFile=\"$ZeppelinName\" WHERE Type=\"$Firmware\"");

print "<p/>You can now:<ul>";
echo '<li><a href="/Dashboard/Receiver_List.php?User_ID=',$User_ID,'">View and edit receivers</a>';
echo '<li><a href="/Dashboard/Receiver_Upgrade.php?User_ID=',$User_ID,'">Update Reciever Firmware</a>';
echo '<li><a href="/Dashboard/fw_upload.php?User_ID=',$User_ID,'">Upload more firmware</a>';
echo '<li><a href="/Dashboard/Edit_User.php?User_ID=',$User_ID,'">Edit your user details</a>';

?>
</body>
</html>
