"""SQLite-backed approved memory, guest tickets, and auditable agent events."""
from __future__ import annotations

import json
import os
import re
import sqlite3
import threading
import time
import uuid
from contextlib import contextmanager, closing
from datetime import datetime, timedelta, timezone
from pathlib import Path

DB_PATH = Path(os.environ.get("STAYMATE_DB_PATH", str(Path(__file__).resolve().parents[2] / "user-data" / "staymate.sqlite3")))
DEFAULT_DATA_DIR = Path(__file__).resolve().parents[2] / "user-data"
DEFAULT_BACKUP_DIR = DEFAULT_DATA_DIR / "backups"
_init_lock = threading.Lock()
_initialized_paths: set[str] = set()
_cleanup_lock = threading.Lock()
_last_cleanup_monotonic = 0.0
_backup_cleanup_lock = threading.Lock()
_last_backup_cleanup_monotonic = 0.0


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def connect(path: Path | str = DB_PATH) -> sqlite3.Connection:
    database = Path(path)
    database.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    if database.parent.resolve() == DEFAULT_DATA_DIR.resolve():
        os.chmod(database.parent, 0o700)
    db = sqlite3.connect(database, timeout=10)
    os.chmod(database, 0o600)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys=ON")
    key = str(database.resolve())
    if key not in _initialized_paths:
        with _init_lock:
            if key not in _initialized_paths:
                db.execute("PRAGMA journal_mode=WAL")
                db.executescript("""
                    CREATE TABLE IF NOT EXISTS memory (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        content TEXT NOT NULL,
                        source TEXT NOT NULL,
                        scope TEXT NOT NULL,
                        status TEXT NOT NULL DEFAULT 'pending',
                        approved_by TEXT,
                        created_at TEXT NOT NULL,
                        expires_at TEXT
                    );
                    CREATE INDEX IF NOT EXISTS memory_scope_status ON memory(scope, status);
                    CREATE TABLE IF NOT EXISTS host_tickets (
                        id TEXT PRIMARY KEY,
                        conversation_id TEXT NOT NULL DEFAULT '',
                        property_id TEXT NOT NULL,
                        property_name TEXT NOT NULL,
                        source_url TEXT NOT NULL DEFAULT '',
                        question TEXT NOT NULL,
                        category TEXT NOT NULL,
                        priority TEXT NOT NULL,
                        summary TEXT NOT NULL,
                        status TEXT NOT NULL DEFAULT 'open',
                        host_reply TEXT NOT NULL DEFAULT '',
                        created_at TEXT NOT NULL,
                        updated_at TEXT NOT NULL
                    );
                    CREATE INDEX IF NOT EXISTS tickets_status_created ON host_tickets(status, created_at DESC);
                    CREATE TABLE IF NOT EXISTS agent_events (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        request_id TEXT NOT NULL,
                        property_id TEXT NOT NULL,
                        event_type TEXT NOT NULL,
                        payload_json TEXT NOT NULL,
                        created_at TEXT NOT NULL
                    );
                    CREATE INDEX IF NOT EXISTS events_request ON agent_events(request_id, id);
                    CREATE TABLE IF NOT EXISTS users (
                        id TEXT PRIMARY KEY,
                        email TEXT NOT NULL UNIQUE COLLATE NOCASE,
                        display_name TEXT NOT NULL DEFAULT '',
                        password_hash TEXT NOT NULL,
                        role TEXT NOT NULL DEFAULT 'guest' CHECK(role IN ('guest','host')),
                        created_at TEXT NOT NULL
                    );
                    CREATE TABLE IF NOT EXISTS auth_sessions (
                        token_hash TEXT PRIMARY KEY,
                        user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                        expires_at TEXT NOT NULL,
                        created_at TEXT NOT NULL
                    );
                    CREATE INDEX IF NOT EXISTS sessions_user ON auth_sessions(user_id);
                    CREATE TABLE IF NOT EXISTS conversations (
                        conversation_id TEXT PRIMARY KEY,
                        user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                        created_at TEXT NOT NULL
                    );
                    CREATE TABLE IF NOT EXISTS model_call_usage (
                        usage_date TEXT PRIMARY KEY,
                        calls INTEGER NOT NULL DEFAULT 0 CHECK(calls >= 0)
                    );
                """)
                memory_columns = {row["name"] for row in db.execute("PRAGMA table_info(memory)").fetchall()}
                if "approved_by" not in memory_columns:
                    db.execute("ALTER TABLE memory ADD COLUMN approved_by TEXT")
                columns = {row["name"] for row in db.execute("PRAGMA table_info(host_tickets)").fetchall()}
                if "conversation_id" not in columns:
                    db.execute("ALTER TABLE host_tickets ADD COLUMN conversation_id TEXT NOT NULL DEFAULT ''")
                if "owner_id" not in columns:
                    db.execute("ALTER TABLE host_tickets ADD COLUMN owner_id TEXT")
                db.execute("PRAGMA user_version=3")
                db.commit()
                _initialized_paths.add(key)
    if database.parent.resolve() == DEFAULT_DATA_DIR.resolve():
        for sidecar in (Path(str(database) + "-wal"), Path(str(database) + "-shm")):
            if sidecar.exists():
                os.chmod(sidecar, 0o600)
    return db


