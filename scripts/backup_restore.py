"""Create a consistent local SQLite backup or restore with explicit confirmation."""
from __future__ import annotations
import argparse
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from trinity.hub.memory import DB_PATH, backup  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("backup", "restore"))
    parser.add_argument("file", nargs="?", help="Backup-Ziel oder Restore-Quelldatei")
    parser.add_argument("--confirm", action="store_true", help="Bestätigt den Restore in die lokale Datenbank")
    args = parser.parse_args()
    if args.action == "backup":
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        target = Path(args.file) if args.file else ROOT / "user-data" / "backups" / f"staymate-{stamp}.sqlite3"
        print(backup(target))
        return 0
    source = Path(args.file or "")
    if not source.is_file():
        parser.error("Für Restore eine vorhandene SQLite-Datei angeben.")
    if not args.confirm:
        parser.error("Restore schreibt die aktive lokale Datenbank um. Zur Bestätigung --confirm ergänzen.")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup(ROOT / "user-data" / "backups" / f"pre-restore-{stamp}.sqlite3")
    with sqlite3.connect(source) as incoming, sqlite3.connect(DB_PATH) as current:
        incoming.backup(current)
    print(f"Wiederhergestellt: {DB_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
