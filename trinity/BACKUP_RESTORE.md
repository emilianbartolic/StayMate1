# Backup und Wiederherstellung

Die Laufzeitdatenbank liegt unter `user-data/staymate.sqlite3`. Sie enthält freigegebene Memory-Einträge, Host-Tickets und minimierte Audit-Ereignisse. Sie wird von Git ausgeschlossen.

Backup:

```bash
python3 scripts/backup_restore.py backup
```

Restore erfordert die ausdrückliche Bestätigung `--confirm`. Vor dem Restore wird automatisch ein Vorher-Backup angelegt:

```bash
python3 scripts/backup_restore.py restore user-data/backups/staymate-YYYYMMDDTHHMMSSZ.sqlite3 --confirm
```

Restore zuerst mit einer Kopie der Datenbank prüfen. API-Schlüssel und Codex-Anmeldedaten gehören nicht in das Backup. Das Backup enthält Gästefragen aus Host-Tickets und muss entsprechend geschützt werden.
