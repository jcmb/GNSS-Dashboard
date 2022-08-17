<html>
<head>
<title>
<?php
$DUP=FALSE;
if ($_REQUEST["GNSS_ID"]) {
   if ($_REQUEST["DUP"]) {
      echo "Add GNSS Receiver based on an existing receiver";
      $Editing=TRUE;
      $DUP=TRUE;
      }
   else {
      echo "Edit GNSS Receiver";
      $Editing=TRUE;
      }
   }
else {
   echo "Add GNSS Receiver";
   $Editing=FALSE;
   }

?>
</title>

<link rel="stylesheet" type="text/css" href="/Dashboard/style.css"></link>
<link rel="stylesheet" type="text/css" href="/Dashboard/tcui-styles.css">
<script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
<script src="/Dashboard/jquery.tablesorter.min.js"></script>
<body class="page">
<div class="container clearfix">
  <div style="padding: 10px 10px 10px 0 ;"> <a href="http://construction.trimble.com/">
        <img src="/Dashboard/trimble-logo.png" alt="Trimble Logo" id="logo"> </a>
      </div>
  <!-- end #logo-area -->
</div>
<div id="top-header-trim"></div>
<div id="content-area">
<div id="content">
<div id="main-content" class="clearfix">

<?php
#   error_reporting(E_ALL);
#   include 'error.php.inc';
   include 'db.inc.php';

   if ($_REQUEST["GNSS_ID"]) {
      if ($DUP) {
         echo "Add GNSS Receiver based on existing";
         }
      else {
         echo "Edit GNSS Receiver";
         }
      $db = new SQLite3($databaseFile);

     // create a new table in the file
      $query="SELECT * FROM GNSS WHERE id='".$_REQUEST["GNSS_ID"]."'";
   //   echo $query;
      $result = $db->query($query);

      if (!($result))
        {
        showerror();
        }
      $row = $result->fetchArray(SQLITE3_ASSOC);
      if ($DUP) {
         $row["Address"]="";
         }
   //   echo $result->numColumns();
      // Display the results
      }
   else {
      echo "Add GNSS Receiver";
      $Editing=FALSE;
      }

?>

</H1>

<form name="input" action="/cgi-bin/Dashboard/Do_Edit_GNSS.py" method="get">

<?php
var_dump($row);

echo '<input name="User_ID" type="hidden" value="'.$_REQUEST["User_ID"] . '">';

$User_ID=$_REQUEST["User_ID"];
if ($User_ID=="") {
    exit ("Internal Error: No User ID");
    }

if ($Editing && !$DUP) {
   echo '<input name="GNSS_ID" type="hidden" value="'.$_REQUEST["GNSS_ID"] . '">';
   }

?>

<p/>
<table border="0">
<tr><td>
Name:
</td><td>
<input name="Name" type="text" value="<?php echo $row["name"] ?>"/>
</td></tr>

<tr><td>
Enabled:
</td><td>
<input name="Enabled" type="checkbox" <?php echo ($row["Enabled"]==1)?"checked":""; echo ($Editing?"":"checked") ?>/>
</td></tr>

<tr><td>
Receiver Group:
</td><td>
<input name="Loc_Group" type="text" value="<?php echo $row["Loc_Group"] ?>"/>
</td></tr>



<tr><td>
Address:
</td><td>
<input name="Address" type="text"  value="<?php echo $row["Address"] ?>">
</td></tr>

<tr><td>
Port:
</td><td>
<input name="Port" type="number" min="1" max="65535" step="1" value="<?php echo ($row["Port"])?$row["Port"]:"80" ?>" />
</td></tr>

<tr><td>
Firmware to install:
</td><td>
<select required name="Firmware">
  <option value="Released" <?php echo ($row["Firmware"]=="Released")?"selected":"" ?>>Released</option>
  <option value="Beta" <?php echo ($row["Firmware"]=="Beta")?"selected":"" ?>>Beta</option>
  <option value="Branch" <?php echo ($row["Firmware"]=="Branch")?"selected":"" ?> <?php echo ($Editing?"":"selected") ?> >Branch</option>
  <option value="Trunk" <?php echo ($row["Firmware"]=="Trunk")?"selected":"" ?>>Trunk</option>
  <option value="Unmanaged" <?php echo ($row["Firmware"]=="Unmanaged")?"selected":"" ?>>Unmanaged</option>
