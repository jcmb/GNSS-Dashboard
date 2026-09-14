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
table.tablesorter th.radio-mhz-col,
table.tablesorter td.radio-mhz-col {
    min-width: 11ch;
    white-space: nowrap;
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
   error_reporting(E_ALL);
   include 'error.php.inc';
   include 'db.inc.php';
   include 'security.inc.php';

   $user_id = gnss_require_user_id(gnss_open_db());
   echo '<input name="User_ID" type="hidden" value="'.h($user_id).'">';
?>


<?php


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
       return 48;
   }


   function gnss_wireless_modes_sorted($modes)
   {
       uasort($modes, function ($a, $b) {
           return strcasecmp($a, $b);
       });
       return $modes;
   }


   function gnss_radio_wireless_modes()
   {
       $paths = array(
           '/usr/lib/cgi-bin/Dashboard/radio_wireless_modes.json',
           __DIR__ . '/radio_wireless_modes.json',
       );
       foreach ($paths as $path) {
           if (is_readable($path)) {
               $raw = json_decode(file_get_contents($path), true);
               if (is_array($raw)) {
                   return gnss_wireless_modes_sorted($raw);
               }
           }
       }
       return array();
   }


   function radio_mode_display($mode)
   {
       if ($mode === "RadioModeBase" || $mode === "RadioModeBaseW4Repeater") {
           return "Base w/ 4 Repeaters";
       }
       $labels = array(
           "RadioModeBaseW0Repeater" => "Base w/ 0 Repeaters",
           "RadioModeBaseW1Repeater" => "Base w/ 1 Repeater",
           "RadioModeBaseW2Repeater" => "Base w/ 2 Repeaters",
           "RadioModeRover" => "Rover",
           "RadioModeRepeater1" => "Repeater 1",
           "RadioModeRepeater2" => "Repeater 2",
           "RadioModeRepeater3" => "Repeater 3",
           "RadioModeRepeater4" => "Repeater 4",
       );
       return isset($labels[$mode]) ? $labels[$mode] : (string)$mode;
   }


   function radio_issue_class($row)
   {
       if (empty($row["RadioEnabled"])) {
           return "";
       }
       if (!array_key_exists("Radio_Valid", $row) || $row["Radio_Valid"] === null) {
           return "";
       }
       if ((int)$row["Radio_Valid"] === 1) {
           return "";
       }
       return ' class="Issue"';
   }


   function radio_band_value($row)
   {
       $band = !empty($row["RadioBand"]) ? $row["RadioBand"] : "900";
       if ($band === "450" || $band === "900") {
           return $band;
       }
       if (!empty($row["Radio"])) {
           if (strpos($row["Radio"], "(450)") !== false) {
               return "450";
           }
           if (strpos($row["Radio"], "(900)") !== false) {
               return "900";
           }
       }
       if (!empty($row["RadioFrequency"])) {
           return "450";
       }
       if (!empty($row["RadioNetworkNumber"])) {
           return "900";
       }
       return "900";
   }


   function radio_channel_display($row, $band)
   {
       if ($band === "900") {
           $net = isset($row["RadioNetworkNumber"]) ? $row["RadioNetworkNumber"] : "";
           return ($net !== "" && $net !== null) ? (string)$net : "";
       }
       if ($band === "450") {
           $freq = isset($row["RadioFrequency"]) ? $row["RadioFrequency"] : "";
           return ($freq !== "" && $freq !== null) ? $freq . " MHz" : "";
       }
       return "";
   }


   function gnss_radio_wireless_mode_xml_names()
   {
       $paths = array(
           '/usr/lib/cgi-bin/Dashboard/radio_wireless_mode_xml_names.json',
           __DIR__ . '/radio_wireless_mode_xml_names.json',
       );
       foreach ($paths as $path) {
           if (is_readable($path)) {
               $raw = json_decode(file_get_contents($path), true);
               if (is_array($raw)) {
                   return $raw;
               }
           }
       }
       return array();
   }


   function radio_wireless_display($mode_id, $modes, $xml_names = array())
   {
       if ($mode_id === null || $mode_id === "") {
           return "";
       }
       $key = (string)(int)$mode_id;
       if (!empty($xml_names) && isset($xml_names[$key])) {
           return $xml_names[$key];
       }
       if (isset($modes[$key])) {
           return $modes[$key];
       }
       return (string)$mode_id;
   }


   function radio_disabled_cells()
   {
       echo "\n<td> Disabled </td>";
       echo "\n<td>&nbsp;</td>";
       echo "\n<td>&nbsp;</td>";
       echo "\n<td>&nbsp;</td>";
       echo "\n<td class=\"radio-mhz-col\">&nbsp;</td>";
       echo "\n<td>&nbsp;</td>";
   }


   function radio_status_cells($row, $wireless_modes, $wireless_xml_names)
   {
       $issue = radio_issue_class($row);
       $band = radio_band_value($row);

       echo "\n<td" . $issue . "> " . h(isset($row["Radio"]) ? $row["Radio"] : "") . " </td>";
       echo "\n<td" . $issue . "> " . h($band) . " </td>";
       echo "\n<td" . $issue . "> " . h(radio_mode_display(isset($row["RadioMode"]) ? $row["RadioMode"] : "")) . " </td>";
       echo "\n<td" . $issue . "> " . (!empty($row["RadioOnOffState"]) ? "On" : "Off") . " </td>";
       echo "\n<td" . $issue . " class=\"radio-mhz-col\"> " . h(radio_channel_display($row, $band)) . " </td>";

       if ($band === "450") {
           echo "\n<td" . $issue . "> " . h(radio_wireless_display(isset($row["RadioWirelessMode"]) ? $row["RadioWirelessMode"] : "", $wireless_modes, $wireless_xml_names)) . " </td>";
       } else {
           echo "\n<td>&nbsp;</td>";
       }
   }


   function status_row_pad_columns($emitted_cell_count)
   {
       $need = status_table_column_count() - $emitted_cell_count;
       if ($need > 0) {
           echo str_repeat("\n<td>&nbsp;</td>", $need);
       }
   }


   function gnss_distinct_groups($db, $user_id)
   {
       $groups = array();
       $stmt = $db->prepare('SELECT DISTINCT Loc_Group FROM GNSS WHERE User_ID=? ORDER BY Loc_Group COLLATE NOCASE');
       $stmt->bindValue(1, $user_id, SQLITE3_INTEGER);
       $result = $stmt->execute();
       if ($result) {
           while ($row = $result->fetchArray(SQLITE3_ASSOC)) {
               $groups[] = $row["Loc_Group"] !== null ? $row["Loc_Group"] : "";
           }
       }
       return $groups;
   }


   function gnss_group_filter_value()
   {
       if (!isset($_REQUEST["Group"])) {
           return "*";
       }
       return (string)$_REQUEST["Group"];
   }


   function gnss_show_disabled_filter_value()
   {
       return isset($_REQUEST["ShowDisabled"]) && $_REQUEST["ShowDisabled"] === "1";
   }


   function display_status_filters($user_id, $groups, $group_selected, $show_disabled)
   {
       echo '<form method="get" style="margin-bottom: 1em;">';
       echo '<input type="hidden" name="User_ID" value="' . h($user_id) . '">';
       echo '<label for="group-filter">Group: ';
       echo '<select name="Group" id="group-filter" onchange="this.form.submit()">';
       echo '<option value="*"' . ($group_selected === "*" ? ' selected' : '') . '>All groups</option>';
       $has_empty = false;
       foreach ($groups as $group) {
           if ($group === "") {
               $has_empty = true;
               continue;
           }
           $is_selected = $group_selected === (string)$group;
           echo '<option value="' . h($group) . '"' . ($is_selected ? ' selected' : '') . '>' . h($group) . '</option>';
       }
       if ($has_empty) {
           $is_selected = $group_selected === "";
           echo '<option value=""' . ($is_selected ? ' selected' : '') . '>(no group)</option>';
       }
       echo '</select></label> ';
       echo '<label for="show-disabled">';
       echo '<input type="checkbox" name="ShowDisabled" id="show-disabled" value="1"' . ($show_disabled ? ' checked' : '') . ' onchange="this.form.submit()"> ';
       echo 'Show disabled receivers</label>';
       echo '</form>';
   }


   function gnss_status_query_sql($group_filter, $show_disabled)
   {
       $where = "GNSS.User_ID=?";
       if ($group_filter !== "*") {
           if ($group_filter === "") {
               $where .= " AND (GNSS.Loc_Group IS NULL OR GNSS.Loc_Group=?)";
           } else {
               $where .= " AND GNSS.Loc_Group=?";
           }
       }
       if (!$show_disabled) {
           $where .= " AND GNSS.Enabled=1";
       }
       return 'SELECT STATUS.*, GNSS.Loc_Group, GNSS.Name, GNSS.User_ID, GNSS.Address, GNSS.Port, GNSS.UseHTTPS, GNSS.RadioEnabled, GNSS.RadioOnOffState, GNSS.RadioMode, GNSS.RadioBand, GNSS.RadioNetworkNumber, GNSS.RadioFrequency, GNSS.RadioWirelessMode FROM STATUS INNER JOIN GNSS ON GNSS.id = STATUS.id WHERE ' . $where . ' ORDER BY GNSS.Name';
   }


   function gnss_bind_status_query($stmt, $user_id, $group_filter)
   {
       $stmt->bindValue(1, $user_id, SQLITE3_INTEGER);
       if ($group_filter !== "*") {
           $stmt->bindValue(2, $group_filter, SQLITE3_TEXT);
       }
   }


   function displayStatus($result, $user_id)
   {
       $wireless_modes = gnss_radio_wireless_modes();
       $wireless_xml_names = gnss_radio_wireless_mode_xml_names();

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
          "\n<th>SysLog Changed</th>" .
          "\n<th>FTP</th>" .
          "\n<th>Radio</th>" .
          "\n<th>Band</th>" .
          "\n<th>Radio Mode</th>" .
          "\n<th>Radio On</th>" .
          "\n<th class=\"radio-mhz-col\">Net / MHz</th>" .
          "\n<th>Wireless</th>" .
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

     while ($row = $result->fetchArray(SQLITE3_ASSOC))
        {
//        var_dump($row);
//        echo "<hr>";
        // ... start a TABLE row ...
        echo "\n<tr data-group=\"" . h(isset($row["Loc_Group"]) ? $row["Loc_Group"] : "") . "\">";

        // ... and print out each of the attributes
        // in that row as a separate TD (Table Data).
       echo '<td><a target="_blank" href="/Dashboard/Edit_GNSS.php?GNSS_ID='.h($row["id"]).'&User_ID='. h($user_id).'">Edit</a></td>';
       echo "\n<td> ".h($row["id"])." </td>";
       echo "\n<td> ".h($row["name"])." </td>";
       echo "\n<td> ".$row["SystemName"]." </td>";
       echo "\n<td> ".$row["Loc_Group"]." </td>";
       echo "\n<td> <a target=\"_blank\" href=\"".h(gnss_receiver_url($row["Address"], $row["Port"], $row["UseHTTPS"] ?? false))."\"> ".h($row["Address"]).":".h($row["Port"])." </a></td>";

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
       echo "\n<td " . ($row["Firmware_Valid"]?"":"class=\"Issue\"") . " > ".$row["Firmware_Version"]." </td>";

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
          case "112":
            echo "Ag542";
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
            echo "MP86";
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
            echo "MP86";
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
          case "758":
            echo "R780-2";
            break;
          case "721":
            echo "R780";
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

       $syslog_issue = "";
       if (array_key_exists("SysLog_Valid", $row) && $row["SysLog_Valid"] !== null && (int)$row["SysLog_Valid"] !== 1) {
           $syslog_issue = ' class="Issue"';
       }
       $syslog_changed = "";
       if (!empty($row["SysLog_Length_Changed"])) {
           $syslog_changed = $row["SysLog_Length_Changed"];
       }
       echo "\n<td" . $syslog_issue . "> " . h($syslog_changed) . " </td>";

       if ($row["FTP_Enabled"] == 0 ) {
           echo "\n<td " . ($row["FTP_Valid"]?"":"class=\"Issue\"") . " > Disabled </td>";
           }
        else {
           echo "\n<td " . ($row["FTP_Valid"]?"":"class=\"Issue\"") . " > ".$row["FTP_To"]." </td>";
           }

       if (empty($row["RadioEnabled"])) {
           radio_disabled_cells();
       } else {
           radio_status_cells($row, $wireless_modes, $wireless_xml_names);
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

$db = gnss_open_db();

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
$group_filter = gnss_group_filter_value();
$show_disabled = gnss_show_disabled_filter_value();
$groups = gnss_distinct_groups($db, $user_id);
display_status_filters($user_id, $groups, $group_filter, $show_disabled);

$stmt = $db->prepare(gnss_status_query_sql($group_filter, $show_disabled));
gnss_bind_status_query($stmt, $user_id, $group_filter);
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

</form>

</div>
</div>
</div>

</html>
