"""Radio configuration helpers for GNSS Dashboard."""

import json
import os
import re
import sqlite3


_LEGACY_BASE_MODES = {
    "RadioModeBase",
    "RadioModeBaseW4Repeater",
}

RADIO_CHANNEL_SPACINGS = (12.5, 25.0)

# Dual-band (450/900 combo) receiver type IDs from the edit form / SerialNumber rxType.
# MPS566-2=193, R750-2=191, R780-2=329
COMBO_RECEIVER_TYPES = frozenset({"191", "193", "329"})
COMBO_RADIO_INSTANCE_COUNT = 2

# Auto Rx modes report the active FEC ON/OFF string from the receiver, not the Auto Rx label.
_RTCM135_AUTO_RX_ALIASES = {
    104: (100, 102),
    105: (101, 103),
}


def radio_wireless_modes_path():
    paths = [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "radio_wireless_modes.json"),
        "/usr/lib/cgi-bin/Dashboard/radio_wireless_modes.json",
    ]
    for path in paths:
        if os.path.isfile(path):
            return path
    return paths[0]


def _wireless_mode_label_allowed(label):
    lowered = str(label).lower()
    if "reserved" in lowered:
        return False
    if "deprecated" in lowered:
        return False
    if "legacy error" in lowered:
        return False
    if "220 mhz" in lowered or "220mhz" in lowered:
        return False
    if "trimtalk v2" in lowered:
        return False
    if "trimtalk v1 auto" in lowered:
        return False
    if "sitenet 900" in lowered:
        return False
    if "sitenet 2400" in lowered:
        return False
    if "pcc external customer" in lowered:
        return False
    return True


def load_radio_wireless_modes():
    with open(radio_wireless_modes_path(), "r", encoding="utf-8") as handle:
        raw = json.load(handle)
    modes = {
        int(key): value
        for key, value in raw.items()
        if _wireless_mode_label_allowed(value)
    }
    return dict(sorted(modes.items(), key=lambda item: item[1].lower()))


def wireless_mode_label(mode):
    modes = load_radio_wireless_modes()
    return modes.get(int(mode), "Unknown wireless mode {}".format(mode))


def wireless_mode_xml_names_path():
    paths = [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "radio_wireless_mode_xml_names.json"),
        "/usr/lib/cgi-bin/Dashboard/radio_wireless_mode_xml_names.json",
    ]
    for path in paths:
        if os.path.isfile(path):
            return path
    return paths[0]


def load_wireless_mode_xml_names():
    path = wireless_mode_xml_names_path()
    if not os.path.isfile(path):
        return {}
    with open(path, "r", encoding="utf-8") as handle:
        raw = json.load(handle)
    return {int(key): value for key, value in raw.items()}


def wireless_mode_display_name(mode):
    mode_id = int(mode)
    xml_names = load_wireless_mode_xml_names()
    if mode_id in xml_names:
        return xml_names[mode_id]
    return wireless_mode_label(mode_id)


def normalize_wireless_mode_text(text):
    text = str(text).strip().lower()
    text = re.sub(r"^\d+\s+", "", text)
    text = re.sub(r"\(auto cs and whitening\)", "", text, flags=re.I)
    text = text.replace(":", " ")
    text = re.sub(r"\bat\b", " ", text)
    text = re.sub(r"[,/()]", " ", text)
    text = re.sub(r"(\d)\s+bps", r"\1bps", text)
    text = re.sub(r"\s+bps\b", "bps", text)
    return re.sub(r"\s+", " ", text).strip()


def wireless_mode_text_variants(text):
    raw = str(text).strip()
    variants = {normalize_wireless_mode_text(raw)}
    stripped = re.sub(r"^\d+\s+", "", raw)
    if stripped != raw:
        variants.add(normalize_wireless_mode_text(stripped))
    return variants


def wireless_mode_match_names(mode_id):
    mode_id = int(mode_id)
    xml_names = load_wireless_mode_xml_names()
    modes = load_radio_wireless_modes()
    mode_ids = [mode_id]
    if mode_id in _RTCM135_AUTO_RX_ALIASES:
        mode_ids.extend(_RTCM135_AUTO_RX_ALIASES[mode_id])
    deduped = []
    seen = set()
    for mid in mode_ids:
        names = []
        if mid in xml_names:
            names.append(xml_names[mid])
        if mid in modes:
            names.append(modes[mid])
        for name in names:
            key = normalize_wireless_mode_text(name)
            if key not in seen:
                seen.add(key)
                deduped.append(name)
            prefixed = "{} {}".format(mid, name)
            prefixed_key = normalize_wireless_mode_text(prefixed)
            if prefixed_key not in seen:
                seen.add(prefixed_key)
                deduped.append(prefixed)
    return deduped


def wireless_mode_long_matches(mode_id, actual_long):
    if actual_long is None:
        return False
    actual_variants = wireless_mode_text_variants(actual_long)
    expected_variants = set()
    for name in wireless_mode_match_names(mode_id):
        expected_variants.update(wireless_mode_text_variants(name))
    return not actual_variants.isdisjoint(expected_variants)