</select>
</td></tr>


<tr><td>
Receiver:
</td><td>
<select required name=Receiver_Type>
  <option value="118" <?php echo ($row["Reciever_Type"]=="118")?"selected":"" ?> <?php echo ($Editing?"":"selected") ?>>SPS855</option>
  <option value="107" <?php echo ($row["Reciever_Type"]=="107")?"selected":"" ?> >SPS852</option>
  <option value="250" <?php echo ($row["Reciever_Type"]=="250")?"selected":"" ?>>SPS585</option>
  <option value="101" <?php echo ($row["Reciever_Type"]=="101")?"selected":"" ?>>SPS985</option>
  <option value="169" <?php echo ($row["Reciever_Type"]=="169")?"selected":"" ?>>SPS986</option>
  <option value="138" <?php echo ($row["Reciever_Type"]=="138")?"selected":"" ?>>SPS356</option>
  <option value="38" <?php echo ($row["Reciever_Type"]=="38")?"selected":"" ?> >SPS850</option>
  <option value="59" <?php echo ($row["Reciever_Type"]=="59")?"selected":"" ?> >SPS851</option>
  <option value="240" <?php echo ($row["Reciever_Type"]=="240")?"selected":"" ?> >BD935</option>
  <option value="100" <?php echo ($row["Reciever_Type"]=="100")?"selected":"" ?> >R10</option>
  <option value="188" <?php echo ($row["Reciever_Type"]=="188")?"selected":"" ?> >R750</option>
  <option value="76" <?php echo ($row["Reciever_Type"]=="76")?"selected":"" ?> >NetR9</option>
</select>
</td></tr>

<tr><td>
Admin password:
</td><td>
<input name="Password" type="text" value="<?php echo $row["Password"]?$row["Password"]:"password" ?>"/>
</td></tr>

<tr><td>
Position Type:
</td><td>
<input name="Pos_Type" type="text" value="<?php echo $row["Pos_Type"]?$row["Pos_Type"]:"RTK" ?>"/>
</td></tr>

<tr><td>
Static:
</td><td>
<input name="Static" type="checkbox" <?php echo ($row["Static"]==1?"checked":""); ?>/>
</td></tr>

<tr><td>
Low Latency:
</td><td>
<input name="LowLatency" type="checkbox" <?php echo ($row["LowLatency"]==1?"checked":""); ?>/>
</td></tr>

<tr><td>
Elevation Mask:
</td><td>
<input name="Elev_Mask" type="text" value="<?php echo $row["Elev_Mask"]?$row["Elev_Mask"]:"10" ?>"/>
</td></tr>

<tr><td>
PDOP:
</td><td>
<input name="PDOP" type="text" value="<?php echo $row["PDOP"]?$row["PDOP"]:"99" ?>"/>
</td></tr>

<tr><td>
Frequencies:
</td><td>
<select required name="Frequencies">
  <option value="1" <?php echo ($row["Frequencies"]=="1")?"selected":"" ?>> Single </option>
  <option value="2" <?php echo ($row["Frequencies"]=="2")?"selected":"" ?>> Dual </option>
  <option value="3" <?php echo ($row["Frequencies"]=="3")?"selected":"" ?> <?php echo ($Editing?"":"selected") ?>>Triple</option>
</select>
</td></tr>


<tr><td>
GPS Enabled:
</td><td>
<input name="GPS" type="checkbox" <?php echo ($row["GPS"]==1?"checked":""); echo ($Editing?"":"checked") ?>/>
</td></tr>

