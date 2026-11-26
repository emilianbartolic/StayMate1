"""Check local HTTP route protections against a running StayMate service."""
from __future__ import annotations

import json
import os
import sys
from http.cookiejar import CookieJar
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import HTTPCookieProcessor, Request, build_opener

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = os.environ.get("STAYMATE_CHECK_URL", "http://127.0.0.1:8000").rstrip("/")
ORIGIN = os.environ.get("STAYMATE_CHECK_ORIGIN", "http://127.0.0.1:8000")
DB_PATH = Path(os.environ.get("STAYMATE_DB_PATH", str(ROOT / "user-data" / "staymate.sqlite3")))
CREDENTIALS_FILE = DB_PATH.parent / "local-admin-credentials.txt"
opener = build_opener(HTTPCookieProcessor(CookieJar()))


def json_or_empty(content: bytes) -> dict:
    try:
        parsed = json.loads(content)
        return parsed if isinstance(parsed, dict) else {}
    except (ValueError, TypeError):
        return {}


def request(method: str, path: str, data: dict | None = None, csrf: str = "", origin: str = ORIGIN) -> tuple[int, dict, object]:
    body = None if data is None else json.dumps(data).encode()
    headers = {"Origin": origin}
    if body is not None:
        headers["Content-Type"] = "application/json"
    if csrf:
        headers["X-StayMate-CSRF"] = csrf
    req = Request(BASE_URL + path, data=body, headers=headers, method=method)
    try:
        response = opener.open(req, timeout=10)
    except HTTPError as exc:
        return exc.code, json_or_empty(exc.read()), exc.headers
    content = response.read()
    return response.status, json_or_empty(content), response.headers


def main() -> int:
    status, _, headers = request("GET", "/")
    assert status == 200 and headers.get("Content-Security-Policy") and headers.get("X-Content-Type-Options") == "nosniff"
    assert request("GET", "/api/skills")[0] == 401
    assert request("GET", "/api/tickets")[0] == 401
    assert request("GET", "/api/properties/city-loft/knowledge")[0] == 401
    assert request("GET", "/backend/requirements.lock")[0] == 404
    assert request("GET", "/user-data/local-admin-credentials.txt")[0] == 404
    assert request("GET", "/.git/config")[0] == 404
    csrf_status, csrf_body, _ = request("GET", "/api/auth/csrf")
    assert csrf_status == 200 and csrf_body.get("csrf_token")
    csrf = csrf_body["csrf_token"]
    assert request("POST", "/api/auth/login", {"email": "invalid@example.test", "password": "invalid"})[0] == 403
    assert request("POST", "/api/auth/login", {"email": "invalid@example.test", "password": "invalid"}, csrf, "https://evil.example")[0] == 403
    assert request("POST", "/api/auth/login", {"email": "invalid@example.test", "password": "invalid"}, "wrong-token")[0] == 403

    if CREDENTIALS_FILE.exists():
        credentials = json.loads(CREDENTIALS_FILE.read_text(encoding="utf-8"))
        email, password = credentials["email"], credentials["password"]
    else:
        email = os.environ.get("STAYMATE_LOCAL_ADMIN_EMAIL", "host@staymate.local")
        password = os.environ.get("STAYMATE_LOCAL_ADMIN_PASSWORD", "")
    if not password:
        raise RuntimeError(f"Lokales Host-Passwort fehlt in {CREDENTIALS_FILE} oder STAYMATE_LOCAL_ADMIN_PASSWORD.")
    status, _, _ = request("POST", "/api/auth/login", {"email": email, "password": password}, csrf)
    assert status == 200
    assert request("GET", "/api/skills")[0] == 404
    assert request("GET", "/api/tickets")[0] == 200
    assert request("GET", "/api/properties/city-loft/knowledge")[0] == 200
    assert request("POST", "/api/admin/model/stop", {})[0] == 403

    try:
        assert request("POST", "/api/admin/model/stop", {}, csrf)[0] == 200
        assert request("GET", "/api/status")[1]["model_enabled"] is False
    finally:
        assert request("POST", "/api/admin/model/resume", {}, csrf)[0] == 200
    assert request("GET", "/api/status")[1]["model_enabled"] is True
    assert request("POST", "/api/auth/logout", {}, csrf)[0] == 200
    assert request("GET", "/api/tickets")[0] == 401
    print("PASS local HTTP security: headers, private files, host login, origin, CSRF, admin routes, model stop/resume, logout.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"FAIL local HTTP security: {exc}", file=sys.stderr)
        raise
