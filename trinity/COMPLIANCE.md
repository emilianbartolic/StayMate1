# Anforderungen und Umsetzungsstatus

| Anforderung aus Bauplan/Leitfaden | Stand dieser Version | Beleg |
|---|---|---|
| Mehrere Unterkünfte mit objektbezogenem Faktenabruf | Umgesetzt: drei StayMate-Objekte plus neun ergänzende Angebote | `backend/app.py`, `backend/properties.json`, `backend/guest_objects.json` |
| 11 interne Skills bleiben für Gäste unsichtbar | Umgesetzt: alle 11 werden bei jeder Objektfrage als stille Pipeline-Stufen ausgewertet | `trinity/agents/staymate/skills/skills.json`, `backend/app.py` |
| Gastantwort, Sprache, Quellen und Entscheidung | Umgesetzt; Codex erzeugt die Antwort, der Server liefert Quellen und Entscheidung. Skill- und Routing-Diagnosen bleiben im Host-Audit. | `/api/chat`, `/api/cli/chat`, `output.schema.json` |
| Browser und CLI nutzen denselben Dienst | Umgesetzt | Browser-UI und `trinity/hub/cli_adapter.py` |
| Freigegebenes Memory bleibt nach Neustart erhalten | Umgesetzt über SQLite; neue Notizen bleiben bis zur Host-Freigabe pending | `trinity/hub/memory.py`, `/api/memory` |
| Kritische/unbekannte Fragen gehen an den Host | Umgesetzt über SQLite-Tickets mit Priorität, Status und Antwortfeld | `/api/tickets`, Host-Dashboard |
| Auditierbarer Arbeitsstatus | Umgesetzt: Anfrage-ID, Skill-Ergebnisse, Kategorie, Priorität, Quellen und minimierte Ereignisse | `/api/audit/{request_id}` |
| Suchdialog mit Empfehlung und Objekt-Chat | Umgesetzt; lokale Codex-Laufzeit, zehn Suchangaben, Alternativen und Rückwechsel | `finder.js`, `staymate.html` |
| Benchmark- und Skill-Matrix | Skripte und Testkatalog vorhanden; Skripte müssen nach Änderungen ausgeführt werden | `scripts/run_benchmark.py`, `scripts/run_skill_matrix.py`, `test_cases.json` |
| Backup/Restore | Implementiert; Restore verlangt `--confirm` und erstellt vorher ein Backup | `scripts/backup_restore.py`, `BACKUP_RESTORE.md` |
| Sicherheitsgrenzen für lokalen Betrieb | Gehärtet: API loopback-only, rollenbasierte Host-Routen, CSRF-/Origin-Schutz, Codex ohne Gastwerkzeuge, restriktives Datei-/Netzprofil und gepinnte Python-Abhängigkeiten | `SECURITY_REVIEW.md` |
| Öffentlicher Mehrbenutzerbetrieb | Bewusst blockiert, bis offizielle nutzergebundene Codex-Anmeldung und unabhängiger Review vorliegen | `PUBLIC_DEPLOYMENT.md`, Startup-Guard in `backend/app.py` |
| Konten-/Rollenbausteine | Angelegt, aber nicht als Produktions-Login freigeschaltet | `trinity/hub/accounts.py` |
| Read-only Unterkunftssuche | Adapter für Booking.com Demand API implementiert; Live-Nutzung wartet auf freigeschalteten Partnerzugang und Zugangsdaten. Buchung und Zahlung bleiben beim Anbieter. | `PROVIDER_INTEGRATIONS.md`, `backend/booking_inventory.py` |
| Hostnachrichten und Objektverwaltung über Anbieter-APIs | Nicht umgesetzt: Airbnb-/Booking.com-Connectivity-Freigaben und konkrete Hostintegrationen fehlen; manuelle Host-Antwort bleibt verfügbar. | `PROVIDER_INTEGRATIONS.md` |

Die implementierten Komponenten sind nicht gleichbedeutend mit erfolgreicher Produktionsabnahme. Der Python-3.11-`pip-audit`-Scan ist sauber. Externe Scans, unabhängiger Review und Restore-Abnahme sind noch offen dokumentiert.