<tr><td>
GLONASS Enabled:
</td><td>
<input name="GLN" type="checkbox" <?php echo ($row["GLN"]==1?"checked":""); echo ($Editing?"":"checked") ?>/>
</td></tr>

<tr><td>
Galileo Enabled:
</td><td>
<input name="GAL" type="checkbox" <?php echo ($row["GAL"]==1?"checked":""); echo ($Editing?"":"checked") ?>/>
</td></tr>

<tr><td>
BDS Enabled:
</td><td>
<input name="BDS" type="checkbox" <?php echo ($row["BDS"]==1?"checked":""); echo ($Editing?"":"checked") ?>/>
</td></tr>

<tr><td>
QZSS Enabled:
</td><td>
<input name="QZSS" type="checkbox" <?php echo ($row["QZSS"]==1?"checked":""); echo ($Editing?"":"checked") ?>/>
</td></tr>

<tr><td>
SBAS Enabled:
</td><td>
<input name="SBAS" type="checkbox" <?php echo ($row["SBAS"]==1?"checked":""); echo ($Editing?"":"checked") ?>/>
</td></tr>

<tr><td>
Authentication:
</td><td>
<select required name="Auth">
  <option value="no" <?php echo ($row["Auth"]=="no"?"selected":""); echo ($Editing?"checked":"") ?>>None</option>
  <option value="anonymous" <?php echo ($row["Auth"]=="anonymous"?"selected":""); echo ($Editing?"":"selected") ?>>Enabled with Anonymous Access</option>
  <option value="yes" <?php echo ($row["Auth"]=="yes"?"selected":""); ?>>Enabled</option>
</select>
</td></tr>

<tr><td>
Nagios Monitor:
</td><td>
<input name="NAGIOS" type="checkbox" <?php echo ($row["NAGIOS"]==1?"checked":""); echo ($Editing?"":"checked") ?>/>
</td></tr>
</table>
<p/>

<table>
<caption>Reference Point & Antenna</caption>
<tr><td>
Type:
</td><td>
<select required name="Antenna">
  <option value="209" <?php echo ($row["Antenna"]=="209"?"selected":""); ?>>GNSS Choke Ring</option>
  <option value="85" <?php echo ($row["Antenna"]=="85"?"selected":""); ?>>Zephyr</option>
  <option value="86" <?php echo ($row["Antenna"]=="86"?"selected":""); ?>>Zephyr Geodetic</option>
  <option value="194" <?php echo ($row["Antenna"]=="194"?"selected":""); ?>>GA510</option>
  <option value="250" <?php echo ($row["Antenna"]=="250"?"selected":""); ?>>GA530</option>
  <option value="470" <?php echo ($row["Antenna"]=="470"?"selected":""); ?>>GA830</option>
  <option value="379" <?php echo ($row["Antenna"]=="379"?"selected":""); ?>>SPS585</option>
  <option value="147" <?php echo ($row["Antenna"]=="147"?"selected":""); ?>>SPS985</option>
  <option value="569" <?php echo ($row["Antenna"]=="569"?"selected":""); ?>>SPS986</option>
  <option value="184" <?php echo ($row["Antenna"]=="184"?"selected":""); ?>>Zephyr 2</option>
  <option value="185" <?php echo ($row["Antenna"]=="185"?"selected":"");  echo ($Editing?"":"selected") ?>>Zephyr Geodetic 2</option>
  <option value="512" <?php echo ($row["Antenna"]=="512"?"selected":""); ?>>Zephyr 3 Rover</option>
  <option value="570" <?php echo ($row["Antenna"]=="570"?"selected":"");  ?>>Zephyr 3 Base</option>
  <option value="146" <?php echo ($row["Antenna"]=="146"?"selected":"");  ?>>R10</option>
</select>
</td></tr>

<tr><td>
Antenna Height:
</td><td>
<input name="Ant_Height" type="number" min="-.1" max="4" step="0.001" value="<?php echo ($row["Ant_Height"])?$row["Ant_Height"]:"0"; echo ($Editing)?"":"0"?>">
</td></tr>

