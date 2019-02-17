<html>
<head>
<title>GNSS Receivers</title>
<link rel="stylesheet" type="text/css" href="/style.css"></link>
<link rel="stylesheet" type="text/css" href="/css/tcui-styles.css">
<script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
<script src="/jquery.tablesorter.min.js"></script>
<body class="page">
<div class="container clearfix">
  <div style="padding: 10px 10px 10px 0 ;"> <a href="http://construction.trimble.com/">
        <img src="/images/trimble-logo.png" alt="Trimble Logo" id="logo"> </a>
      </div>
  <!-- end #logo-area -->
</div>
<div id="top-header-trim"></div>
<div id="content-area">
<div id="content">
<div id="main-content" class="clearfix">



<style>

table.tablesorter tbody td.Issue {
    color: red;
}
</style>
<script>
$(document).ready(function()
    {
        $("#Receivers").tablesorter();
    }
);
</script>

</head>
<body>
<H1>GNSS Receivers</H1>

<?php
if ($_REQUEST["User_ID"]) {
    echo '<input name="User_ID" type="hidden" value="'.$_REQUEST["User_ID"] . '">';
    }
else {
    die ("Internal Error: Missing User ID");
//    $_REQUEST["User_ID"]="1";
   }
?>


<?php
   error_reporting(E_ALL);
   include 'error.php.inc';
   include 'db.inc.php';


   function displayStatus($result)
   {
       // Start a table, with column headers

      echo "\n<table id=\"Receivers\" class=\"tablesorter\" border='1'>\n" .
          "<thead>" .
          "\n<tr>" .
          "\n<th>&nbsp;</th>" .
          "\n<th>ID</th>" .
          "\n<th>Name</th>" .
          "\n<th>System Name</th>" .
          "\n<th>Group</th>" .
          "\n<th>IP</th>" .
          "\n<th>Checked</th>" .
          "\n<th>Up</th>" .
          "\n<th>Power</th>" .
          "\n<th>Temp</th>" .
          "\n<th>Uptime (h)</th>" .
          "\n<th>Auth</th>" .
          "\n<th>Serial</th>" .
          "\n<th>Firmware</th>" .
          "\n<th>Type</th>" .
          "\n<th>Antenna</th>" .
          "\n<th>Ant Height</th>" .
          "\n<th>Pos Type</th>" .
          "\n<th>Low Latency</th>" .
          "\n<th>Static</th>" .
          "\n<th>Elev</th>" .
          "\n<th>PDOP</th>" .
          "\n<th>Logging</th>" .
          "\n<th>Email</th>" .
          "\n<th>FTP</th>" .
//          "\n<th>NTRIP</th>" .
//          "\n<th>IBSS</th>" .
          "\n<th>Freq</th>" .
          "\n<th>GPS</th>" .
          "\n<th>GLN</th>" .
          "\n<th>GAL</th>" .
          "\n<th>BDS</th>" .
          "\n<th>QZSS</th>" .
          "\n<th>SBAS</th>" .
          "\n<th>UPS</th>" .
          "\n<th>Clock</th>" .
          "\n<th>Everest</th>" .
          "\n<th>Test Mode</th>" .
          "\n<th>Ref Name</th>" .
          "\n<th>Latitude</th>" .
          "\n<th>Longitude</th>" .
          "\n<th>Height</th>" .
          "\n<th>Ref Code</th>" .
          "\n</tr>".
          "\n</thead>".
          "\n<tbody>";


     // Until there are no rows in the result set,
     // fetch a row into the $row array and ...

     while ($row = @ $result->fetchArray(SQLITE3_ASSOC))
        {
//        var_dump($row);
//        echo "<hr>";
        // ... start a TABLE row ...
        echo "\n<tr>";

        // ... and print out each of the attributes
        // in that row as a separate TD (Table Data).
       echo '<td><a target="_blank" href="/Dashboard/Edit_GNSS.php?GNSS_ID='.$row["id"].'&User_ID='. $_REQUEST["User_ID"].'">Edit</a></td>';
       echo "\n<td> ".$row["id"]." </td>";
       echo "\n<td> ".$row["name"]." </td>";
       echo "\n<td> ".$row["SystemName"]." </td>";
       echo "\n<td> ".$row["Loc_Group"]." </td>";
       echo "\n<td> <a target=\"_blank\" href=\"http://".$row["Address"].":".$row["Port"]."\"> ".$row["Address"].":".$row["Port"]." </a></td>";

       if ($row["Checked"] ){
           echo "\n<td> ". $row["Last_Check"]." </td>";
           }
       else {
          echo "\n<td> Disabled </td>";
          }
       if (! $row["Checked"]) {
          echo "\n</tr>";
          continue;
      }

       echo "\n<td ". ($row["Alive"]?"":"class=\"Issue\"") ."> ".($row["Alive"]?"Up":"Down")." </td>";
       if (! $row["Alive"]) {
          echo "\n</tr>";
          continue;
      }


       echo "\n<td " . ($row["Power_Valid"]?"":"class=\"Issue\"") . " > ".($row["Power_Valid"]?"AC":"Battery")." </td>";


       echo "\n<td> ".$row["Temperature"]." </td>";
       echo "\n<td> ".$row["Uptime"] ." </td>";
       echo "\n<td " . ($row["Auth_Valid"]?"":"class=\"Issue\"") . " > ".$row["Auth"]." </td>";
       echo "\n<td> ".$row["Serial_Number"]." </td>";
       echo "\n<td> ".$row["Firmware_Version"]." </td>";

       echo "\n<td ". ($row["Reciever_Type_Valid"]?"":"class=\"Issue\"")." > ";
       switch ($row["Reciever_Type"]) {
          case "118":
            echo "SPS855";
            break;
          case "107":
            echo "SPS852";
            break;
          case "101":
            echo "SPS985";
            break;
          case "169":
            echo "SPS986";
            break;
          case "138":
            echo "SPS356";
            break;
          case "240":
            echo "BD935";
            break;
          case "248":
            echo "Brewster Upgradable";
            break;
          case "249":
            echo "Brewster Heading";
            break;
          case "38":
            echo "SPS850";
            break;
          case "59":
            echo "SPS851";
            break;

          default:
            echo "Unknown ID ". $row["Reciever_Type"];
       }
       echo " </td>";


       echo "\n<td ". ($row["Antenna_Valid"]?"":"class=\"Issue\"")." > ";
       switch ($row["Antenna"]) {

          case "209":
            echo "Choke";
            break;
          case "85":
            echo "Zephyr";
            break;
          case "86":
            echo "Zephyr Geodetic";
            break;
          case "250":
            echo "GA510";
            break;
          case "470":
            echo "GA830";
            break;
          case "147":
            echo "SPS985";
            break;
          case "569":
            echo "SPS986";
            break;
          case "184":
            echo "Zephyr 2";
            break;
          case "185":
            echo "Zephyr 2 Geodetic";
            break;

          case "512":
            echo "Zephyr 3 Rover";
            break;
          case "570":
            echo "Zephyr 3 Base";
            break;

          default:
            echo "Unknown ID ". $row["Antenna"];
       }
       echo " </td>";

       echo "\n<td " . ($row["Antenna_Valid"]?"":"class=\"Issue\"") . " > ".$row["Ant_Height"]. " (" . $row["Measurement_Method"].") </td>";


       echo "\n<td " . ($row["Pos_Type_Valid"]?"":"class=\"Issue\"") . " > ".$row["Pos_Type"]." </td>";
       echo "\n<td " . ($row["LowLatency_Valid"]?"":"class=\"Issue\"") . " > ".($row["LowLatency"] ? 'True' : 'False')." </td>";
       echo "\n<td " . ($row["Static_Valid"]?"":"class=\"Issue\"") . " > ".($row["Static"] ? 'True' : 'False')." </td>";
       echo "\n<td " . ($row["Elev_Mask_Valid"]?"":"class=\"Issue\"") . " > ".$row["Elev_Mask"]." </td>";
       echo "\n<td " . ($row["Pos_Type_Valid"]?"":"class=\"Issue\"") . " > ".$row["PDOP"]." </td>";
       if ($row["Logging_Enabled"] == 0 ) {
           echo "\n<td " . ($row["Logging_Valid"]?"":"class=\"Issue\"") . " > Disabled </td>";
           }
       else {
           echo "\n<td " . ($row["Logging_Valid"]?"":"class=\"Issue\"") . " > ".$row["Logging_Duration"]."m, ".$row["Logging_Position_Interval"]."s, ".$row["Logging_Measurement_Interval"]."s, " .$row["Logging_Volt_Temp_Interval"]."s </td>";
           }


       if ($row["Email_Enabled"] == 0 ) {
           echo "\n<td " . ($row["Email_Valid"]?"":"class=\"Issue\"") . " > Disabled </td>";
           }
        else {
           echo "\n<td " . ($row["Email_Valid"]?"":"class=\"Issue\"") . " > ".$row["Email_To"]." </td>";
           }

       if ($row["FTP_Enabled"] == 0 ) {
           echo "\n<td " . ($row["FTP_Valid"]?"":"class=\"Issue\"") . " > Disabled </td>";
           }
        else {
           echo "\n<td " . ($row["FTP_Valid"]?"":"class=\"Issue\"") . " > ".$row["FTP_To"]." </td>";
           }

//       echo "\n<td> ".($row["NTRIP_Enabled"] ? 'True' : 'False') ." </td>";
//       echo "\n<td> ".($row["IBSS_Enabled"] ? 'True' : 'False') ." </td>";

       echo "\n<td " . ($row["Frequencies_Valid"]?"":"class=\"Issue\"") . " > ".$row["Frequencies"] ." </td>";
       echo "\n<td " . ($row["GPS_Valid"]?"":"class=\"Issue\"") . " > ".($row["GPS"] ? 'Enabled' : 'Disabled') ." </td>";
       echo "\n<td " . ($row["GLN_Valid"]?"":"class=\"Issue\"") . " > ".($row["GLN"] ? 'Enabled' : 'Disabled') ." </td>";
       echo "\n<td " . ($row["GAL_Valid"]?"":"class=\"Issue\"") . "> ".($row["GAL"] ? 'Enabled' : 'Disabled')." </td>";
       echo "\n<td " . ($row["BDS_Valid"]?"":"class=\"Issue\"") . "> ".($row["BDS"] ? 'Enabled' : 'Disabled')." </td>";
       echo "\n<td " . ($row["QZSS_Valid"]?"":"class=\"Issue\"") . "> ".($row["QZSS"] ? 'Enabled' : 'Disabled')." </td>";
       echo "\n<td " . ($row["SBAS_Valid"]?"":"class=\"Issue\"") . "> ".($row["SBAS"] ? 'Enabled' : 'Disabled')." </td>";
       echo "\n<td " . ($row["UPS_Valid"]?"":"class=\"Issue\"") . "> ".($row["UPS"] ? 'Enabled' : 'Disabled')." </td>";
       echo "\n<td " . ($row["Clock_Valid"]?"":"class=\"Issue\"") . "> ".($row["Clock"] ? 'Steered' : 'Unsteered')." </td>";
       echo "\n<td " . ($row["MultipathReject_Valid"]?"":"class=\"Issue\"") . "> ".($row["MultipathReject"] ? 'Enabled' : 'Disabled')." </td>";
       echo "\n<td " . ($row["testMode_Valid"]?"":"class=\"Issue\"") . "> ".($row["testMode"] ? 'Enabled' : 'Disabled')." </td>";
       echo "\n<td " . ($row["Ref_Valid"]?"":"class=\"Issue\"") . "> ". $row["Ref_Name"] ." </td>";
       echo "\n<td " . ($row["Ref_Valid"]?"":"class=\"Issue\"") . "> ". $row["Ref_Lat"] ." </td>";
       echo "\n<td " . ($row["Ref_Valid"]?"":"class=\"Issue\"") . "> ". $row["Ref_Long"] ." </td>";
       echo "\n<td " . ($row["Ref_Valid"]?"":"class=\"Issue\"") . "> ". $row["Ref_Height"] ." </td>";
       echo "\n<td " . ($row["Ref_Valid"]?"":"class=\"Issue\"") . "> ". $row["Ref_Code"] ." </td>";
       echo "\n</tr>";

     }

     // Then, finish the table
     echo "\n</tbody>\n";
     echo "\n</table>\n";
     echo "<p>\n";
  }


// Connect to sqlite

$db = new SQLite3($databaseFile);

if (! $db) {
   die ("Failed to open GNSS.db");
   }
//$handle = sqlite_open($db) or die("Could not open database");
//if (!(mysql_select_db($databaseName, $connection)))
//  showerror();

// Run the query on the connection

//$query = "SELECT * FROM GNSS WHERE User_ID=" . $_REQUEST["User_ID"];
  $query = "SELECT STATUS.*, GNSS.Loc_Group, GNSS.Name, GNSS.User_ID, GNSS.Address, GNSS.Port FROM STATUS INNER JOIN GNSS ON GNSS.id == STATUS.id WHERE  User_ID=" . $_REQUEST["User_ID"]. " order by GNSS.Name";


$result = $db->query($query);

if (!($result))
  {
  showerror();
  }

   // Display the results
displayStatus($result);


  // Close the connection
if (!($db->close()))
  showerror();


?>

<p/>

<?php
if ($_REQUEST["User_ID"]) {
    echo 'View <a href="/Dashboard/Receiver_List.php?User_ID='.$_REQUEST["User_ID"] . '">Receiver List</a>';
    }
?>
</form>

</div>
</div>
</div>

</html>
