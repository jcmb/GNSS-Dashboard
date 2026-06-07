<html>
<head>
<title>GNSS Receivers</title>
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



<style>

table.tablesorter tbody td.Issue {
    color: red;
}
table.tablesorter tbody td.ntrip-ok {
    color: #000;
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
    $user_id = gnss_require_user_id(new SQLite3($databaseFile));
    echo '<input name="User_ID" type="hidden" value="'.h($user_id).'">';
    }
else {
    die ("Internal Error: Missing User ID");
   }
?>


<?php
   error_reporting(E_ALL);
   include 'error.php.inc';
   include 'db.inc.php';
   include 'security.inc.php';


   function ntrip_summary_html($row)
   {
       $parts = array();
       if ((int)$row["NTRIP_Client_1_Enabled"]) {
           $m = isset($row["NTRIP_Client_1_Mount"]) ? $row["NTRIP_Client_1_Mount"] : "";
           $parts[] = "Cl1: " . htmlspecialchars((string)$m, ENT_QUOTES, "UTF-8");
       }
       if ((int)$row["NTRIP_Client_2_Enabled"]) {
           $m = isset($row["NTRIP_Client_2_Mount"]) ? $row["NTRIP_Client_2_Mount"] : "";
           $parts[] = "Cl2: " . htmlspecialchars((string)$m, ENT_QUOTES, "UTF-8");
       }
       if ((int)$row["NTRIP_Client_3_Enabled"]) {
           $m = isset($row["NTRIP_Client_3_Mount"]) ? $row["NTRIP_Client_3_Mount"] : "";
           $parts[] = "Cl3: " . htmlspecialchars((string)$m, ENT_QUOTES, "UTF-8");
       }
       if ((int)$row["NTRIP_Server_1_Enabled"]) {
           $m = isset($row["NTRIP_Server_1_Mount"]) ? $row["NTRIP_Server_1_Mount"] : "";
           $f = isset($row["NTRIP_Server_1_Format"]) ? $row["NTRIP_Server_1_Format"] : "";
           $parts[] = "Sv1: " . htmlspecialchars((string)$m, ENT_QUOTES, "UTF-8") . " (" . htmlspecialchars((string)$f, ENT_QUOTES, "UTF-8") . ")";
       }
       if ((int)$row["NTRIP_Server_2_Enabled"]) {
           $m = isset($row["NTRIP_Server_2_Mount"]) ? $row["NTRIP_Server_2_Mount"] : "";
           $f = isset($row["NTRIP_Server_2_Format"]) ? $row["NTRIP_Server_2_Format"] : "";
           $parts[] = "Sv2: " . htmlspecialchars((string)$m, ENT_QUOTES, "UTF-8") . " (" . htmlspecialchars((string)$f, ENT_QUOTES, "UTF-8") . ")";
       }
       if ((int)$row["NTRIP_Server_3_Enabled"]) {
           $m = isset($row["NTRIP_Server_3_Mount"]) ? $row["NTRIP_Server_3_Mount"] : "";
           $f = isset($row["NTRIP_Server_3_Format"]) ? $row["NTRIP_Server_3_Format"] : "";
           $parts[] = "Sv3: " . htmlspecialchars((string)$m, ENT_QUOTES, "UTF-8") . " (" . htmlspecialchars((string)$f, ENT_QUOTES, "UTF-8") . ")";
       }
       if ((int)$row["NTRIP_Caster_1_Enabled"]) {
           $m = isset($row["NTRIP_Caster_1_Mount"]) ? $row["NTRIP_Caster_1_Mount"] : "";
           $f = isset($row["NTRIP_Caster_1_Format"]) ? $row["NTRIP_Caster_1_Format"] : "";
           $parts[] = "Ca1: " . htmlspecialchars((string)$m, ENT_QUOTES, "UTF-8") . " (" . htmlspecialchars((string)$f, ENT_QUOTES, "UTF-8") . ")";
       }
       if ((int)$row["NTRIP_Caster_2_Enabled"]) {
           $m = isset($row["NTRIP_Caster_2_Mount"]) ? $row["NTRIP_Caster_2_Mount"] : "";
           $f = isset($row["NTRIP_Caster_2_Format"]) ? $row["NTRIP_Caster_2_Format"] : "";
           $parts[] = "Ca2: " . htmlspecialchars((string)$m, ENT_QUOTES, "UTF-8") . " (" . htmlspecialchars((string)$f, ENT_QUOTES, "UTF-8") . ")";
       }
       if ((int)$row["NTRIP_Caster_3_Enabled"]) {
           $m = isset($row["NTRIP_Caster_3_Mount"]) ? $row["NTRIP_Caster_3_Mount"] : "";
           $f = isset($row["NTRIP_Caster_3_Format"]) ? $row["NTRIP_Caster_3_Format"] : "";
           $parts[] = "Ca3: " . htmlspecialchars((string)$m, ENT_QUOTES, "UTF-8") . " (" . htmlspecialchars((string)$f, ENT_QUOTES, "UTF-8") . ")";
       }
       if (count($parts) === 0) {
           return "Disabled";
       }
       return implode("; ", $parts);
   }


   function ntrip_cell_classes($row)
   {
       if (!array_key_exists("NTRIP_Valid", $row) || $row["NTRIP_Valid"] === null) {
           return "";
       }
       if ((int)$row["NTRIP_Valid"] === 1) {
           return ' class="ntrip-ok"';
       }
       return ' class="Issue"';
   }


   /** Must match the number of <th> cells in the status table header row. */
   function status_table_column_count()
   {
       return 41;
   }


   function status_row_pad_columns($emitted_cell_count)
   {
       $need = status_table_column_count() - $emitted_cell_count;
       if ($need > 0) {
           echo str_repeat("\n<td>&nbsp;</td>", $need);
       }
   }


   function displayStatus($result, $user_id)
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
          "\n<th>NTRIP</th>" .
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
       echo '<td><a target="_blank" href="/Dashboard/Edit_GNSS.php?GNSS_ID='.h($row["id"]).'&User_ID='. h($user_id).'">Edit</a></td>';
       echo "\n<td> ".h($row["id"])." </td>";
       echo "\n<td> ".h($row["name"])." </td>";
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
          status_row_pad_columns(7);
          echo "\n</tr>";
          continue;
      }

       echo "\n<td ". ($row["Alive"]?"":"class=\"Issue\"") ."> ".($row["Alive"]?"Up":"Down")." </td>";
       if (! $row["Alive"]) {
          status_row_pad_columns(8);
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
          case "38":
            echo "SPS850";
            break;
          case "59":
            echo "SPS851";
            break;
          case "76":
            echo "NetR9";
            break;
          case "118":
            echo "SPS855";
            break;
          case "107":
            echo "SPS852";
            break;
          case "100":
            echo "R10";
            break;
          case "101":
            echo "SPS985";
            break;
          case "138":
            echo "SPS356";
            break;
          case "162":
            echo "Alloy";
            break;
          case "164":
            echo "BD992-INS";
            break;
          case "169":
            echo "SPS986";
            break;
          case "188":
            echo "R750";
            break;
          case "191":
            echo "R750-2";
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
          case "193":
            echo "MPS566-2";
            break;
          case "327":
            echo "R780";
            break;
          case "329":
            echo "R780-2";
            break;
          case "330":
            echo "MP1086";
            break;
          case "331":
            echo "MS1086";
            break;
          case "509":
            echo "BX992-SPS";
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
            echo "GA530";
            break;
          case "470":
            echo "GA830";
            break;
          case "784":
            echo "MP1086";
            break;
          case "146":
            echo "R10";
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
          case "194":
            echo "GA510";
            break;
          case "265":
            echo "Zephyr 2 Geodetic ROHS";
            break;
          case "512":
            echo "Zephyr 3 Rover";
            break;
          case "513":
            echo "Zephyr 3 Geodetic";
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
       echo "\n<td " . ($row["PDOP_Valid"]?"":"class=\"Issue\"") . " > ".$row["PDOP"]." </td>";
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

       echo "\n<td" . ntrip_cell_classes($row) . "> " . ntrip_summary_html($row) . " </td>";

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

$pragma_cols = $db->query("PRAGMA table_info(STATUS)");
$have_ntrip_valid_col = false;
if ($pragma_cols) {
    while ($col = $pragma_cols->fetchArray(SQLITE3_ASSOC)) {
        if ($col["name"] === "NTRIP_Valid") {
            $have_ntrip_valid_col = true;
            break;
        }
    }
}
if (!$have_ntrip_valid_col) {
    $db->exec("ALTER TABLE STATUS ADD COLUMN NTRIP_Valid BOOLEAN");
}
//$handle = sqlite_open($db) or die("Could not open database");
//if (!(mysql_select_db($databaseName, $connection)))
//  showerror();

// Run the query on the connection

//$query = "SELECT * FROM GNSS WHERE User_ID=" . $_REQUEST["User_ID"];
  $stmt = $db->prepare('SELECT STATUS.*, GNSS.Loc_Group, GNSS.Name, GNSS.User_ID, GNSS.Address, GNSS.Port FROM STATUS INNER JOIN GNSS ON GNSS.id = STATUS.id WHERE User_ID=? order by GNSS.Name');
  $stmt->bindValue(1, $user_id, SQLITE3_INTEGER);
  $result = $stmt->execute();

if (!($result))
  {
  showerror();
  }

   // Display the results
displayStatus($result, $user_id);


  // Close the connection
if (!($db->close()))
  showerror();


?>

<p/>

<?php
if ($user_id) {
    echo 'View <a href="/Dashboard/Receiver_List.php?User_ID='.h($user_id).'">Receiver List</a>';
    }
?>
<br>
<?php
if ($user_id) {
    echo 'View <a href="/Dashboard/Receiver_Upgrade.php?User_ID='.h($user_id).'">Upgrade Firmware</a>';
    }
?>

<br>
<?php
if ($user_id) {
    echo 'View <a href="/Dashboard/Error_List.php?User_ID='.h($user_id).'">Errors and Warnings</a>';
    }
?>

</form>

</div>
</div>
</div>

</html>