<tr><td>
Measurement Method:
</td><td>
<select required name="Measurement_Method">
  <option value="APC" <?php echo ($row["Measurement_Method"]=="APC"?"selected":""); ?>>APC</option>
  <option value="ARP" <?php echo ($row["Measurement_Method"]=="ARP"?"selected":""); echo ($Editing?"":"selected") ?>>ARP</option>
</select>
</td></tr>

<tr><td>
Point Name:
</td><td>
<input name="Ref_Name" type="text" size="20" maxlength="16" value="<?php echo $row["Ref_Name"]?$row["Ref_Name"]:"Pt Name" ?>"/>
</td></tr>

<tr><td>
Point Code:
</td><td>
<input name="Ref_Code" type="text" size="40" maxlength="40" value="<?php echo $row["Ref_Code"]?$row["Ref_Code"]:"" ?>"/>
</td></tr>


<tr><td>
Latitude:
</td><td>
<input name="Ref_Lat" type="text" value="<?php echo $row["Ref_Lat"]?$row["Ref_Lat"]:"40.295269094" ?>"/>
</td></tr>

<tr><td>
Latitude:
</td><td>
<input name="Ref_Long" type="text" value="<?php echo $row["Ref_Lat"]?$row["Ref_Long"]:"-104.997829081" ?>"/>
</td></tr>

<tr><td>
Mark Height:
</td><td>
<input name="Ref_Height" type="text" value="<?php echo $row["Ref_Height"]?$row["Ref_Height"]:"1486.972" ?>"/>
</td></tr>
</table>


<p/>

<table>
<tr><caption>Logging</caption>
<tr><td>
Enabled:
</td><td>
<input name="Logging_Enabled" type="checkbox" <?php echo ($row["Logging_Enabled"]==1?"checked":""); echo ($Editing?"":"checked")?>/>
</td></tr>

<tr><td>
Duration:
</td><td>
<input name="Logging_Duration" type="number" min="1" max="1440" step="1" value="<?php echo ($row["Logging_Duration"])?$row["Logging_Duration"]:60 ?>" />
</td></tr>

<tr><td>
Measurement Rate:
</td><td>
<input name="Logging_Measurement_Interval" type="text" value="<?php echo $row["Logging_Measurement_Interval"]?$row["Logging_Measurement_Interval"]:1 ?>"/>
</td></tr>

<tr><td>
Pos Rate:
</td><td>
<input name="Logging_Position_Interval" type="text" value="<?php echo $row["Logging_Position_Interval"]?$row["Logging_Position_Interval"]:1 ?>" />
</td></tr>
</table>

<p/>

<table>
<tr><caption>FTP</caption>
<tr><td>
Enabled:
</td><td>
<input name="FTP_Enabled" type="checkbox" <?php echo ($row["FTP_Enabled"]==1?"checked":"") ?>/>
</td></tr>

<tr><td>
FTP To:
</td><td>
<input name="FTP_To" type="text" size="40" value=" <?php echo ($Editing?$row["FTP_To"]:"/TCC/BTN/gnsstransfer") ?>"/>
</td></tr>
</table>

<p/>

<table>
<tr><caption>Email</caption>
<tr><td>
Enabled:
</td><td>
<input name="Email_Enabled" type="checkbox" <?php echo ($row["Email_Enabled"]==1?"checked":"") ?>/>
</td></tr>

<tr><td>
Email To:
</td><td>
<input name="Email_To" type="text" size="50" value="<?php echo ($Editing?$row["Email_To"]:"Geoffrey_Kirk@Trimble.com") ?>"/>

</td></tr>
</table>

<p/>


<table>
<tr><caption>Timed Options</caption>
<tr><td>
Enabled:
</td><td>
<input name="Timed_Enabled" type="checkbox" <?php echo ($row["TIMED_ACTIVE"]==1?"checked":"") ?>/>
</td></tr>

<tr><td>
Minimum:
</td><td>
<input name="Timed_Minimum" type="number" size="10" value="<?php echo ($Editing?$row["TIMED_MIN_DELTA"]:"30") ?>"/>
</td></tr>

