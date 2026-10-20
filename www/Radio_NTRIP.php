<html>
<head>
<title>Radio &amp; NTRIP Configuration</title>
<link rel="stylesheet" type="text/css" href="/Dashboard/style.css"></link>
<link rel="stylesheet" type="text/css" href="/Dashboard/tcui-styles.css">
<script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
<body class="page">
<div class="container clearfix">
  <div style="padding: 10px 10px 10px 0 ;"> <a href="http://construction.trimble.com/">
        <img src="/Dashboard/trimble-logo.png" alt="Trimble Logo" id="logo"> </a>
      </div>
</div>
<div id="content-area">
<div id="content">
<div id="main-content" class="clearfix">

<style>
table.tablesorter tbody td.Issue,
table.radio-ntrip .Issue {
    color: red;
}
table.radio-ntrip td.td_header,
table.radio-ntrip th.td_header {
    background: #d0d0d0;
    font-weight: bold;
}
table.radio-ntrip td.td_subheader {
    background: #e8e8e8;
    font-weight: bold;
}
h2.section-title {
    margin-top: 1.5em;
}
</style>
</head>
<body>
<H1>Radio &amp; NTRIP Configuration</H1>

<?php
   include 'error.php.inc';
   include 'db.inc.php';
   include 'security.inc.php';
   include 'radio_ntrip_helpers.inc.php';

   $db = gnss_open_db();
   $user_id = gnss_require_user_id($db);
   rn_ensure_status_live_columns($db);
   $wireless_modes = rn_load_wireless_modes();
   $wireless_xml_names = rn_load_wireless_xml_names();

   $sql = 'SELECT GNSS.*, STATUS.Radio, STATUS.Radio_Valid,
           STATUS.Radio_Live_OnOff, STATUS.Radio_Live_Mode, STATUS.Radio_Live_Band,
           STATUS.Radio_Live_NetworkNumber, STATUS.Radio_Live_Frequency,
           STATUS.Radio_Live_WirelessMode, STATUS.Radio_Live_ChanSpacing,
           STATUS.NTRIP_Valid,
           STATUS.NTRIP_Client_1_Live_Enabled, STATUS.NTRIP_Client_1_Live_Mount,
           STATUS.NTRIP_Client_2_Live_Enabled, STATUS.NTRIP_Client_2_Live_Mount,
           STATUS.NTRIP_Client_3_Live_Enabled, STATUS.NTRIP_Client_3_Live_Mount,
           STATUS.NTRIP_Server_1_Live_Enabled, STATUS.NTRIP_Server_1_Live_Mount, STATUS.NTRIP_Server_1_Live_Format,
           STATUS.NTRIP_Server_2_Live_Enabled, STATUS.NTRIP_Server_2_Live_Mount, STATUS.NTRIP_Server_2_Live_Format,
           STATUS.NTRIP_Server_3_Live_Enabled, STATUS.NTRIP_Server_3_Live_Mount, STATUS.NTRIP_Server_3_Live_Format,
           STATUS.NTRIP_Caster_1_Live_Enabled, STATUS.NTRIP_Caster_1_Live_Mount, STATUS.NTRIP_Caster_1_Live_Format,
           STATUS.NTRIP_Caster_2_Live_Enabled, STATUS.NTRIP_Caster_2_Live_Mount, STATUS.NTRIP_Caster_2_Live_Format,
           STATUS.NTRIP_Caster_3_Live_Enabled, STATUS.NTRIP_Caster_3_Live_Mount, STATUS.NTRIP_Caster_3_Live_Format
           FROM GNSS LEFT JOIN STATUS ON GNSS.id = STATUS.id
           WHERE GNSS.User_ID=?
           ORDER BY GNSS.Loc_Group COLLATE NOCASE, GNSS.name COLLATE NOCASE';
   $stmt = $db->prepare($sql);
   $stmt->bindValue(1, $user_id, SQLITE3_INTEGER);
   $result = $stmt->execute();

   $rows = array();
   if ($result) {
       while ($row = $result->fetchArray(SQLITE3_ASSOC)) {
           $rows[] = $row;
       }
   }

   $name_index = array();
   foreach ($rows as $row) {
       $name_index[(string)$row["name"]] = $row;
   }

   // ---- Radio section: group by Loc_Group, then by expected channel key ----
   $radio_by_group = array();
   foreach ($rows as $row) {
       if (empty($row["RadioEnabled"])) {
           continue;
       }
       $group = isset($row["Loc_Group"]) ? (string)$row["Loc_Group"] : "";
       $key = rn_channel_key($row);
       if (!isset($radio_by_group[$group])) {
           $radio_by_group[$group] = array();
       }
       if (!isset($radio_by_group[$group][$key])) {
           $radio_by_group[$group][$key] = array("base" => array(), "others" => array(), "sample" => $row);
       }
       if (rn_is_base_mode(isset($row["RadioMode"]) ? $row["RadioMode"] : "")) {
           $radio_by_group[$group][$key]["base"][] = $row;
       } else {
           $radio_by_group[$group][$key]["others"][] = $row;
       }
   }

   echo '<h2 class="section-title">Radio configurations</h2>';
   echo '<p>Live values from the last status check. Values that differ from the configured expectation are shown in red.</p>';

   if (count($radio_by_group) === 0) {
       echo "<p>No radio-enabled receivers.</p>";
   } else {
       echo "\n<table border='1' class='tablesorter radio-ntrip'>\n";
       echo "<thead><tr>";
       echo "<th>Edit</th><th>Name</th><th>Role</th><th>On/Off</th><th>Mode</th><th>Band</th><th>Channel / Network</th><th>Wireless</th>";
       echo "</tr></thead>\n<tbody>\n";

       foreach ($radio_by_group as $group => $clusters) {
           $group_label = ($group === "") ? "(ungrouped)" : $group;
           echo "\n<tr><td colspan=\"8\" class=\"td_header\">Group: " . h($group_label) . "</td></tr>\n";

           foreach ($clusters as $key => $cluster) {
               $sample = $cluster["sample"];
               $bases = $cluster["base"];
               $others = $cluster["others"];
               $chan_label = rn_channel_key_label($sample, $wireless_modes, $wireless_xml_names);

               if (count($bases) > 0) {
                   $base_names = array();
                   foreach ($bases as $b) {
                       $base_names[] = $b["name"];
                   }
                   $header = "Base: " . implode(", ", $base_names) . " — " . $chan_label;
               } else {
                   $header = "No base on channel — " . $chan_label;
               }
               echo "\n<tr><td colspan=\"8\" class=\"td_subheader\">" . h($header) . "</td></tr>\n";

               foreach ($bases as $b) {
                   rn_emit_radio_row($b, $user_id, $wireless_modes, $wireless_xml_names);
               }
               foreach ($others as $o) {
                   rn_emit_radio_row($o, $user_id, $wireless_modes, $wireless_xml_names);
               }
           }
       }
       echo "</tbody></table>\n";
   }

   // ---- NTRIP section: mount topology ----
   echo '<h2 class="section-title">NTRIP connections</h2>';
   echo '<p>What is connected to what by mountpoint. Live mount/enabled/format shown; mismatches vs configured values are red. Mounts ending in <code>__wm_IBSS</code> are IBSS 3rd-party shares.</p>';

   $mounts = array(); // mount => array(producers => [], consumers => [], ibss => bool, ibss_base => ?)

   foreach ($rows as $row) {
       foreach (rn_ntrip_slot_defs() as $slot) {
           if (empty($row[$slot["en"]])) {
               continue;
           }
           $expected_mount = isset($row[$slot["mount"]]) ? (string)$row[$slot["mount"]] : "";
           if ($expected_mount === "") {
               continue;
           }
           if (!isset($mounts[$expected_mount])) {
               $ibss_base = rn_ibss_base_name($expected_mount);
               $mounts[$expected_mount] = array(
                   "producers" => array(),
                   "consumers" => array(),
                   "ibss" => ($ibss_base !== null),
                   "ibss_base" => $ibss_base,
               );
           }
           $entry = array(
               "row" => $row,
               "slot" => $slot,
               "expected_mount" => $expected_mount,
               "expected_format" => ($slot["format"] !== null && isset($row[$slot["format"]])) ? (string)$row[$slot["format"]] : "",
           );
           if ($slot["kind"] === "client") {
               $mounts[$expected_mount]["consumers"][] = $entry;
           } else {
               $mounts[$expected_mount]["producers"][] = $entry;
           }
       }
   }

   ksort($mounts, SORT_NATURAL | SORT_FLAG_CASE);

   if (count($mounts) === 0) {
       echo "<p>No enabled NTRIP slots.</p>";
   } else {
       echo "\n<table border='1' class='tablesorter radio-ntrip'>\n";
       echo "<thead><tr><th>Mount</th><th>Notes</th><th>Producers (Server/Caster)</th><th>Consumers (Client)</th></tr></thead>\n<tbody>\n";

       foreach ($mounts as $mount => $info) {
           $notes = array();
           if ($info["ibss"]) {
               $notes[] = "IBSS 3rd-party share";
               $base = $info["ibss_base"];
               if ($base !== null && $base !== "") {
                   if (isset($name_index[$base])) {
                       $notes[] = "Base: " . $base;
                   } else {
                       $notes[] = "Base name: " . $base . " (not in list)";
                   }
               }
           }
           if (count($info["producers"]) === 0) {
               $notes[] = "No producer in dashboard";
           }
           if (count($info["consumers"]) === 0) {
               $notes[] = "No client in dashboard";
           }

           $prod_html = array();
           foreach ($info["producers"] as $p) {
               $prod_html[] = rn_ntrip_endpoint_cells($p);
           }
           $cons_html = array();
           foreach ($info["consumers"] as $c) {
               $cons_html[] = rn_ntrip_endpoint_cells($c);
           }

           echo "\n<tr>";
           echo "\n<td>" . h($mount) . "</td>";
           echo "\n<td>" . h(implode("; ", $notes)) . "</td>";
           echo "\n<td>" . (count($prod_html) ? implode("<br/>", $prod_html) : "&nbsp;") . "</td>";
           echo "\n<td>" . (count($cons_html) ? implode("<br/>", $cons_html) : "&nbsp;") . "</td>";
           echo "\n</tr>";
       }
       echo "</tbody></table>\n";
   }

   if (!($db->close())) {
       showerror();
   }
?>

<p/>
<?php
if ($user_id) {
    echo 'View <a href="Receiver_List.php?User_ID=' . h($user_id) . '">Receiver List</a>';
    echo ' | ';
    echo '<a href="/cgi-bin/Dashboard/List_Status.php?User_ID=' . h($user_id) . '">Receiver Status</a>';
}
?>

</div>
</div>
</div>

</html>
