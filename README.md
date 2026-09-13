# GNSS-Dashboard

Web dashboard and Nagios integration for managing a fleet of Trimble GNSS receivers: verify configuration, get alerts when settings drift, and upgrade firmware.

## Requirements

- **SQLite 3** and **PHP SQLite** extension
- **Python 3** with pip
- **Apache** (or similar) with PHP and CGI enabled
- **Nagios** and nagios-plugins (for scheduled status checks)

```bash
apt-get install sqlite3 php-sqlite3 python3 python3-pip
```

Python dependencies (installed by `setup.sh --install`):

```bash
pip3 install -r requirements.txt
```

Packages: `requests`, `lxml`, `cryptography`.

## Installation

1. Clone or copy this repository onto the server.

2. Run setup as root:

   ```bash
   sudo ./setup.sh --install
   ```

   - **Default** (`sudo ./setup.sh`): copies `www/*` → `/var/www/html/Dashboard` and `cgi/*` → `/usr/lib/cgi-bin/Dashboard` only.
   - **`--install`**: also creates `secret_key`, installs Python packages, runs `DB_Setup.php`, and sets permissions.

3. Enable PHP for the web server and increase upload limits for firmware:

   ```bash
   sudo nano /etc/php/7.4/apache2/php.ini
   ```

   ```ini
   upload_max_filesize = 25M
   post_max_size = 100M
   ```

4. If CGI is not installed under `/usr/lib/cgi-bin/Dashboard`, update paths in:

   - `www/db.inc.php`
   - `cgi/db.inc.php`
   - `cgi/db.inc.py`

### Deploying updates

`git pull` does **not** update the live site. After pulling changes, run:

```bash
sudo ./setup.sh
```

Use `sudo ./setup.sh --install` only when setting up a new host or when install steps (DB schema, dependencies) are needed.

## Security

On first install, `setup.sh --install` creates `/usr/lib/cgi-bin/Dashboard/secret_key` (mode 600). You can instead set the environment variable `GNSS_SECRET_KEY` or copy `cgi/secret_key.example` to `secret_key`.

The secret key is used for:

- CSRF tokens on edit forms
- Encrypting receiver admin passwords in the database (`enc:` prefix)

Receiver passwords are not shown in plain text in list views. HTTPS links to receivers are supported via the **UseHTTPS** option on each receiver.

## Nagios

Install Nagios and plugins as usual. The command definition is in `User/GNSS-Commands.cfg`:

```text
command_line    /usr/lib/cgi-bin/Dashboard/Status_Update.py $ARG1$
```

Add to `nagios.cfg`:

```text
cfg_dir=/usr/lib/cgi-bin/Dashboard/User
```

`Status_Update.py` polls each receiver over HTTP/HTTPS, compares live settings to the database, and updates the `STATUS` table.

If email is enabled and `<result>` is not OK, Nothing, or InProgress, the checker calls **`/cgi-bin/emailAlert.xml?request=1`** and re-reads **`/xml/dynamic/email.xml`** every 2 seconds for up to 20 seconds (retrying emailAlert each poll) before reporting a failure.

### Database access

The web UI and background `Status_Update.py` jobs share one SQLite database (`GNSS.db`). Connections use **WAL mode** and a **10 second busy timeout** (`gnss_open_db()` in PHP, `open_database()` in Python) so list pages do not fail when Nagios runs many checks at once.

**WAL needs a writable directory**, not only a writable `.db` file. Opening the DB creates or updates `GNSS.db-wal` and `GNSS.db-shm` next to `GNSS.db`. If you see `Error opening db` when not root, check:

```bash
ls -la /usr/lib/cgi-bin/Dashboard/
ls -la /usr/lib/cgi-bin/Dashboard/GNSS.db*
```

`setup.sh` sets the CGI directory to `www-data:nagios` mode `2775` and the DB/sidecars to mode `0660`. For manual CLI runs, either:

```bash
sudo -u www-data /usr/lib/cgi-bin/Dashboard/Status_Update.py <GNSS_ID>
# or add your user to the nagios group, then re-login:
sudo usermod -aG nagios "$USER"
```

`Status_Update.py` holds the database open while polling receivers (slow). If you still see lock contention under heavy load, consider serializing checks or refactoring status updates to close the DB during HTTP calls.

## Web UI

| Page | Purpose |
|------|---------|
| `Receiver_List.php` | All receivers for a user; edit, duplicate, delete |
| `List_Status.php` | Live status from Nagios checks |
| `Edit_GNSS.php` | Add or edit receiver configuration |
| `Receiver_Upgrade.php` | Firmware upgrade workflow |
| `Error_List.php` | Receiver error logs |

All pages require `User_ID` in the query string (from sign-in).

### List Status filters

`List_Status.php` provides:

- **Group** — filter by `Loc_Group` (All groups, each distinct group, or “no group”).
- **Show disabled receivers** — unchecked by default. Disabled receivers (`Enabled` unchecked in the edit form) are hidden unless this box is checked.

### Edit receiver

Notable radio and connectivity fields:

- **HTTPS** — use `https://` when opening the receiver link and during status checks (`verify=False` for self-signed certs).
- **Radio Band** — `900 MHz` or `450 MHz` (not combo).
- **Radio On** — when off, status checks only verify on/off state; frequency, wireless mode, and other radio fields are not compared.
- **450 MHz** — frequency, active channel spacing (12.5 / 25 kHz), wireless mode.
- **900 MHz** — network number (1–40).

The receiver link beside **Port** is focused on load when an address is set (not the password field).

## Radio configuration

Wireless mode labels and receiver XML name overrides live in:

- `cgi/radio_wireless_modes.json` — dropdown labels (filtered and sorted alphabetically in the UI)
- `cgi/radio_wireless_mode_xml_names.json` — strings as returned in `type450/curWirelessModeLong`

Logic in `cgi/radio_config.py`:

- Drops reserved, deprecated, 220 MHz, TrimTalk v2, SiteNet 900/2400, PCC external customer, and TrimTalk v1 Auto RxO modes from the UI list.
- Normalizes receiver strings for matching (leading mode ID, spacing, `at` / `bps` variants).
- **RTCM135 Auto Rx** modes (104, 105) also match the active FEC ON/OFF strings the receiver reports at runtime.

To add or remove modes, edit the JSON files and redeploy. Receivers still configured with a removed mode ID must be updated in the edit form.

### Status check messages

If `radiosummary.xml` is missing:

```text
Radiosummary not found. Does the unit have a radio? Or too old firmware.
```

## Backup

Add to cron (adjust email in `Backup_GNSS_DB.sh`):

```cron
0 0 * * *   www-data   /usr/lib/cgi-bin/Dashboard/Backup_GNSS_DB.sh
1 0 * * *   www-data   /usr/lib/cgi-bin/Dashboard/Backup_GNSS.py
```

Programmatic backup uses [Programmatic_Backup.py](https://github.com/jcmb/Programmatic) in the `cgi/Dashboard` directory.

## Directory layout

```text
www/          PHP pages (deployed to /var/www/html/Dashboard)
cgi/          Python CGI scripts and SQLite DB (deployed to /usr/lib/cgi-bin/Dashboard)
User/         Nagios host/service templates
setup.sh      Deploy script
```

## License

See [LICENSE](LICENSE).