<tr><td>
Maximum:
</td><td>
<input name="Timed_Maximum" type="number" size="10" value="<?php echo ($Editing?$row["TIMED_MAX_DELTA"]:"120") ?>"/>
</td></tr>
</table>
<p/>


<table>
<tr><caption>Radio</caption>
<tr><td>
Check:
</td><td>
<input name="Radio_Enabled" type="checkbox" <?php echo ($row["RadioEnabled"]==1?"checked":""); echo ($Editing?"":"checked") ?>/>
</td></tr>


<tr><td>
On:
</td><td>
<input name="RadioOnOffState" type="checkbox" size="10" <?php echo ($row["RadioOnOffState"]==1?"checked":""); echo ($Editing?"":"checked") ?>/>
</td></tr>

<tr><td>
Operation Mode:
</td><td>
<select required name="RadioMode">
  <option value="Base" <?php echo ($row["RadioMode"]=="Base"?"selected":""); ?>>Base</option>
  <option value="Rover" <?php echo ($row["RadioMode"]=="Rover"?"selected":""); echo ($Editing?"":"selected") ?>>Rover</option>
  <option value="Repeater" <?php echo ($row["RadioMode"]=="Repeater"?"selected":""); ?>>Repeater</option>
</select>

</td></tr>
</table>
<p/>


<!--

<table>
<tr><caption>NTRIP Caster</caption>
<tr><td>
Enabled
</td><td>
<input name="NTRIP_Enabled" type="checkbox" <?php echo ($row["NTRIP_Enabled"]==1?"checked":"") ?>/>
</td></tr>

<tr><td>
Mount 1
</td><td>
<input name="NTRIP1_Mount" type="text" value="<?php echo $row["NTRIP_1_Mount"]?$row["NTRIP_1_Mount"]:"CMRx" ?>"/>
</td></tr>
<tr><td>
Type 1
</td><td>
<select required name="NTRIP1">
  <option value="OFF" <?php echo ($row["NTRIP_1_Type"]=="OFF")?"selected":"" ?>>OFF</option>
  <option value="CMR" <?php echo ($row["NTRIP_1_Type"]=="CMR")?"selected":"" ?>>CMR</option>
  <option value="CMRp" <?php echo ($row["NTRIP_1_Type"]=="CMRp")?"selected":"" ?>>CMR+</option>
  <option value="CMRx" <?php echo ($row["NTRIP_1_Type"]=="CMRx")?"selected":"" ?> <?php echo ($Editing?"":"selected") ?>>CMRx</option>
  <option value="DGPS" <?php echo ($row["NTRIP_1_Type"]=="DGPS")?"selected":"" ?>>DGPS</option>
</select>
</td></tr>

<tr><td>
Mount 2
</td><td>
<input name="NTRIP2_Mount" type="text" value="<?php echo $row["NTRIP_2_Mount"]?$row["NTRIP_2_Mount"]:"CMR" ?>"/>
</td></tr>
<tr><td>
Type 2
</td><td>
<select required name="NTRIP2">
  <option value="OFF" <?php echo ($row["NTRIP_2_Type"]=="OFF")?"selected":"" ?>>OFF</option>
  <option value="CMR" <?php echo ($row["NTRIP_2_Type"]=="CMR")?"selected":"" ?>>CMR</option>
  <option value="CMRp" <?php echo ($row["NTRIP_2_Type"]=="CMRp")?"selected":"" ?> <?php echo ($Editing?"":"selected") ?>>CMR+</option>
  <option value="CMRx" <?php echo ($row["NTRIP_2_Type"]=="CMRx")?"selected":"" ?>>CMRx</option>
  <option value="DGPS" <?php echo ($row["NTRIP_2_Type"]=="DGPS")?"selected":"" ?>>DGPS</option>
</select>
</td></tr>

