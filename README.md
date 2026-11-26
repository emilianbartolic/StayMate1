# StayMate

StayMate verbindet eine geführte Ferienwohnungssuche mit einem separaten Chat pro ausgewählter Unterkunft. WohnBuddy fragt zehn Suchkriterien ab, lässt Codex eine passende Empfehlung und Alternativen formulieren und führt danach in den Objekt-Chat. Beide Bereiche sind wechselseitig erreichbar.

## Lokaler Start mit dem persönlichen Codex

Python 3.11 oder neuer und Codex CLI müssen auf demselben Rechner laufen. Codex einmal anmelden und dann starten:

```bash
codex login
cd backend
python3.11 -m venv .venv311
source .venv311/bin/activate
python -m pip install -r requirements.lock
uvicorn app:app --host 127.0.0.1 --port 8000
```

Die Website ist anschließend unter <http://127.0.0.1:8000> verfügbar. Suchdialog, Objekt-Chat und CLI rufen denselben FastAPI-Dienst und dieselbe lokale Codex-Anmeldung auf. Es gibt keinen Antwort-Fallback: Ist Codex nicht erreichbar, wird kein Modelltext erfunden. Gastaufrufe laufen ephemer, ohne Shell-, Browser-, App- oder Plugin-Werkzeuge, mit gesperrtem Netzwerk für Agentenwerkzeuge und einem deny-by-default-Dateiprofil. Fragen und angehängte Bilder werden an Codex übermittelt; bei aktiver Live-Suche sendet StayMate Suchort, Reisedaten, Gästezahl und Filter an Booking.com.

Die Host-Verwaltung verlangt eine lokale Anmeldung. Beim ersten Start erzeugt StayMate ein zufälliges Host-Passwort in `user-data/local-admin-credentials.txt` (Dateirechte `0600`). Die Gast-Demo braucht kein Konto; Demo-Profil und Favoriten bleiben im Browser.

## Stadtideen für ganz Deutschland

Die Wohnungssuche funktioniert ohne externen Booking.com-Zugang. Sie enthält 262 frei auswählbare fiktive Wohnkonzepte: zwei bis vier individuelle Varianten in jeder der 79 Großstädte der eingebauten Liste sowie je eine Idee für die 26 Kommunen im Landkreis Böblingen. Jede Idee hat ein fotorealistisches KI-Beispielbild, Beschreibung, Beispielgröße, Beispielbelegung, Ausstattungsidee, schematischen Grundriss und einen ausdrücklich fiktiven Preisrichtwert für Budgetvergleiche. Die 186 Einzelmotive werden teils in verschiedenen Städten wiederverwendet; innerhalb einer Stadt erhält jedes Objekt ein anderes Bild. Das sind Entwürfe, keine echten Inserate: Es gibt dafür keinen realen Preis, Kalender, Gastgeber oder Buchungsabschluss. Die Stadtideen erscheinen in der Wohnungssuche und im Objekt-Chat und können dort ausgewählt werden.

