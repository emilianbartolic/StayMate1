"""Password-based accounts and revocable opaque sessions for public deployments."""
from __future__ import annotations

import base64
import hashlib
import hmac
import os
import re
import secrets
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

from trinity.hub.memory import DB_PATH, database, now

SESSION_DAYS = 14
PASSWORD_HASH_ITERATIONS = 600_000
EMAIL_RE = re.compile(r"^[^\s@]{1,64}@[^\s@]{1,190}\.[^\s@]{2,63}$")


def _hash_password(password: str, salt: bytes) -> str:
    derived = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, PASSWORD_HASH_ITERATIONS, dklen=64)
    return "pbkdf2_sha256$" + str(PASSWORD_HASH_ITERATIONS) + "$" + base64.urlsafe_b64encode(salt).decode() + "$" + base64.urlsafe_b64encode(derived).decode()


def _check_password(password: str, encoded: str) -> bool:
    try:
        parts = encoded.split("$")
        if len(parts) == 4 and parts[0] == "pbkdf2_sha256":
            iterations = int(parts[1])
            salt = base64.urlsafe_b64decode(parts[2].encode())
            expected = base64.urlsafe_b64decode(parts[3].encode())
            if not 100_000 <= iterations <= 1_000_000 or len(salt) != 16 or len(expected) != 64:
                return False
            actual = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations, dklen=len(expected))
        elif len(parts) == 6 and parts[:4] == ["scrypt", "16384", "8", "1"] and hasattr(hashlib, "scrypt"):
            salt = base64.urlsafe_b64decode(parts[4].encode())
            expected = base64.urlsafe_b64decode(parts[5].encode())
            if len(salt) != 16 or len(expected) != 64:
                return False
            actual = hashlib.scrypt(password.encode("utf-8"), salt=salt, n=2**14, r=8, p=1, dklen=len(expected), maxmem=64 * 1024 * 1024)
        else:
            return False
        return hmac.compare_digest(actual, expected)
    except (ValueError, TypeError, MemoryError, OverflowError):
        return False


def _new_password_hash(password: str) -> str:
    return _hash_password(password, secrets.token_bytes(16))


def _public_user(row) -> dict:
    return {"id": row["id"], "email": row["email"], "display_name": row["display_name"], "role": row["role"]}


def create_user(email: str, password: str, display_name: str = "", role: str = "guest", path=DB_PATH) -> dict:
    email = email.strip().lower()
    if not EMAIL_RE.fullmatch(email):
        raise ValueError("Bitte eine gültige E-Mail-Adresse eingeben.")
    if len(password) < 12 or len(password) > 256:
        raise ValueError("Das Passwort muss zwischen 12 und 256 Zeichen lang sein.")
    if role not in {"guest", "host"}:
        raise ValueError("Ungültige Kontorolle.")
    user = {"id": str(uuid.uuid4()), "email": email, "display_name": display_name.strip()[:60], "password_hash": _new_password_hash(password), "role": role, "created_at": now()}
    try:
        with database(path) as db:
            db.execute("INSERT INTO users(id,email,display_name,password_hash,role,created_at) VALUES(:id,:email,:display_name,:password_hash,:role,:created_at)", user)
    except Exception as exc:
        if "UNIQUE constraint failed: users.email" in str(exc):
            raise ValueError("Für diese E-Mail-Adresse besteht bereits ein Konto.") from None
        raise
    return {key: value for key, value in user.items() if key not in {"password_hash", "created_at"}}


def ensure_host(email: str, password: str, path=DB_PATH) -> dict:
    email = email.strip().lower()
    with database(path) as db:
        row = db.execute("SELECT * FROM users WHERE email=? COLLATE NOCASE", (email,)).fetchone()
    if row:
        if row["role"] != "host":
            raise ValueError("Die konfigurierte Host-E-Mail gehört bereits zu einem Gastkonto. Verwende eine andere STAYMATE_ADMIN_EMAIL.")
        if not _check_password(password, row["password_hash"]):
            with database(path) as db:
                db.execute("UPDATE users SET password_hash=? WHERE id=?", (_new_password_hash(password), row["id"]))
        return _public_user(row)
    return create_user(email, password, "StayMate Host", "host", path)


def authenticate(email: str, password: str, path=DB_PATH) -> Optional[dict]:
    with database(path) as db:
        row = db.execute("SELECT * FROM users WHERE email=? COLLATE NOCASE", (email.strip().lower(),)).fetchone()
    if row is None:
        # Spend approximately the same password-hash time for unknown emails.
        dummy_salt = base64.urlsafe_b64encode(b"0123456789abcdef").decode()
        dummy_hash = base64.urlsafe_b64encode(b"0" * 64).decode()
        _check_password(password, f"pbkdf2_sha256${PASSWORD_HASH_ITERATIONS}${dummy_salt}${dummy_hash}")
        return None
    if not _check_password(password, row["password_hash"]):
        return None
    if not row["password_hash"].startswith("pbkdf2_sha256$"):
        with database(path) as db:
            db.execute("UPDATE users SET password_hash=? WHERE id=?", (_new_password_hash(password), row["id"]))
    return _public_user(row)


def issue_session(user_id: str, path=DB_PATH) -> tuple[str, str]:
    token = secrets.token_urlsafe(32)
    token_hash = _token_hash(token, path)
    expires = (datetime.now(timezone.utc) + timedelta(days=SESSION_DAYS)).isoformat(timespec="seconds")
    with database(path) as db:
        db.execute("INSERT INTO auth_sessions(token_hash,user_id,expires_at,created_at) VALUES(?,?,?,?)", (token_hash, user_id, expires, now()))
    return token, expires


def get_session(token: str, path=DB_PATH) -> Optional[dict]:
    if not token or len(token) > 128:
        return None
    token_hash = _token_hash(token, path)
    with database(path) as db:
        row = db.execute("SELECT u.id,u.email,u.display_name,u.role,s.expires_at FROM auth_sessions s JOIN users u ON u.id=s.user_id WHERE s.token_hash=?", (token_hash,)).fetchone()
        if row and row["expires_at"] <= now():
            db.execute("DELETE FROM auth_sessions WHERE token_hash=?", (token_hash,))
            return None
    return _public_user(row) if row else None


def revoke_session(token: str, path=DB_PATH) -> None:
    if not token:
        return
    token_hash = _token_hash(token, path)
    with database(path) as db:
        db.execute("DELETE FROM auth_sessions WHERE token_hash=?", (token_hash,))


def _token_hash(token: str, path=DB_PATH) -> str:
    configured_secret = os.environ.get("STAYMATE_SESSION_SECRET", "")
    if configured_secret:
        if len(configured_secret) < 32:
            raise ValueError("STAYMATE_SESSION_SECRET muss mindestens 32 Zeichen haben.")
        secret = configured_secret.encode()
    else:
        key_file = Path(path).parent / ".session-hmac-key"
        key_file.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        try:
            os.chmod(key_file.parent, 0o700)
        except OSError:
            pass
        try:
            descriptor = os.open(key_file, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        except FileExistsError:
            descriptor = None
        if descriptor is not None:
            with os.fdopen(descriptor, "wb") as stream:
                stream.write(secrets.token_bytes(32))
        secret = key_file.read_bytes()
        if len(secret) != 32:
            raise RuntimeError("Der lokale Sitzungs-Schlüssel ist ungültig.")
        os.chmod(key_file, 0o600)
    return hmac.new(secret, token.encode(), hashlib.sha256).hexdigest()

