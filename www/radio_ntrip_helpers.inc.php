<?php
/**
 * Shared helpers for Radio / NTRIP configuration views.
 */

function rn_ensure_status_live_columns($db)
{
    $columns = array(
        "Radio_Live_OnOff" => "TEXT",
        "Radio_Live_Mode" => "TEXT",
        "Radio_Live_Band" => "TEXT",
        "Radio_Live_NetworkNumber" => "INTEGER",
        "Radio_Live_Frequency" => "NUMERIC",
        "Radio_Live_WirelessMode" => "TEXT",
        "Radio_Live_ChanSpacing" => "NUMERIC",
        "NTRIP_Client_1_Live_Enabled" => "BOOLEAN",
        "NTRIP_Client_1_Live_Mount" => "TEXT",
        "NTRIP_Client_2_Live_Enabled" => "BOOLEAN",
        "NTRIP_Client_2_Live_Mount" => "TEXT",
        "NTRIP_Client_3_Live_Enabled" => "BOOLEAN",
        "NTRIP_Client_3_Live_Mount" => "TEXT",
        "NTRIP_Server_1_Live_Enabled" => "BOOLEAN",
        "NTRIP_Server_1_Live_Mount" => "TEXT",
        "NTRIP_Server_1_Live_Format" => "TEXT",
        "NTRIP_Server_2_Live_Enabled" => "BOOLEAN",
        "NTRIP_Server_2_Live_Mount" => "TEXT",
        "NTRIP_Server_2_Live_Format" => "TEXT",
        "NTRIP_Server_3_Live_Enabled" => "BOOLEAN",
        "NTRIP_Server_3_Live_Mount" => "TEXT",
        "NTRIP_Server_3_Live_Format" => "TEXT",
        "NTRIP_Caster_1_Live_Enabled" => "BOOLEAN",
        "NTRIP_Caster_1_Live_Mount" => "TEXT",
        "NTRIP_Caster_1_Live_Format" => "TEXT",
        "NTRIP_Caster_2_Live_Enabled" => "BOOLEAN",
        "NTRIP_Caster_2_Live_Mount" => "TEXT",
        "NTRIP_Caster_2_Live_Format" => "TEXT",
        "NTRIP_Caster_3_Live_Enabled" => "BOOLEAN",
        "NTRIP_Caster_3_Live_Mount" => "TEXT",
        "NTRIP_Caster_3_Live_Format" => "TEXT",
    );
    foreach ($columns as $name => $type) {
        @$db->exec("ALTER TABLE STATUS ADD COLUMN {$name} {$type}");
    }
}


function rn_radio_mode_display($mode)
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


function rn_radio_role($mode)
{
    $mode = (string)$mode;
    if ($mode === "RadioModeBase" || strpos($mode, "RadioModeBase") === 0) {
        return "Base";
    }
    if (strpos($mode, "RadioModeRepeater") === 0) {
        return "Repeater";
    }
    if ($mode === "RadioModeRover") {
        return "Rover";
    }
    return "Unknown";
}


function rn_is_base_mode($mode)
{
    return rn_radio_role($mode) === "Base";
}


function rn_radio_modes_match($expected, $live)
{
    if ($expected === null || $live === null || $expected === "" || $live === "") {
        return false;
    }
    if ((string)$expected === (string)$live) {
        return true;
    }
    $legacy = array("RadioModeBase", "RadioModeBaseW4Repeater");
    return in_array((string)$expected, $legacy, true) && in_array((string)$live, $legacy, true);
}


function rn_wireless_modes_sorted($modes)
{
    uasort($modes, function ($a, $b) {
        return strcasecmp($a, $b);
    });
    return $modes;
}


function rn_load_wireless_modes()
{
    $paths = array(
        '/usr/lib/cgi-bin/Dashboard/radio_wireless_modes.json',
        dirname(__DIR__) . '/cgi/radio_wireless_modes.json',
        __DIR__ . '/radio_wireless_modes.json',
    );
    foreach ($paths as $path) {
        if (is_readable($path)) {
            $raw = json_decode(file_get_contents($path), true);
            if (is_array($raw)) {
                return rn_wireless_modes_sorted($raw);
            }
        }
    }
    return array();
}


