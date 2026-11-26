"""Exercise SQLite persistence, approval, ticket replies, audit, and backup."""
from __future__ import annotations
import tempfile
import sys
import os
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import trinity.hub.memory as memory_store
from trinity.hub.memory import (
    backup, claim_model_call, create_ticket, list_events, list_memory, list_tickets,
    model_calls_today, purge_expired_data, purge_old_backups, record_event, remember, reply_ticket,
    search, set_memory_status, database,
)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="staymate-storage-check-") as directory:
        root = Path(directory)
        db_path = root / "staymate.sqlite3"
        backup_path = root / "backup.sqlite3"
        memory_id = remember("Confirmed parking is available", "smoke-check", "city-loft", path=db_path)
        assert list_memory(status="pending", path=db_path)[0]["id"] == memory_id
        assert set_memory_status(memory_id, "approved", path=db_path)
        assert search("parking available", scope="city-loft", path=db_path)
        ticket = create_ticket("city-loft", "City Loft", "", "Can I arrive early?", "host_decision", "normal", "early arrival", "demo-session", path=db_path)
        record_event("request-demo", "city-loft", "guest_response", {"skills_applied": 11}, path=db_path)
        assert reply_ticket(ticket["id"], "The host confirmed the time.", path=db_path)["status"] == "answered"
        assert list_tickets(status="answered", conversation_id="demo-session", path=db_path)[0]["id"] == ticket["id"]
        assert list_events("request-demo", path=db_path)[0]["payload"]["skills_applied"] == 11
        assert claim_model_call(1, path=db_path)
        assert not claim_model_call(1, path=db_path)
        assert model_calls_today(path=db_path) == 1
        old_ticket = create_ticket("city-loft", "City Loft", "", "Old question", "unknown", "normal", "old summary", path=db_path)
        old_memory_id = remember("Expired host note", "smoke-check", "city-loft", status="approved", path=db_path)
        with database(db_path) as db:
            db.execute("UPDATE host_tickets SET updated_at='2000-01-01T00:00:00+00:00' WHERE id=?", (old_ticket["id"],))
            db.execute("UPDATE agent_events SET created_at='2000-01-01T00:00:00+00:00' WHERE request_id='request-demo'")
            db.execute("UPDATE memory SET expires_at='2000-01-01T00:00:00+00:00' WHERE id=?", (old_memory_id,))
        deleted = purge_expired_data(path=db_path, force=True)
        assert deleted["tickets"] == deleted["events"] == deleted["memory"] == 1
        assert list_tickets(path=db_path)[0]["id"] == ticket["id"]
        assert list_events("request-demo", path=db_path) == []
        assert old_memory_id not in {item["id"] for item in list_memory(path=db_path)}
        backup(backup_path, path=db_path)
        assert list_tickets(status="answered", path=backup_path)[0]["host_reply"] == "The host confirmed the time."
        backup_dir = root / "backups"
        backup_dir.mkdir(mode=0o700)
        memory_store.DEFAULT_BACKUP_DIR = backup_dir
        old_backup = backup_dir / "staymate-old.sqlite3"
        recent_backup = backup_dir / "staymate-recent.sqlite3"
        old_backup.write_bytes(b"synthetic old backup")
        recent_backup.write_bytes(b"synthetic recent backup")
        old_time = time.time() - 100 * 86400
        os.utime(old_backup, (old_time, old_time))
        assert purge_old_backups(backup_dir, force=True) == 1
        assert not old_backup.exists() and recent_backup.exists()
    print("PASS SQLite memory, approval, retention, model quota, host reply, audit, and backup.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