@contextmanager
def database(path: Path | str = DB_PATH):
    db = connect(path)
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def _retention_days(name: str, default: int) -> int:
    try:
        value = int(os.environ.get(name, str(default)))
    except (TypeError, ValueError):
        return default
    return min(max(value, 1), 3650)


def purge_expired_data(path: Path | str = DB_PATH, *, force: bool = False) -> dict[str, int]:
    """Delete expired user data and old daily counters, at most hourly by default."""
    global _last_cleanup_monotonic
    current_mono = time.monotonic()
    with _cleanup_lock:
        if not force and current_mono - _last_cleanup_monotonic < 3600:
            return {"tickets": 0, "events": 0, "memory": 0, "sessions": 0, "conversations": 0}
        current = datetime.now(timezone.utc)
        ticket_cutoff = (current - timedelta(days=_retention_days("STAYMATE_TICKET_RETENTION_DAYS", 90))).isoformat(timespec="seconds")
        event_cutoff = (current - timedelta(days=_retention_days("STAYMATE_AUDIT_RETENTION_DAYS", 90))).isoformat(timespec="seconds")
        memory_cutoff = (current - timedelta(days=_retention_days("STAYMATE_MEMORY_RETENTION_DAYS", 365))).isoformat(timespec="seconds")
        current_timestamp = current.isoformat(timespec="seconds")
        usage_cutoff = (current.date() - timedelta(days=30)).isoformat()
        with database(path) as db:
            counts = {
                "tickets": db.execute("DELETE FROM host_tickets WHERE updated_at < ?", (ticket_cutoff,)).rowcount,
                "events": db.execute("DELETE FROM agent_events WHERE created_at < ?", (event_cutoff,)).rowcount,
                "memory": db.execute(
                    "DELETE FROM memory WHERE (expires_at IS NOT NULL AND expires_at <= ?) OR created_at < ?",
                    (current_timestamp, memory_cutoff),
                ).rowcount,
                "sessions": db.execute("DELETE FROM auth_sessions WHERE expires_at <= ?", (current_timestamp,)).rowcount,
                "conversations": db.execute("DELETE FROM conversations WHERE created_at < ?", (ticket_cutoff,)).rowcount,
            }
            db.execute("DELETE FROM model_call_usage WHERE usage_date < ?", (usage_cutoff,))
        _last_cleanup_monotonic = current_mono
        return counts


def purge_old_backups(directory: Path | str = DEFAULT_BACKUP_DIR, *, force: bool = False) -> int:
    """Remove aged StayMate backups from the private default backup directory at most hourly."""
    global _last_backup_cleanup_monotonic
    backup_dir = Path(directory)
    if backup_dir.resolve() != DEFAULT_BACKUP_DIR.resolve() or not backup_dir.exists():
        return 0
    current_mono = time.monotonic()
    with _backup_cleanup_lock:
        if not force and current_mono - _last_backup_cleanup_monotonic < 3600:
            return 0
        _last_backup_cleanup_monotonic = current_mono
    cutoff = time.time() - _retention_days("STAYMATE_BACKUP_RETENTION_DAYS", 90) * 86400
    removed = 0
    for candidate in backup_dir.glob("staymate-*.sqlite3"):
        try:
            if candidate.is_file() and not candidate.is_symlink() and candidate.stat().st_mtime < cutoff:
                candidate.unlink()
                removed += 1
        except OSError:
            continue
    return removed


