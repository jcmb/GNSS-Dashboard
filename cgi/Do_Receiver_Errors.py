#!/usr/bin/env python3
"""Receiver error-log actions without exposing credentials in URLs."""

import cgi
import datetime
import os
import sqlite3
import subprocess
import sys

from db_inc import cgiDir, databaseFile
from gnss_security import decrypt_receiver_password, require_csrf, verify_gnss_owner, verify_user_exists


def _load_receiver(cursor, user_id, gnss_id):
    verify_user_exists(cursor, user_id)
    verify_gnss_owner(cursor, gnss_id, user_id)
    cursor.execute(
        "SELECT id, name, Address, Port, Password FROM GNSS WHERE id=? AND User_ID=?",
        (gnss_id, user_id),
    )
    row = cursor.fetchone()
    if row is None:
        print("Receiver not found<br/>")
        raise SystemExit(404)
    return {
        "id": row[0],
        "name": row[1],
        "address": row[2],
        "port": row[3],
        "password": decrypt_receiver_password(row[4]),
    }


def _errorlogs_cmd(receiver, extra_args):
    script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ErrorLogs.py")
    return [
        sys.executable,
        script,
        receiver["address"],
        str(receiver["port"]),
        "admin",
        receiver["password"],
        receiver["name"],
    ] + extra_args


def main():
    form = cgi.FieldStorage()
    user_id = form.getfirst("User_ID", "")
    gnss_id = form.getfirst("GNSS_ID", "")
    action = form.getfirst("action", "view")

    if not user_id or not gnss_id:
        print("Content-Type: text/html\n")
        print("Missing User_ID or GNSS_ID")
        raise SystemExit(400)

    conn = sqlite3.connect(databaseFile())
    cursor = conn.cursor()
    receiver = _load_receiver(cursor, user_id, gnss_id)
    conn.close()

    if action in ("clear",):
        require_csrf(form, user_id)

    if action == "view":
        print("Content-Type: text/html\n")
        print("<html><head><title>Receiver Error Log</title></head><body>")
        print(f"{receiver['name']} ({receiver['address']}:{receiver['port']})<br/><pre>")
        subprocess.run(_errorlogs_cmd(receiver, ["--View"]), check=False)
        print("</pre></body></html>")
        return

    if action == "clear":
        print("Content-Type: text/html\n")
        print("<html><head><title>Receiver Error Log</title></head><body>")
        print(f"{receiver['name']} ({receiver['address']}:{receiver['port']})<br/>Clearing<br/><pre>")
        subprocess.run(_errorlogs_cmd(receiver, ["--View", "--Clear"]), check=False)
        status_script = os.path.join(cgiDir(), "Status_Update.py")
        subprocess.run([sys.executable, status_script, str(receiver["id"])], check=False)
        print("</pre></body></html>")
        return

    if action == "download":
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        zip_path = os.path.join("/tmp", f"{receiver['name']}.zip")
        subprocess.run(_errorlogs_cmd(receiver, ["--Zip", "--Clone"]), check=False)
        print("Content-Type: application/octet-stream")
        print(f'Content-Disposition: attachment; filename="{receiver["name"]}-{date}.zip"')
        print()
        if os.path.isfile(zip_path):
            with open(zip_path, "rb") as handle:
                sys.stdout.buffer.write(handle.read())
        return

    if action == "clone":
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        clone_path = os.path.join("/tmp", f"{receiver['name']}.clone.xml")
        subprocess.run(_errorlogs_cmd(receiver, ["--Clone"]), check=False)
        print("Content-Type: application/octet-stream")
        print(f'Content-Disposition: attachment; filename="{receiver["name"]}-{date}.clone.xml"')
        print()
        if os.path.isfile(clone_path):
            with open(clone_path, "rb") as handle:
                sys.stdout.buffer.write(handle.read())
        return

    print("Content-Type: text/html\n")
    print("Unknown action")
    raise SystemExit(400)


if __name__ == "__main__":
    main()