def ensure_gnss_radio_columns(conn):
    columns = (
        ("RadioBand", "TEXT"),
        ("RadioNetworkNumber", "INTEGER"),
        ("RadioFrequency", "NUMERIC"),
        ("RadioWirelessMode", "INTEGER"),
        ("RadioActiveChanSpacing", "NUMERIC"),
        ("Serial_Number", "TEXT"),
        ("RefStationName", "TEXT"),
    )
    for name, coltype in columns:
        try:
            conn.execute("ALTER TABLE GNSS ADD COLUMN {} {}".format(name, coltype))
            conn.commit()
        except sqlite3.OperationalError as err:
            if "duplicate column name" not in str(err).lower():
                raise


def pos_type_expects_rtk(pos_type):
    return "RTK" in (pos_type or "").upper()


def xml_find_text(root, *paths):
    for path in paths:
        node = root.find(path)
        if node is not None and node.text is not None and str(node.text).strip() != "":
            return str(node.text).strip()
    return None


def _local_tag(element):
    if element is None:
        return None
    tag = element.tag
    if "}" in tag:
        return tag.split("}", 1)[1]
    return tag


def radio_summary_root(root):
    if _local_tag(root) == "radioSummary":
        return root
    for child in root:
        if _local_tag(child) == "radioSummary":
            return child
    return root


def receiver_expects_combo_radio(receiver_type):
    if receiver_type is None:
        return False
    return str(receiver_type).strip() in COMBO_RECEIVER_TYPES


def xml_has_child(root, local_name):
    if root is None:
        return False
    for child in root:
        if _local_tag(child) == local_name:
            return True
    return False


def radio_instance_count(root):
    text = xml_find_text(root, "radioInstanceCount")
    if text is None:
        return None
    try:
        return int(text)
    except (TypeError, ValueError):
        return None


def _band_from_hardware_type(root):
    hardware = xml_find_text(root, "HardwareType")
    if hardware is None:
        return None
    lowered = hardware.lower()
    # Prefer the more specific token when both appear (unlikely).
    has_450 = "450" in lowered
    has_900 = "900" in lowered
    if has_450 and not has_900:
        return "450"
    if has_900 and not has_450:
        return "900"
    return None


def _band_from_radioconfig(radioconfig_root):
    if radioconfig_root is None:
        return None
    is_900 = xml_find_text(radioconfig_root, "is900Radio")
    if is_900 == "1":
        return "900"
    if is_900 == "0":
        return "450"
    if xml_find_text(
        radioconfig_root,
        "networkId",
        "networkID",
        "type900/networkId",
        "type900/networkID",
    ) is not None:
        return "900"
    if xml_find_text(
        radioconfig_root,
        "curChannel",
        "currentChannel",
        "type450/curChannel",
        "frequency",
    ) is not None:
        return "450"
    return _band_from_hardware_type(radioconfig_root)


def detect_active_radio_band(root, radioconfig_root=None):
    """Detect whether the active radio channel is 450 or 900 MHz.

    Preference order:
    1. Explicit type450/curChannel vs type900/networkId fields
    2. Presence of type450 / type900 sections
    3. HardwareType text (RadioType450*, RadioType900*)
    4. radioconfig.xml fallbacks (is900Radio, networkId, frequency)
    """
    has_450_channel = xml_find_text(
        root,
        "type450/curChannel",
        "general/currentChannel",
        "general/currentChannelMHz",
        "general/frequency",
        "radio450MHz/currentChannel",
    ) is not None
    has_900_network = xml_find_text(
        root,
        "type900/networkId",
        "type900/networkID",
        "general/networkID",
        "general/networkId",
        "general/networkNumber",
        "networkID",
    ) is not None

    if has_450_channel and not has_900_network:
        return "450"
    if has_900_network and not has_450_channel:
        return "900"
    if has_450_channel and has_900_network:
        # Both channel fields present; prefer HardwareType, else 450.
        hw_band = _band_from_hardware_type(root)
        if hw_band in ("450", "900"):
            return hw_band
        return "450"

    has_type450 = xml_has_child(root, "type450")
    has_type900 = xml_has_child(root, "type900")
    if has_type450 and not has_type900:
        return "450"
    if has_type900 and not has_type450:
        return "900"
    if has_type450 and has_type900:
        hw_band = _band_from_hardware_type(root)
        if hw_band in ("450", "900"):
            return hw_band
        return "450"

    hw_band = _band_from_hardware_type(root)
    if hw_band in ("450", "900"):
        return hw_band

    return _band_from_radioconfig(radioconfig_root)


def radio_modes_match(expected, actual):
    if expected == actual:
        return True
    if expected in _LEGACY_BASE_MODES and actual in _LEGACY_BASE_MODES:
        return True
    return False


def normalize_radio_mode(mode):
    if mode == "RadioModeBase":
        return "RadioModeBaseW4Repeater"
    return mode


def channel_spacing_matches(expected, actual):
    return abs(float(expected) - float(actual)) < 0.01


def normalize_channel_spacing(value):
    spacing = float(value)
    for allowed in RADIO_CHANNEL_SPACINGS:
        if abs(spacing - allowed) < 0.01:
            return allowed
    return spacing