Optional kann StayMate zusätzlich echte Partnerangebote abfragen. Dafür verlangt Booking.com einen freigeschalteten Partnerzugang mit API-Key und Affiliate-ID; die Anmeldedaten bleiben serverseitig ([Authentifizierung](https://developers.booking.com/demand/docs/development-guide/authentication), [Voraussetzungen](https://developers.booking.com/demand/docs/getting-started/prerequisites)). Die Such-API prüft verfügbare Unterkünfte anhand von Reisedaten und Gästen, die Detail-API liefert Inseratsdaten und Fotos ([Verfügbarkeitssuche](https://developers.booking.com/demand/docs/accommodations/search-for-available-properties), [Objektdetails und Fotos](https://developers.booking.com/demand/docs/accommodations/look-accommodation-details)). Diese Erweiterung ist optional und wird für die fiktiven Stadtideen nicht benötigt. Zum lokalen Aktivieren:

Für die Live-Suche ist ein freigeschalteter Booking.com-Partnerzugang mit API-Key und Affiliate-ID erforderlich. Booking.com dokumentiert beide Zugangsdaten als verpflichtende Header und empfiehlt, den API-Key nur serverseitig in Umgebungsvariablen oder einem Secret-Store abzulegen ([Authentifizierung](https://developers.booking.com/demand/docs/development-guide/authentication), [Partnerzugang](https://developers.booking.com/demand/docs/getting-started/prerequisites)). Die Such-API filtert nach Reisedaten, Gästezahl, Ort und Preis; die Detail-API liefert Inseratsdaten und Fotos ([Verfügbarkeitssuche](https://developers.booking.com/demand/docs/accommodations/search-for-available-properties), [Objektdetails und Fotos](https://developers.booking.com/demand/docs/accommodations/look-accommodation-details)). Nach Freischaltung:

```bash
cp backend/.env.example backend/.env
# BOOKING_DEMAND_API_KEY und BOOKING_DEMAND_AFFILIATE_ID in backend/.env eintragen
```

`backend/.env` ist von Git ausgeschlossen. Ohne Zugangsdaten bleiben die fiktiven, auswählbaren Ideen vollständig verfügbar; die Website zeigt klar an, dass sie nicht buchbar sind und keine Live-Verfügbarkeit vorliegt.

## Agentenbestandteile

- **11 interne Fähigkeiten** laufen serverseitig bei jeder Objektfrage. Sie klassifizieren Anliegen, suchen Objektwissen, berücksichtigen Sprache und Dringlichkeit, leiten Host-Fälle weiter und erstellen Zusammenfassungen. Die Skill-Namen und Ergebnisse werden Gästen nicht gezeigt.
- **Portfolio über Deutschland**: 262 fiktive Wohnideen mit lokalen KI-Beispielbildern für die 79 Großstädte und 26 Landkreisorte. In jeder Großstadt gibt es zwei bis vier unterschiedliche Konzepte; die Beispielwerte passen zu Personen-, Objektart- und Größenfiltern. Die Ideen sind auswählbar und im Objekt-Chat besprechbar, bleiben aber klar als nicht buchbar gekennzeichnet.
- **SQLite-Memory und Tickets** liegen lokal unter `user-data/staymate.sqlite3`. Host-Notizen werden erst nach manueller Freigabe an Codex übergeben. Eskalationen speichern Objekt, Frage, Kategorie, Priorität und Host-Antwort.
- **Browser und CLI** verwenden dieselbe Agentenpipeline. Beispiel: `python3 trinity/hub/cli_adapter.py "Gibt es Parkplätze?" --property design-maisonette`.
- **Auditdaten** dokumentieren Request-ID, Quellen, Entscheidung, Priorität und Skill-Auswertung; die Gastfrage wird nicht zusätzlich als Audit-Event kopiert.
- **Host-Übergabe**: Ein Host prüft Anbieterangaben selbst und trägt die Antwort im Dashboard ein. Das Ticket bleibt auf der lokalen StayMate-Installation gespeichert und wird im zugehörigen Gastchat sichtbar.
- **Verwaltung** unter `/settings.html`: Codex-/Portfolio-Status, Memory prüfen und freigeben, SQLite-Backup erstellen und Tickets exportieren.

## Tests und Pflege

Mit aktivem lokalen Backend:

```bash
python3 scripts/run_benchmark.py
```

Die vollständige deterministische Matrix für 11 Fähigkeiten über alle 274 Portfolioeinträge läuft ohne Modellkosten:

```bash
backend/.venv311/bin/python scripts/run_skill_matrix.py
```

Die Matrix prüft die Agentenverträge und die getrennte Faktenbasis. Sie bewertet nicht die Qualität jeder möglichen Codex-Formulierung.

SQLite-Memory, Ticketantworten, Audit-Ereignisse und Backup werden mit temporären lokalen Daten geprüft:

```bash
backend/.venv311/bin/python scripts/run_storage_check.py
```

Die lokalen HTTP-Sicherheitsrouten (fremder Origin, ungültiger und fehlender CSRF-Token, Host-Anmeldung, Admin-Routen, Not-Aus und private Dateisperren) lassen sich bei laufendem Server prüfen:

```bash
python scripts/run_security_check.py
```

SQLite-Backup und bestätigungspflichtiger Restore sind in `trinity/BACKUP_RESTORE.md` beschrieben. Die Laufzeitdateien unter `user-data/` sind von Git ausgeschlossen.

## Betriebsgrenzen

Der Dienst ist für einen lokalen Einzelplatzbetrieb an `127.0.0.1` gebunden. Das Gastkonto in der Demo ist ein Browserprofil, kein Konto mit Anmeldung. Backend-Bausteine für Konten und Rollen bleiben gesperrt, bis ein offizieller, nutzergebundener Modellzugang eingerichtet ist. `STAYMATE_PUBLIC=1` wird beim Start abgewiesen, damit mehrere Gäste nicht versehentlich die eine Codex-Anmeldung des Serverprozesses teilen. Details stehen in `trinity/PUBLIC_DEPLOYMENT.md`.

Tickets werden nicht automatisch an Airbnb oder einen Host gesendet. Die Booking.com-Abfrage liefert Angebote und leitet zur Buchungsseite weiter; sie löst keine Buchung oder Zahlung aus. Partnerfreigabe und Zugangsdaten müssen für den jeweiligen Betrieb eingerichtet sein. Verfügbarkeit ist nur nach einer Suche mit konkreten Terminen geprüft und kann sich bis zur Buchung ändern. Siehe `trinity/PROVIDER_INTEGRATIONS.md`.

Ein früher pip-audit-Lauf fand Schwachstellen in der alten Python-3.9-Umgebung. Die Anwendung verwendet jetzt Python 3.11+ mit festgeschriebenen Abhängigkeiten in `backend/requirements.lock`; der neue Laufzeit-Scan steht im Sicherheitsbericht. Unabhängige Security-Reviews und Restore-Abnahme sind noch nicht abgeschlossen. Der dokumentierte Sicherheitsstatus ist keine Zertifizierung: `trinity/SECURITY_REVIEW.md` und `trinity/COMPLIANCE.md`.

Siehe `assets/properties/ATTRIBUTION.md` für Bildquellen. Generierte Innenraumbilder sind als Visualisierungen gekennzeichnet; sie zeigen nicht zwingend das konkrete Mietobjekt. Die aktuelle Liste der deutschen Großstädte folgt der [2025er Übersicht](https://de.wikipedia.org/wiki/Liste_der_Gro%C3%9Fst%C3%A4dte_in_Deutschland); die Böblinger Kommunen entsprechen der [offiziellen Landkreisübersicht](https://www.lrabb.de/unser-kreis/Staedte%2Bund%2BGemeinden).
