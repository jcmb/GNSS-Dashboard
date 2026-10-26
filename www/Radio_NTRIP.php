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
table.radio-ntrip tr.group-spacer td {
    height: 2em;
    border: none;
    background: transparent;
    padding: 0;
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
           WHERE GNSS.User_ID=? AND GNSS.Enabled=1
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

   // ---- Radio section: group by Loc_Group, then by expected channel key ----
   $radio_by_group = array();
   foreach ($rows as $row) {
       if (empty($row["RadioEnabled"])) {
           continue;
       }
       // Skip radios that are correctly Off (expected Off and live Off).
       if (rn_expected_onoff($row) === "Off" && rn_live_onoff($row) === "Off") {
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

   if (count($radio_by_group) === 0) {
       echo "<p>No radio-enabled receivers.</p>";
   } else {
       echo "\n<table border='1' class='tablesorter radio-ntrip'>\n";
       echo "<thead><tr>";
       echo "<th>Edit</th><th>Name</th><th>Role</th><th>On/Off</th><th>Mode</th><th>Band</th><th>Channel / Network</th><th>Wireless</th>";
       echo "</tr></thead>\n<tbody>\n";

       $radio_group_i = 0;
       foreach ($radio_by_group as $group => $clusters) {
           if ($radio_group_i > 0) {
               echo "\n<tr class=\"group-spacer\"><td colspan=\"8\">&nbsp;</td></tr>\n";
           }
           $radio_group_i++;
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

   // ---- NTRIP section: by producer Loc_Group; clients may be from other groups ----
   echo '<h2 class="section-title">NTRIP connections</h2>';
   echo '<p>Grouped by the producer&rsquo;s group. Clients from other groups still appear under the mount. IBSS shares are labeled Org / Mountpoint; other NTRIP mounts use Server / Mountpoint.</p>';

   // Bases referenced by clients as <Base>__wm_IBSS (case-insensitive name => true).
   $ibss_base_names = array();
   foreach ($rows as $row) {
       foreach (rn_ntrip_slot_defs() as $slot) {
           if ($slot["kind"] !== "client" || empty($row[$slot["en"]])) {
               continue;
           }
           $m = isset($row[$slot["mount"]]) ? (string)$row[$slot["mount"]] : "";
           $base = rn_ibss_base_name($m);
           if ($base !== null && $base !== "") {
               $ibss_base_names[strtolower($base)] = true;
           }
       }
   }

   // key => array(label, org, mount, producers, consumers, ibss, ibss_base)
   $mounts = array();

   // First pass: producers. IBSS-shared bases use Org / Mountpoint (not receiver name).
   foreach ($rows as $row) {
       foreach (rn_ntrip_slot_defs() as $slot) {
           if ($slot["kind"] === "client" || empty($row[$slot["en"]])) {
               continue;
           }
           $expected_mount = isset($row[$slot["mount"]]) ? (string)$row[$slot["mount"]] : "";
           if ($expected_mount === "") {
               continue;
           }
           $server = rn_ntrip_server_name($row);
           $as_ibss = isset($ibss_base_names[strtolower($server)]);
           list($key, $label, $ibss, $ibss_base) = rn_ntrip_mount_identity($expected_mount, $row, $as_ibss);
           if ($as_ibss) {
               // Keep mountpoint as configured; label is always Org / Mountpoint.
               $org = rn_ntrip_org($row);
               $key = "ibss|" . strtolower($org) . "|" . $expected_mount;
               $label = rn_ntrip_ibss_label($org, $expected_mount);
               $ibss = true;
               $ibss_base = $server;
           }
           if (!isset($mounts[$key])) {
               $mounts[$key] = array(
                   "label" => $label,
                   "org" => rn_ntrip_org($row),
                   "mount" => $expected_mount,
                   "producers" => array(),
                   "consumers" => array(),
                   "ibss" => $ibss,
                   "ibss_base" => $ibss_base,
               );
           }
           $mounts[$key]["producers"][] = array(
               "row" => $row,
               "slot" => $slot,
               "expected_mount" => $expected_mount,
               "expected_format" => ($slot["format"] !== null && isset($row[$slot["format"]])) ? (string)$row[$slot["format"]] : "",
           );
       }
   }

   // Second pass: clients. IBSS clients attach to Org/base buckets; others by mountpoint.
   foreach ($rows as $row) {
       foreach (rn_ntrip_slot_defs() as $slot) {
           if ($slot["kind"] !== "client" || empty($row[$slot["en"]])) {
               continue;
           }
           $expected_mount = isset($row[$slot["mount"]]) ? (string)$row[$slot["mount"]] : "";
           if ($expected_mount === "") {
               continue;
           }
           $entry = array(
               "row" => $row,
               "slot" => $slot,
               "expected_mount" => $expected_mount,
               "expected_format" => "",
           );
           $ibss_base = rn_ibss_base_name($expected_mount);
           if ($ibss_base !== null) {
               $org = rn_ntrip_org($row);
               $keys = rn_ntrip_matching_mount_keys($mounts, $expected_mount, $row);
               if (count($keys) === 0) {
                   // No producer in dashboard: still show Org / Mountpoint.
                   $key = "ibss|" . strtolower($org) . "|" . $expected_mount;
                   $mounts[$key] = array(
                       "label" => rn_ntrip_ibss_label($org, $expected_mount),
                       "org" => $org,
                       "mount" => $expected_mount,
                       "producers" => array(),
                       "consumers" => array($entry),
                       "ibss" => true,
                       "ibss_base" => $ibss_base,
                   );
               } else {
                   foreach ($keys as $key) {
                       $mounts[$key]["consumers"][] = $entry;
                   }
               }
               continue;
           }
           $keys = rn_ntrip_matching_mount_keys($mounts, $expected_mount, $row);
           if (count($keys) === 0) {
               list($key, $label, $ibss, $ibss_base) = rn_ntrip_mount_identity($expected_mount, $row, false);
               $mounts[$key] = array(
                   "label" => $label,
                   "org" => rn_ntrip_org($row),
                   "mount" => $expected_mount,
                   "producers" => array(),
                   "consumers" => array($entry),
                   "ibss" => $ibss,
                   "ibss_base" => $ibss_base,
               );
           } else {
               foreach ($keys as $key) {
                   $mounts[$key]["consumers"][] = $entry;
               }
           }
       }
   }

   // Index mounts under each producer Loc_Group; client-only mounts under "(no producer)".
   $ntrip_by_group = array();
   foreach ($mounts as $key => $info) {
       $producer_groups = array();
       foreach ($info["producers"] as $p) {
           $g = isset($p["row"]["Loc_Group"]) ? (string)$p["row"]["Loc_Group"] : "";
           $producer_groups[$g] = true;
       }
       if (count($producer_groups) === 0) {
           // IBSS / client-only: group by the consumer org when present.
           foreach ($info["consumers"] as $c) {
               $g = isset($c["row"]["Loc_Group"]) ? (string)$c["row"]["Loc_Group"] : "";
               $producer_groups[$g] = true;
           }
       }
       if (count($producer_groups) === 0) {
           $producer_groups = array("(no producer)" => true);
       }
       foreach ($producer_groups as $g => $_) {
           if (!isset($ntrip_by_group[$g])) {
               $ntrip_by_group[$g] = array();
           }
           $ntrip_by_group[$g][$key] = $info;
       }
   }

   // Sort groups: named groups first, then ungrouped "", then "(no producer)".
   uksort($ntrip_by_group, function ($a, $b) {
       if ($a === "(no producer)") {
           return 1;
       }
       if ($b === "(no producer)") {
           return -1;
       }
       if ($a === "" && $b !== "") {
           return 1;
       }
       if ($b === "" && $a !== "") {
           return -1;
       }
       return strcasecmp($a, $b);
   });

   if (count($mounts) === 0) {
       echo "<p>No enabled NTRIP slots.</p>";
   } else {
       echo "\n<table border='1' class='tablesorter radio-ntrip'>\n";
       echo "<thead><tr><th>Mount</th><th>Format</th><th>Producers (Server/Caster)</th><th>Consumers (Client)</th></tr></thead>\n<tbody>\n";

       $ntrip_group_i = 0;
       foreach ($ntrip_by_group as $group => $group_mounts) {
           if ($ntrip_group_i > 0) {
               echo "\n<tr class=\"group-spacer\"><td colspan=\"4\">&nbsp;</td></tr>\n";
           }
           $ntrip_group_i++;
           if ($group === "(no producer)") {
               $group_label = "(no producer in dashboard)";
           } elseif ($group === "") {
               $group_label = "(ungrouped)";
           } else {
               $group_label = $group;
           }
           echo "\n<tr><td colspan=\"4\" class=\"td_header\">Group: " . h($group_label) . "</td></tr>\n";

           uasort($group_mounts, function ($a, $b) {
               return strnatcasecmp($a["label"], $b["label"]);
           });
           foreach ($group_mounts as $key => $info) {
               // Producers for this group header (or all when in "(no producer)").
               $prod_html = array();
               $seen_prod = array();
               $format_html = "";
               $format_mismatch = false;
               foreach ($info["producers"] as $p) {
                   $p_group = isset($p["row"]["Loc_Group"]) ? (string)$p["row"]["Loc_Group"] : "";
                   if ($group !== "(no producer)" && $p_group !== $group) {
                       continue;
                   }
                   list($fmt_txt, $fmt_bad) = rn_ntrip_format_display($p);
                   if ($format_html === "" && $fmt_txt !== "") {
                       $format_html = $fmt_txt;
                       $format_mismatch = $fmt_bad;
                   } elseif ($fmt_bad) {
                       $format_mismatch = true;
                   }
                   // One row per server name (collapse Server/Caster slots on the same receiver).
                   $prod_dedupe = strtolower(rn_ntrip_server_name($p["row"])) . "|" . $p["expected_mount"];
                   if (isset($seen_prod[$prod_dedupe])) {
                       continue;
                   }
                   $seen_prod[$prod_dedupe] = true;
                   $prod_html[] = rn_ntrip_endpoint_cells($p, $user_id);
               }

               // All consumers; annotate group when it differs from this section's group.
               $cons_html = array();
               $seen_cons = array();
               foreach ($info["consumers"] as $c) {
                   $c_group = isset($c["row"]["Loc_Group"]) ? (string)$c["row"]["Loc_Group"] : "";
                   $cons_dedupe = strtolower(rn_ntrip_server_name($c["row"])) . "|" . $c["slot"]["label"] . "|" . $c["expected_mount"];
                   if (isset($seen_cons[$cons_dedupe])) {
                       continue;
                   }
                   $seen_cons[$cons_dedupe] = true;
                   $cell = rn_ntrip_endpoint_cells($c, $user_id);
                   if ($group !== "(no producer)" && $c_group !== $group) {
                       $c_label = ($c_group === "") ? "(ungrouped)" : $c_group;
                       $cell .= " <em>[" . h($c_label) . "]</em>";
                   }
                   $cons_html[] = $cell;
               }

               echo "\n<tr>";
               echo "\n<td>" . h($info["label"]) . "</td>";
               if ($format_html !== "") {
                   echo rn_cell($format_html, $format_mismatch);
               } else {
                   echo "\n<td>&nbsp;</td>";
               }
               echo "\n<td>" . (count($prod_html) ? implode("<br/>", $prod_html) : "&nbsp;") . "</td>";
               echo "\n<td>" . (count($cons_html) ? implode("<br/>", $cons_html) : "&nbsp;") . "</td>";
               echo "\n</tr>";
           }
       }
       echo "</tbody></table>\n";
   }

   // ---- Receiver details: expected base-observables streams ----
   echo '<h2 class="section-title">Receiver details</h2>';
   echo '<p>Expected base-observables / correction streams for each enabled receiver (Radio and NTRIP). ';
   echo 'UDP/TCP source or sink roles and external serial connections are not supported by this dashboard yet.</p>';

   echo "\n<table border='1' class='tablesorter radio-ntrip'>\n";
   echo "<thead><tr><th>Edit</th><th>Name</th><th>Group</th><th>Serial</th><th>Base station</th><th>Expected observables stream</th></tr></thead>\n<tbody>\n";

   $detail_i = 0;
   $current_group = null;
   foreach ($rows as $row) {
       $group = isset($row["Loc_Group"]) ? (string)$row["Loc_Group"] : "";
       if ($current_group !== $group) {
           if ($detail_i > 0) {
               echo "\n<tr class=\"group-spacer\"><td colspan=\"6\">&nbsp;</td></tr>\n";
           }
           $detail_i++;
           $current_group = $group;
           $group_label = ($group === "") ? "(ungrouped)" : $group;
           echo "\n<tr><td colspan=\"6\" class=\"td_header\">Group: " . h($group_label) . "</td></tr>\n";
       }

       $receiver_url = gnss_receiver_url(
           isset($row["Address"]) ? $row["Address"] : "",
           isset($row["Port"]) ? $row["Port"] : "",
           isset($row["UseHTTPS"]) ? $row["UseHTTPS"] : false
       );
       $name_html = h($row["name"]);
       if ($receiver_url !== "") {
           $name_html = '<a href="' . h($receiver_url) . '" target="_blank" rel="noopener noreferrer">' . $name_html . '</a>';
       }

       $streams = rn_expected_observables_streams($row);
       $stream_html = count($streams) ? h(implode("; ", $streams)) : "<em>None configured (Radio/NTRIP)</em>";

       $serial = isset($row["Serial_Number"]) ? (string)$row["Serial_Number"] : "";
       $base_station = isset($row["Ref_Name"]) ? (string)$row["Ref_Name"] : "";

       echo "\n<tr>";
       echo '<td><a href="Edit_GNSS.php?GNSS_ID=' . h($row["id"]) . '&User_ID=' . h($user_id) . '">Edit</a></td>';
       echo "\n<td>" . $name_html . "</td>";
       echo "\n<td>" . h($group_label) . "</td>";
       echo "\n<td>" . ($serial !== "" ? h($serial) : "<em>(auto on first check)</em>") . "</td>";
       echo "\n<td>" . ($base_station !== "" ? h($base_station) : "<em>(auto on first check)</em>") . "</td>";
       echo "\n<td>" . $stream_html . "</td>";
       echo "\n</tr>";
   }
   echo "</tbody></table>\n";

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
