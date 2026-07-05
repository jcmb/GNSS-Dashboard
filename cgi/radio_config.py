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
    names = []
    xml_names = load_wireless_mode_xml_names()
    modes = load_radio_wireless_modes()
    if mode_id in xml_names:
        names.append(xml_names[mode_id])
    if mode_id in modes:
        names.append(modes[mode_id])
    deduped = []
    seen = set()
    for name in names:
        key = normalize_wireless_mode_text(name)
        if key not in seen:
            seen.add(key)
            deduped.append(name)
        prefixed = "{} {}".format(mode_id, name)
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
    )
    for name, coltype in columns:
        try:
            conn.execute("ALTER TABLE GNSS ADD COLUMN {} {}".format(name, coltype))
            conn.commit()
        except sqlite3.OperationalError as err:
            if "duplicate column name" not in str(err).lower():
                raise


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


def detect_active_radio_band(root):
    has_450 = xml_find_text(root, "type450/curChannel") is not None
    has_900 = xml_find_text(
        root,
        "type900/networkId",
        "type900/networkID",
    ) is not None
    if has_450 and not has_900:
        return "450"
    if has_900 and not has_450:
        return "900"
    if has_450 and has_900:
        return "450" if xml_find_text(root, "type450/curChannel") else "900"
    return None


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
