#!/usr/bin/env python3

import os
import sys
import re
import json
import requests
import argparse
from pathlib import Path

# --- Constants & Defaults ---
DEFAULT_URL = None
DEFAULT_USER_ID = "1"
CONFIG_FILE = Path.home() / ".gnss_upload_config"

FILE_MAPPING = {
    "AlloyUpload": "alloy",
    "BarracudaUpload": "bcuda",
    "ChinstrapUpload": "chinstrap",
    "ClarkUpload": "clark",
    "LancetUpload": "lancet",
    "KryptonUpload": "krypton_titan"
}

def load_config():
    """Loads configuration from the home directory if it exists."""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Could not read config file: {e}")
    return {}

def get_version_from_files(files):
    pattern = re.compile(r"V(\d+_\d+)\.(timg|img)$", re.IGNORECASE)
    for f in files:
        match = pattern.search(f)
        if match:
            s=match.group(1).replace("_", "-")
            part1, part2 = s.split('-')

            # Format the first part: insert '.' after the first character
            # e.g., "660" -> "6.60"
            formatted_part1 = f"{part1[0]}.{part1[1:]}"

            # Format the second part: remove leading zeros by converting to int
            # e.g., "023" -> "23"
            formatted_part2 = str(int(part2))

            # Join them back together
            return f"{formatted_part1}-{formatted_part2}"
    return None

def find_file_for_field(field_keyword, files):
    for f in files:
        if field_keyword.lower() in f.lower():
            return f
    return None

def main():
    # 1. Setup Argument Parser
    parser = argparse.ArgumentParser(description="GNSS Firmware Upload Utility")
    parser.add_argument("--host", help="Target server name")
    parser.add_argument("--user", help="User ID")
    parser.add_argument("--type", choices=['release', 'beta', 'branch', 'trunk'],
                        default='branch', help="Release type (default: branch)")

    args = parser.parse_args()
    config = load_config()

    # 2. Determine Final Parameters (CLI > Config > Default)
    target_host = args.host or config.get("host") or DEFAULT_URL
    if target_host is None:
        sys.exit("Error: URL must be provided.")

    target_url = "https://"+target_host+"/cgi-bin/Dashboard/do_fw_upload.php"

    user_id = args.user or config.get("user_id") or DEFAULT_USER_ID
    fw_type = args.type.capitalize() # Capitalize to match typical form values

    current_dir = os.getcwd()
    files = [f for f in os.listdir(current_dir) if os.path.isfile(f)]

    version = get_version_from_files(files)
    if not version:
        sys.exit("Error: Could not determine firmware version from local files.")

    print(f"Target URL: {target_url}")
    print(f"User ID:    {user_id}")
    print(f"Type:       {fw_type}")
    print(f"Version:    {version}\n")

    # 3. Prepare Payload
    data = {
        "User_ID": user_id,
        "Firmware": fw_type,
        "Titianversion": version
    }

    files_payload = {}
    missing_files = []

    for field_name, keyword in FILE_MAPPING.items():
        filename = find_file_for_field(keyword, files)
        if filename:
            files_payload[field_name] = open(os.path.join(current_dir, filename), 'rb')
        else:
            missing_files.append(field_name)

    if missing_files:
        print(f"Warning: Missing files for: {', '.join(missing_files)}")
        if input("Continue anyway? (y/n): ").lower() != 'y':
            sys.exit("Aborted.")

    # 4. Upload
    try:
        print(f"Uploading...")
        # verify=False handles self-signed certs often found on dyndns setups
        response = requests.post(target_url, data=data, files=files_payload, verify=True)

        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("Upload successful!")
        else:
            print(f"Upload failed: {response.text[:500]}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        for f in files_payload.values():
            f.close()

if __name__ == "__main__":
    main()
