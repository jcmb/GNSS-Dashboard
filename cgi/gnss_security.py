"""Shared security helpers for GNSS Dashboard CGI scripts."""

import hashlib
import hmac
import os
import re
import time
from hashlib import pbkdf2_hmac

try:
    from cryptography.fernet import Fernet, InvalidToken
except ImportError:
    Fernet = None
    InvalidToken = Exception

PBKDF2_ITERATIONS = 600_000
_ENCRYPTED_PREFIX = "enc:"


def _secret_key_paths():
    try:
        from db_inc import cgiDir
        cgi_dir = cgiDir()
    except ImportError:
        cgi_dir = os.path.dirname(os.path.abspath(__file__)) + os.sep
    return [
        os.environ.get("GNSS_SECRET_KEY", "").strip(),
        "/usr/lib/cgi-bin/Dashboard/secret_key",
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "secret_key"),
        os.path.join(cgi_dir, "secret_key"),
    ]


def get_secret_key():
    for path in _secret_key_paths():
        if not path:
            continue
        if os.path.isfile(path):
            with open(path, "r", encoding="utf-8") as handle:
                key = handle.read().strip()
            if key:
                return key.encode("utf-8")
        if len(path) >= 32 and not os.path.isfile(path):
            return path.encode("utf-8")
    raise RuntimeError(
        "GNSS secret key not configured. Set GNSS_SECRET_KEY or create secret_key in the cgi directory."
    )


def _fernet():
    if Fernet is None:
        return None
    raw = get_secret_key()
    import base64
    key = base64.urlsafe_b64encode(hashlib.sha256(raw).digest())
    return Fernet(key)


def encrypt_receiver_password(plain):
    if plain is None or plain == "":
        return plain
    if Fernet is None:
        return plain
    fernet = _fernet()
    if fernet is None:
        return plain
    token = fernet.encrypt(str(plain).encode("utf-8")).decode("ascii")
    return _ENCRYPTED_PREFIX + token


def decrypt_receiver_password(stored):
    if stored is None:
        return ""
    stored = str(stored)
    if not stored.startswith(_ENCRYPTED_PREFIX):
        return stored
    if Fernet is None:
        return stored
    fernet = _fernet()
    if fernet is None:
        return stored
    token = stored[len(_ENCRYPTED_PREFIX):].encode("ascii")
    try:
        return fernet.decrypt(token).decode("utf-8")
    except InvalidToken:
        return stored


def generate_csrf_token(user_id):
    secret = get_secret_key()
    ts = str(int(time.time()))
    msg = f"{user_id}:{ts}".encode("utf-8")
    sig = hmac.new(secret, msg, hashlib.sha256).hexdigest()
    return f"{ts}:{sig}"


def validate_csrf_token(token, user_id, max_age=3600):
    if not token or ":" not in token:
        return False
    ts, sig = token.split(":", 1)
    try:
        ts_int = int(ts)
    except ValueError:
        return False
    if time.time() - ts_int > max_age:
        return False
    secret = get_secret_key()
    msg = f"{user_id}:{ts}".encode("utf-8")
    expected = hmac.new(secret, msg, hashlib.sha256).hexdigest()
    return hmac.compare_digest(sig, expected)


def require_csrf(form, user_id):
    token = form.getfirst("csrf_token", "")
    if not validate_csrf_token(token, user_id):
        print("CSRF validation failed<br/>")
        raise SystemExit(403)


def verify_user_exists(cursor, user_id):
    cursor.execute("SELECT id FROM Users WHERE id=?", (user_id,))
    if cursor.fetchone() is None:
        print("Invalid user<br/>")
        raise SystemExit(403)


def verify_gnss_owner(cursor, gnss_id, user_id):
    cursor.execute("SELECT User_ID FROM GNSS WHERE id=?", (gnss_id,))
    row = cursor.fetchone()
    if row is None or str(row[0]) != str(user_id):
        print("Access denied<br/>")
        raise SystemExit(403)


def sanitize_upload_filename(name):
    name = os.path.basename(name)
    if not re.match(r"^[A-Za-z0-9._-]+\.(timg|img)$", name, re.IGNORECASE):
        raise ValueError(f"Invalid firmware filename: {name}")
    return name


def validate_prog_command(cmd):
    if not re.match(r"^[A-Za-z0-9_]+$", cmd or ""):
        raise ValueError("Invalid programmatic command")


def verify_user_password(password, salt, stored_hash):
    """Verify password, accepting legacy iteration counts."""
    for iters in (PBKDF2_ITERATIONS, 1000):
        dk = pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iters)
        if dk.hex() == str(stored_hash):
            return True, iters
    return False, None


def hash_user_password(password, salt):
    dk = pbkdf2_hmac("sha256", password.encode("utf-8"), salt, PBKDF2_ITERATIONS)
    return dk.hex()


def validate_prog_params(params):
    if params is None:
        return ""
    params = str(params)
    if re.search(r"[\r\n]", params):
        raise ValueError("Invalid programmatic parameters")
    if len(params) > 500:
        raise ValueError("Programmatic parameters too long")
    return params