<tr><td>
Mount 3
</td><td>
<input name="NTRIP3_Mount" type="text" value="<?php echo $row["NTRIP_3_Mount"]?$row["NTRIP_3_Mount"]:"DGPS" ?>"/>
</td></tr>
<tr><td>
Type 3
</td><td>
<select required name="NTRIP3">
  <option value="OFF" <?php echo ($row["NTRIP_3_Type"]=="OFF")?"selected":"" ?>>OFF</option>
  <option value="CMR" <?php echo ($row["NTRIP_3_Type"]=="CMR")?"selected":"" ?>>CMR</option>
  <option value="CMRp" <?php echo ($row["NTRIP_3_Type"]=="CMRp")?"selected":"" ?>>CMR+</option>
  <option value="CMRx" <?php echo ($row["NTRIP_3_Type"]=="CMRx")?"selected":"" ?>>CMRx</option>
  <option value="DGPS" <?php echo ($row["NTRIP_3_Type"]=="DGPS")?"selected":"" ?> <?php echo ($Editing?"":"selected")?>>DGPS</option>
</select>
</td></tr>
</table>

<p/>

<table>
<tr><caption>IBSS Client</caption>
<tr><td>
Enabled
</td><td>
<input name="IBSS_Enabled" type="checkbox" <?php echo ($row["IBSS_Enabled"]==1?"checked":"") ?>/>
</td></tr>

<tr><td>
Organisation
</td><td>
<input name="IBSS_Org" type="text" value="<?php echo $row["IBSS_Org"] ?>"/>
</td></tr>

<tr><td>
Test User
</td><td>
<input name="IBSS_Test_User" type="text"  value="<?php echo $row["IBSS_Test_User"] ?>"/>
</td></tr>

<tr><td>
Test Password
</td><td>
<input name="IBSS_Test_Password" type="type" value="<?php echo $row["IBSS_Test_Password"] ?>"/>
</td></tr>

<tr><td>
Mount 1
</td><td>
<input name="IBSS1_Mount" type="text" value="<?php echo $row["IBSS1_Mount"] ?>"/>
</td></tr>
<tr><td>
Type 1
</td><td>
<select required name="IBSS_1_Type">
  <option value="OFF" <?php echo ($row["IBSS_1_Type"]=="OFF")?"selected":"" ?>>OFF</option>
  <option value="CMR" <?php echo ($row["IBSS_1_Type"]=="CMR")?"selected":"" ?>>CMR</option>
  <option value="CMRp" <?php echo ($row["IBSS_1_Type"]=="CMRp")?"selected":"" ?>>CMR+</option>
  <option value="CMRx" <?php echo ($row["IBSS_1_Type"]=="CMRx")?"selected":"" ?>>CMRx</option>
</select>
</td></tr>
-->


<!--
<tr><td>
Mount 2
</td><td>
<input name="IBSS2_Mount" type="text"/>
</td></tr>
<tr><td>
Type 2
</td><td>
<select required name="IBSS2">
  <option value="OFF">OFF</option>
  <option value="CMR">CMR</option>
  <option value="CMRp" selected>CMR+</option>
  <option value="CMRx">CMRx</option>
</select>
</td></tr>

<tr><td>
Mount 3
</td><td>
<input name="IBSS3_Mount" type="text"/>
</td></tr>
<tr><td>
Type 3
</td><td>
<select required name="IBSS3">
  <option value="OFF">OFF</option>
  <option value="CMR">CMR</option>
  <option value="CMRp" selected>CMR+</option>
  <option value="CMRx">CMRx</option>
</select>
</td></tr>
-->
</table>
<p/>

<?php
if ($Editing && !$DUP) {
   echo '<input type="submit" value="Edit GNSS Receiver" autofocus/>';
   }
else {
   echo '<input type="submit" value="Add a GNSS Receiver" />';
   }
echo '<p/>';

echo '<a href="Receiver_List.php?User_ID='. $_REQUEST["User_ID"].'">Back</a>';

if ($Editing) {
   $db->close();
   }
?>

</form>
</div>
</div>
</div>
</body>
</html>