function rn_load_wireless_xml_names()
{
    $paths = array(
        '/usr/lib/cgi-bin/Dashboard/radio_wireless_mode_xml_names.json',
        dirname(__DIR__) . '/cgi/radio_wireless_mode_xml_names.json',
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


function rn_wireless_display($mode_id, $modes, $xml_names = array())
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


function rn_normalize_wireless_text($text)
{
    $text = strtolower(trim((string)$text));
    $text = preg_replace('/^\d+\s+/', '', $text);
    $text = preg_replace('/\(auto cs and whitening\)/i', '', $text);
    $text = str_replace(':', ' ', $text);
    $text = preg_replace('/\bat\b/', ' ', $text);
    $text = preg_replace('/[,\/()]/', ' ', $text);
    $text = preg_replace('/(\d)\s+bps/', '$1bps', $text);
    $text = preg_replace('/\s+bps\b/', 'bps', $text);
    $text = preg_replace('/\s+/', ' ', $text);
    return trim($text);
}


function rn_wireless_live_matches($mode_id, $live_long, $modes, $xml_names)
{
    if ($mode_id === null || $mode_id === "" || $live_long === null || $live_long === "") {
        return false;
    }
    $actual = rn_normalize_wireless_text($live_long);
    $expected_name = rn_wireless_display($mode_id, $modes, $xml_names);
    $candidates = array($expected_name, (string)(int)$mode_id . ' ' . $expected_name);
    foreach ($candidates as $name) {
        if ($actual !== "" && rn_normalize_wireless_text($name) === $actual) {
            return true;
        }
    }
    // Loose contains match for Auto Rx alias labels.
    $norm_expected = rn_normalize_wireless_text($expected_name);
    if ($norm_expected !== "" && (strpos($actual, $norm_expected) !== false || strpos($norm_expected, $actual) !== false)) {
        return true;
    }
    return false;
}


function rn_expected_band($row)
{
    $band = !empty($row["RadioBand"]) ? $row["RadioBand"] : "900";
    if ($band === "450" || $band === "900" || $band === "combo") {
        return $band;
    }
    if (!empty($row["RadioFrequency"])) {
        return "450";
    }
    if (!empty($row["RadioNetworkNumber"])) {
        return "900";
    }
    return "900";
}


function rn_channel_key($row)
{
    $band = rn_expected_band($row);
    if ($band === "combo") {
        // Cluster combo with peers using frequency if set, else network number.
        if (!empty($row["RadioFrequency"])) {
            $band = "450";
        } else {
            $band = "900";
        }
    }
    if ($band === "900") {
        $net = isset($row["RadioNetworkNumber"]) ? $row["RadioNetworkNumber"] : "";
        return "900|" . (string)$net;
    }
    $freq = isset($row["RadioFrequency"]) ? $row["RadioFrequency"] : "";
    $spacing = isset($row["RadioActiveChanSpacing"]) ? $row["RadioActiveChanSpacing"] : "";
    $wm = isset($row["RadioWirelessMode"]) ? $row["RadioWirelessMode"] : "";
    return "450|" . (string)$freq . "|" . (string)$spacing . "|" . (string)$wm;
}


function rn_channel_key_label($row, $modes, $xml_names)
{
    $band = rn_expected_band($row);
    if ($band === "combo") {
        if (!empty($row["RadioFrequency"])) {
            $band = "450";
        } else {
            $band = "900";
        }
    }
    if ($band === "900") {
        $net = isset($row["RadioNetworkNumber"]) ? $row["RadioNetworkNumber"] : "?";
        return "900 MHz network " . $net;
    }
    $freq = isset($row["RadioFrequency"]) ? $row["RadioFrequency"] : "?";
    $spacing = isset($row["RadioActiveChanSpacing"]) ? $row["RadioActiveChanSpacing"] : "?";
    $wm = rn_wireless_display(isset($row["RadioWirelessMode"]) ? $row["RadioWirelessMode"] : "", $modes, $xml_names);
    return "450 MHz " . $freq . " / " . $spacing . " kHz / " . $wm;
}


function rn_issue_class($mismatch)
{
    return $mismatch ? ' class="Issue"' : '';
}


function rn_cell($text, $mismatch)
{
    return "<td" . rn_issue_class($mismatch) . ">" . h($text) . "</td>";
}


function rn_expected_onoff($row)
{
    return !empty($row["RadioOnOffState"]) ? "On" : "Off";
}


function rn_live_onoff($row)
{
    if (!isset($row["Radio_Live_OnOff"]) || $row["Radio_Live_OnOff"] === null || $row["Radio_Live_OnOff"] === "") {
        return "";
    }
    return (string)$row["Radio_Live_OnOff"];
}


function rn_live_mode_display($row)
{
    if (!isset($row["Radio_Live_Mode"]) || $row["Radio_Live_Mode"] === null || $row["Radio_Live_Mode"] === "") {
        return "";
    }
    return rn_radio_mode_display($row["Radio_Live_Mode"]);
}


function rn_live_band($row)
{
    if (!isset($row["Radio_Live_Band"]) || $row["Radio_Live_Band"] === null || $row["Radio_Live_Band"] === "") {
        return "";
    }
    return (string)$row["Radio_Live_Band"];
}


function rn_live_channel_display($row)
{
    $band = rn_live_band($row);
    if ($band === "" && !empty($row["Radio_Live_Frequency"])) {
        $band = "450";
    }
    if ($band === "" && isset($row["Radio_Live_NetworkNumber"]) && $row["Radio_Live_NetworkNumber"] !== null && $row["Radio_Live_NetworkNumber"] !== "") {
        $band = "900";
    }
    if ($band === "900" || ($band === "combo" && empty($row["Radio_Live_Frequency"]))) {
        if (!isset($row["Radio_Live_NetworkNumber"]) || $row["Radio_Live_NetworkNumber"] === null || $row["Radio_Live_NetworkNumber"] === "") {
            return "";
        }
        return (string)$row["Radio_Live_NetworkNumber"];
    }
    if ($band === "450" || !empty($row["Radio_Live_Frequency"])) {
        $parts = array();
        if (isset($row["Radio_Live_Frequency"]) && $row["Radio_Live_Frequency"] !== null && $row["Radio_Live_Frequency"] !== "") {
            $parts[] = $row["Radio_Live_Frequency"] . " MHz";
        }
        if (isset($row["Radio_Live_ChanSpacing"]) && $row["Radio_Live_ChanSpacing"] !== null && $row["Radio_Live_ChanSpacing"] !== "") {
            $parts[] = $row["Radio_Live_ChanSpacing"] . " kHz";
        }
        return implode(" / ", $parts);
    }
    return "";
}


function rn_onoff_mismatch($row)
{
    $live = rn_live_onoff($row);
    if ($live === "") {
        return false;
    }
    return $live !== rn_expected_onoff($row);
}


function rn_mode_mismatch($row)
{
    if (!isset($row["Radio_Live_Mode"]) || $row["Radio_Live_Mode"] === null || $row["Radio_Live_Mode"] === "") {
        return false;
    }
    return !rn_radio_modes_match(isset($row["RadioMode"]) ? $row["RadioMode"] : "", $row["Radio_Live_Mode"]);
}


function rn_band_mismatch($row)
{
    $live = rn_live_band($row);
    if ($live === "") {
        return false;
    }
    $expected = rn_expected_band($row);
    if ($expected === "combo") {
        return ($live !== "450" && $live !== "900");
    }
    return $live !== $expected;
}


function rn_channel_mismatch($row)
{
    $expected_band = rn_expected_band($row);
    if ($expected_band === "combo") {
        $expected_band = !empty($row["RadioFrequency"]) ? "450" : "900";
    }
    if ($expected_band === "900") {
        if (!isset($row["Radio_Live_NetworkNumber"]) || $row["Radio_Live_NetworkNumber"] === null || $row["Radio_Live_NetworkNumber"] === "") {
            return false;
        }
        if (!isset($row["RadioNetworkNumber"]) || $row["RadioNetworkNumber"] === null || $row["RadioNetworkNumber"] === "") {
            return false;
        }
        return (int)$row["Radio_Live_NetworkNumber"] !== (int)$row["RadioNetworkNumber"];
    }
    if (isset($row["RadioFrequency"]) && $row["RadioFrequency"] !== null && $row["RadioFrequency"] !== ""
        && isset($row["Radio_Live_Frequency"]) && $row["Radio_Live_Frequency"] !== null && $row["Radio_Live_Frequency"] !== "") {
        if (abs((float)$row["Radio_Live_Frequency"] - (float)$row["RadioFrequency"]) > 0.0005) {
            return true;
        }
    }
    return false;
}


function rn_wireless_mismatch($row, $modes, $xml_names)
{
    if (!isset($row["Radio_Live_WirelessMode"]) || $row["Radio_Live_WirelessMode"] === null || $row["Radio_Live_WirelessMode"] === "") {
        return false;
    }
    if (!isset($row["RadioWirelessMode"]) || $row["RadioWirelessMode"] === null || $row["RadioWirelessMode"] === "") {
        return false;
    }
    return !rn_wireless_live_matches($row["RadioWirelessMode"], $row["Radio_Live_WirelessMode"], $modes, $xml_names);
}


function rn_ibss_base_name($mount)
{
    $suffix = "__wm_IBSS";
    $mount = (string)$mount;
    $len = strlen($suffix);
    if ($len > 0 && substr($mount, -$len) === $suffix) {
        return substr($mount, 0, -$len);
    }
    return null;
}


function rn_ntrip_slot_defs()
{
    return array(
        array("kind" => "client", "label" => "Client 1", "en" => "NTRIP_Client_1_Enabled", "mount" => "NTRIP_Client_1_Mount", "format" => null,
              "live_en" => "NTRIP_Client_1_Live_Enabled", "live_mount" => "NTRIP_Client_1_Live_Mount", "live_format" => null),
        array("kind" => "client", "label" => "Client 2", "en" => "NTRIP_Client_2_Enabled", "mount" => "NTRIP_Client_2_Mount", "format" => null,
              "live_en" => "NTRIP_Client_2_Live_Enabled", "live_mount" => "NTRIP_Client_2_Live_Mount", "live_format" => null),
        array("kind" => "client", "label" => "Client 3", "en" => "NTRIP_Client_3_Enabled", "mount" => "NTRIP_Client_3_Mount", "format" => null,
              "live_en" => "NTRIP_Client_3_Live_Enabled", "live_mount" => "NTRIP_Client_3_Live_Mount", "live_format" => null),
        array("kind" => "server", "label" => "Server 1", "en" => "NTRIP_Server_1_Enabled", "mount" => "NTRIP_Server_1_Mount", "format" => "NTRIP_Server_1_Format",
              "live_en" => "NTRIP_Server_1_Live_Enabled", "live_mount" => "NTRIP_Server_1_Live_Mount", "live_format" => "NTRIP_Server_1_Live_Format"),
        array("kind" => "server", "label" => "Server 2", "en" => "NTRIP_Server_2_Enabled", "mount" => "NTRIP_Server_2_Mount", "format" => "NTRIP_Server_2_Format",
              "live_en" => "NTRIP_Server_2_Live_Enabled", "live_mount" => "NTRIP_Server_2_Live_Mount", "live_format" => "NTRIP_Server_2_Live_Format"),
        array("kind" => "server", "label" => "Server 3", "en" => "NTRIP_Server_3_Enabled", "mount" => "NTRIP_Server_3_Mount", "format" => "NTRIP_Server_3_Format",
              "live_en" => "NTRIP_Server_3_Live_Enabled", "live_mount" => "NTRIP_Server_3_Live_Mount", "live_format" => "NTRIP_Server_3_Live_Format"),
        array("kind" => "caster", "label" => "Caster 1", "en" => "NTRIP_Caster_1_Enabled", "mount" => "NTRIP_Caster_1_Mount", "format" => "NTRIP_Caster_1_Format",
              "live_en" => "NTRIP_Caster_1_Live_Enabled", "live_mount" => "NTRIP_Caster_1_Live_Mount", "live_format" => "NTRIP_Caster_1_Live_Format"),
        array("kind" => "caster", "label" => "Caster 2", "en" => "NTRIP_Caster_2_Enabled", "mount" => "NTRIP_Caster_2_Mount", "format" => "NTRIP_Caster_2_Format",
              "live_en" => "NTRIP_Caster_2_Live_Enabled", "live_mount" => "NTRIP_Caster_2_Live_Mount", "live_format" => "NTRIP_Caster_2_Live_Format"),
        array("kind" => "caster", "label" => "Caster 3", "en" => "NTRIP_Caster_3_Enabled", "mount" => "NTRIP_Caster_3_Mount", "format" => "NTRIP_Caster_3_Format",
              "live_en" => "NTRIP_Caster_3_Live_Enabled", "live_mount" => "NTRIP_Caster_3_Live_Mount", "live_format" => "NTRIP_Caster_3_Live_Format"),
    );
}


function rn_emit_radio_row($row, $user_id, $modes, $xml_names)
{
    $role = rn_radio_role(isset($row["RadioMode"]) ? $row["RadioMode"] : "");
    $live_on = rn_live_onoff($row);
    $live_mode = rn_live_mode_display($row);
    $live_band = rn_live_band($row);
    $live_chan = rn_live_channel_display($row);
    $live_wm = isset($row["Radio_Live_WirelessMode"]) ? (string)$row["Radio_Live_WirelessMode"] : "";

    $receiver_url = gnss_receiver_url(
        isset($row["Address"]) ? $row["Address"] : "",
        isset($row["Port"]) ? $row["Port"] : "",
        isset($row["UseHTTPS"]) ? $row["UseHTTPS"] : false
    );
    $name_html = h($row["name"]);
    if ($receiver_url !== "") {
        $name_html = '<a href="' . h($receiver_url) . '" target="_blank" rel="noopener noreferrer">' . $name_html . '</a>';
    }

    echo "\n<tr>";
    echo '<td><a href="Edit_GNSS.php?GNSS_ID=' . h($row["id"]) . '&User_ID=' . h($user_id) . '">Edit</a></td>';
    echo "\n<td>" . $name_html . "</td>";
    echo rn_cell($role, false);
    echo rn_cell($live_on !== "" ? $live_on : "(no data)", rn_onoff_mismatch($row));
    echo rn_cell($live_mode !== "" ? $live_mode : "(no data)", rn_mode_mismatch($row));
    echo rn_cell($live_band !== "" ? $live_band : "(no data)", rn_band_mismatch($row));
    echo rn_cell($live_chan !== "" ? $live_chan : "(no data)", rn_channel_mismatch($row));
    $band_for_wm = $live_band !== "" ? $live_band : rn_expected_band($row);
    if ($band_for_wm === "450" || $band_for_wm === "combo" || $live_wm !== "") {
        echo rn_cell($live_wm !== "" ? $live_wm : "(no data)", rn_wireless_mismatch($row, $modes, $xml_names));
    } else {
        echo "\n<td>&nbsp;</td>";
    }
    echo "\n</tr>";
}


function rn_ntrip_endpoint_cells($entry, $user_id)
{
    $row = $entry["row"];
    $slot = $entry["slot"];
    $live_en = isset($row[$slot["live_en"]]) ? $row[$slot["live_en"]] : null;
    $live_mount = isset($row[$slot["live_mount"]]) ? $row[$slot["live_mount"]] : null;
    $live_format = ($slot["live_format"] !== null && isset($row[$slot["live_format"]])) ? $row[$slot["live_format"]] : null;

    $en_mismatch = ($live_en !== null && (int)$live_en !== 1);
    $mount_mismatch = ($live_mount !== null && $live_mount !== "" && (string)$live_mount !== (string)$entry["expected_mount"]);
    $format_mismatch = false;
    if ($slot["format"] !== null && $entry["expected_format"] !== "" && $live_format !== null && $live_format !== "") {
        $format_mismatch = ((string)$live_format !== (string)$entry["expected_format"]);
    }

    $live_en_txt = ($live_en === null || $live_en === "") ? "(no data)" : ((int)$live_en ? "On" : "Off");
    $live_mount_txt = ($live_mount === null || $live_mount === "") ? "(no data)" : (string)$live_mount;
    $live_format_txt = "";
    if ($slot["format"] !== null) {
        $live_format_txt = ($live_format === null || $live_format === "") ? "(no data)" : (string)$live_format;
    }

    $edit_html = '<a href="Edit_GNSS.php?GNSS_ID=' . h($row["id"]) . '&User_ID=' . h($user_id) . '">Edit</a>';
    $receiver_url = gnss_receiver_url(
        isset($row["Address"]) ? $row["Address"] : "",
        isset($row["Port"]) ? $row["Port"] : "",
        isset($row["UseHTTPS"]) ? $row["UseHTTPS"] : false
    );
    $name_html = h($row["name"]);
    if ($receiver_url !== "") {
        $name_html = '<a href="' . h($receiver_url) . '" target="_blank" rel="noopener noreferrer">' . $name_html . '</a>';
    }

    $parts = array();
    $parts[] = $edit_html;
    $parts[] = $name_html . " (" . h($slot["label"]) . ")";
    $parts[] = '<span' . rn_issue_class($en_mismatch) . '>live ' . h($live_en_txt) . '</span>';
    $parts[] = '<span' . rn_issue_class($mount_mismatch) . '>mount ' . h($live_mount_txt) . '</span>';
    if ($slot["format"] !== null) {
        $parts[] = '<span' . rn_issue_class($format_mismatch) . '>fmt ' . h($live_format_txt) . '</span>';
    }
    return implode(" — ", $parts);
}