def claim_model_call(limit_per_day: int, path: Path | str = DB_PATH) -> bool:
    """Atomically reserve one Codex call from the UTC daily installation quota."""
    if limit_per_day < 1:
        return False
    usage_date = datetime.now(timezone.utc).date().isoformat()
    with database(path) as db:
        db.execute("BEGIN IMMEDIATE")
        row = db.execute("SELECT calls FROM model_call_usage WHERE usage_date=?", (usage_date,)).fetchone()
        if row and row["calls"] >= limit_per_day:
            return False
        db.execute(
            "INSERT INTO model_call_usage(usage_date,calls) VALUES(?,1) "
            "ON CONFLICT(usage_date) DO UPDATE SET calls=calls+1",
            (usage_date,),
        )
    return True


def model_calls_today(path: Path | str = DB_PATH) -> int:
    usage_date = datetime.now(timezone.utc).date().isoformat()
    with database(path) as db:
        row = db.execute("SELECT calls FROM model_call_usage WHERE usage_date=?", (usage_date,)).fetchone()
    return int(row["calls"]) if row else 0


def remember(content: str, source: str = "host", scope: str = "shared", status: str = "pending", approved_by: str | None = None, path: Path | str = DB_PATH) -> int:
    if status not in {"pending", "approved", "rejected"}:
        raise ValueError("Ungültiger Memory-Status")
    retention = _retention_days("STAYMATE_PENDING_MEMORY_RETENTION_DAYS", 30) if status == "pending" else _retention_days("STAYMATE_MEMORY_RETENTION_DAYS", 365)
    expires_at = (datetime.now(timezone.utc) + timedelta(days=retention)).isoformat(timespec="seconds")
    with database(path) as db:
        cursor = db.execute(
            "INSERT INTO memory(content,source,scope,status,approved_by,created_at,expires_at) VALUES(?,?,?,?,?,?,?)",
            (content.strip(), source.strip()[:100], scope.strip()[:100], status, approved_by, now(), expires_at),
        )
        return int(cursor.lastrowid)


def search(query: str, scope: str = "shared", limit: int = 8, path: Path | str = DB_PATH) -> list[dict]:
    tokens = list(dict.fromkeys(token for token in re.findall(r"[\wäöüß-]{3,}", query.lower()) if token not in {"the", "and", "for", "ist", "gibt", "bitte", "with", "this", "that"}))[:8]
    if not tokens:
        return []
    slots = (tokens + [None] * 8)[:8]
    token_params = [value for token in slots for value in (token, f"%{token}%" if token else None)]
    with database(path) as db:
        rows = db.execute(
            "SELECT id,content,source,scope,status,created_at FROM memory "
            "WHERE status='approved' AND (scope=? OR scope='shared') "
            "AND (expires_at IS NULL OR expires_at > ?) AND ("
            "(? IS NOT NULL AND lower(content) LIKE ?) OR (? IS NOT NULL AND lower(content) LIKE ?) OR "
            "(? IS NOT NULL AND lower(content) LIKE ?) OR (? IS NOT NULL AND lower(content) LIKE ?) OR "
            "(? IS NOT NULL AND lower(content) LIKE ?) OR (? IS NOT NULL AND lower(content) LIKE ?) OR "
            "(? IS NOT NULL AND lower(content) LIKE ?) OR (? IS NOT NULL AND lower(content) LIKE ?)"
            ") ORDER BY created_at DESC LIMIT ?",
            [scope, now(), *token_params, limit],
        ).fetchall()
    return [dict(row) for row in rows]


def list_memory(status: str | None = None, scope: str | None = None, path: Path | str = DB_PATH) -> list[dict]:
    with database(path) as db:
        rows = db.execute(
            "SELECT * FROM memory WHERE (? IS NULL OR status=?) AND (? IS NULL OR scope=?) "
            "AND (expires_at IS NULL OR expires_at > ?) ORDER BY created_at DESC LIMIT 200",
            (status, status, scope, scope, now()),
        ).fetchall()
    return [dict(row) for row in rows]


def set_memory_status(memory_id: int, status: str, approved_by: str = "local-host", path: Path | str = DB_PATH) -> bool:
    if status not in {"approved", "rejected"}:
        raise ValueError("Ungültiger Freigabestatus")
    retention = _retention_days("STAYMATE_MEMORY_RETENTION_DAYS", 365) if status == "approved" else _retention_days("STAYMATE_PENDING_MEMORY_RETENTION_DAYS", 30)
    expires_at = (datetime.now(timezone.utc) + timedelta(days=retention)).isoformat(timespec="seconds")
    with database(path) as db:
        cursor = db.execute("UPDATE memory SET status=?,approved_by=?,expires_at=? WHERE id=?", (status, approved_by[:100], expires_at, memory_id))
        return cursor.rowcount == 1


def create_ticket(property_id: str, property_name: str, source_url: str, question: str, category: str, priority: str, summary: str, conversation_id: str = "", owner_id: str | None = None, path: Path | str = DB_PATH) -> dict:
    ticket = {
        "id": str(uuid.uuid4()), "conversation_id": conversation_id, "owner_id": owner_id, "property_id": property_id, "property_name": property_name,
        "source_url": source_url or "", "question": question, "category": category,
        "priority": priority, "summary": summary, "status": "open", "host_reply": "",
        "created_at": now(), "updated_at": now(),
    }
    with database(path) as db:
        db.execute("INSERT INTO host_tickets(id,conversation_id,owner_id,property_id,property_name,source_url,question,category,priority,summary,status,host_reply,created_at,updated_at) VALUES(:id,:conversation_id,:owner_id,:property_id,:property_name,:source_url,:question,:category,:priority,:summary,:status,:host_reply,:created_at,:updated_at)", ticket)
    return ticket


def list_tickets(status: str | None = None, limit: int = 200, conversation_id: str | None = None, owner_id: str | None = None, path: Path | str = DB_PATH) -> list[dict]:
    with database(path) as db:
        rows = db.execute("SELECT * FROM host_tickets WHERE (? IS NULL OR status=?) AND (? IS NULL OR conversation_id=?) AND (? IS NULL OR owner_id=?) ORDER BY created_at DESC LIMIT ?", (status, status, conversation_id, conversation_id, owner_id, owner_id, limit)).fetchall()
    return [dict(row) for row in rows]


def create_conversation(conversation_id: str, user_id: str, path: Path | str = DB_PATH) -> bool:
    with database(path) as db:
        existing = db.execute("SELECT user_id FROM conversations WHERE conversation_id=?", (conversation_id,)).fetchone()
        if existing:
            return existing["user_id"] == user_id
        db.execute("INSERT INTO conversations(conversation_id,user_id,created_at) VALUES(?,?,?)", (conversation_id, user_id, now()))
    return True


def conversation_owner(conversation_id: str, path: Path | str = DB_PATH) -> str | None:
    with database(path) as db:
        row = db.execute("SELECT user_id FROM conversations WHERE conversation_id=?", (conversation_id,)).fetchone()
    return row["user_id"] if row else None


def reply_ticket(ticket_id: str, reply: str, path: Path | str = DB_PATH) -> dict | None:
    with database(path) as db:
        cursor = db.execute("UPDATE host_tickets SET host_reply=?,status='answered',updated_at=? WHERE id=?", (reply.strip(), now(), ticket_id))
        if cursor.rowcount != 1:
            return None
        row = db.execute("SELECT * FROM host_tickets WHERE id=?", (ticket_id,)).fetchone()
    return dict(row) if row else None


def record_event(request_id: str, property_id: str, event_type: str, payload: dict, path: Path | str = DB_PATH) -> None:
    with database(path) as db:
        db.execute("INSERT INTO agent_events(request_id,property_id,event_type,payload_json,created_at) VALUES(?,?,?,?,?)", (request_id, property_id, event_type, json.dumps(payload, ensure_ascii=False), now()))


def list_events(request_id: str, path: Path | str = DB_PATH) -> list[dict]:
    with database(path) as db:
        rows = db.execute("SELECT * FROM agent_events WHERE request_id=? ORDER BY id", (request_id,)).fetchall()
    result = []
    for row in rows:
        item = dict(row); item["payload"] = json.loads(item.pop("payload_json")); result.append(item)
    return result


def backup(target: Path | str, path: Path | str = DB_PATH) -> str:
    target_path = Path(target)
    target_path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    if target_path.parent.resolve() == DEFAULT_BACKUP_DIR.resolve():
        os.chmod(target_path.parent, 0o700)
    with database(path) as db, closing(sqlite3.connect(target_path)) as output:
        db.backup(output)
    os.chmod(target_path, 0o600)
    return str(target_path)
