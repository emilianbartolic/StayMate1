# StayMate Sicherheitsprüfung

**Stand: 26.11.2026.** Prüfung des lokalen Demo-Codes anhand der drei Risikosäulen und OWASP ASI01–ASI10. Die Prüfung umfasst Quellcode, Abhängigkeiten und lokale Funktionschecks; sie ist weder Zertifizierung noch unabhängiger Penetrationstest.

## Datenflüsse und Angriffsflächen

- **Private Daten:** Objektfragen, Suchprofil und optional hochgeladene Bilder gehen an den Codex-Dienst der lokalen Installation. Freigegebene Host-Notizen können in den Modellkontext gelangen. Eskalierte Fragen und Host-Antworten werden lokal als Tickets gespeichert. Audit-Ereignisse enthalten Anfrage-ID, Entscheidung, Kategorie, Quellen und Status, aber nicht den vollständigen Gasttext. Demo-Profil, Suchauswahl und Favoriten liegen im Browser-`localStorage`.
- **Drittinhalte:** Gasttexte und Bilder, optionale Anbieterangebote/Beschreibungen sowie freigegebene Host-Notizen. Die Anwendung verbindet keine E-Mail-, Kalender-, Dateiablage-, MCP- oder A2A-Quelle. Öffentliche Inseratsbilder und Anbieterlinks laden Inhalte direkt von deren Domains.
- **Nach außen:** Codex erhält den Antwortkontext über die persönliche lokale Codex-Anmeldung. Bei aktivierter Booking.com-Partnersuche übermittelt der Backend-Adapter Ort, Termine, Belegung und Filter an Booking.com. Der Gast wird darüber im Suchdialog informiert. Host-Tickets werden nicht automatisch an Plattformen gesendet. StayMate bucht oder bezahlt nicht. JSON-Export und Backup sind lokale Host-Aktionen.
- **Rechte und Identität:** Der Backend-Dienst bindet standardmäßig an `127.0.0.1`. Die Host-Verwaltung und vollständigen Objekt-Wissensbasen verlangen ein lokales Host-Konto; erstes zufälliges Host-Passwort und SQLite-Dateien liegen privat unter `user-data/` (`0700` für Verzeichnisse, `0600` für Dateien). Schreibende API-Routen prüfen Origin und CSRF. Öffentlicher Mehrbenutzerbetrieb wird beim Start abgewiesen, solange ein Gastmodellaufruf die Codex-Identität des Serverprozesses verwenden würde.
- **Codex-Grenze:** Gastaufrufe ignorieren die normale Nutzerkonfiguration und Regeldateien und deaktivieren Shell-, Browser-, Computer-, App-, Plugin- und Skill-Suchwerkzeuge. Das Dateiprofil verweigert standardmäßig den Datenträgerzugriff, lässt nur minimale Laufzeitdateien lesen und sperrt temporäre Pfade; Netzwerk für Agentenwerkzeuge ist deaktiviert. Der Modelltransport selbst bleibt ein externer Codex-Datenfluss. Antworttext ist auf 24 KB begrenzt; pro Installation gelten 300 Modellaufrufe/UTC-Tag, zwei gleichzeitige Aufrufe sowie ein Host-Not-Aus. Zeitüberschreitungen beenden den Prozessverbund.

## OWASP Top 10 für Agenten

| Risiko | Befund und derzeitige Grenze |
|---|---|
| **ASI01 Goal Hijack / Prompt Injection** | **Mittel, verbleibend:** Gasttexte, Bilder, Anbieterbeschreibungen und Host-Notizen können weiterhin die Formulierung einer Modellantwort beeinflussen. Sie werden als untrusted Daten markiert; der Gastaufruf hat keine Agentenwerkzeuge, keinen Pluginzugriff und keinen Werkzeug-Netzverkehr. Das verhindert keine falsche oder manipulative Formulierung vollständig. |
| **ASI02 Tool Misuse** | **Niedrig im getesteten lokalen Stand:** Shell-, Browser-, Computer-, App-, Plugin- und Skill-Suchwerkzeuge sind für Gastaufrufe deaktiviert; `CODEX_HOME` und die lokale Codex-Anmeldung bleiben für den Modelltransport nötig. Die CLI-Version wird vom lokalen Betreiber verwaltet und ist nicht im Repository gepinnt. |
| **ASI03 Identity / Privilege Abuse** | **Hoch vor öffentlichem Einsatz, lokal begrenzt:** Host-Endpunkte prüfen die Host-Rolle; lokale Anmeldung, Passwort-Hashing (PBKDF2-HMAC-SHA256, 600.000 Runden), HMAC-gehashte Sitzungstoken, Ablauf und Widerruf sind umgesetzt. Gäste teilen lokal weiterhin die Codex-Identität des betreibenden Rechners; deshalb bleibt Public-Mode gesperrt. |
| **ASI04 Supply Chain** | **Niedrig für Python-Abhängigkeiten, mittel für Codex-CLI:** Python-Zielversion 3.11, 22 exakt gepinnte Pakete mit SHA-256-Hashes in `backend/requirements.lock`; der Laufzeit-`pip-audit` fand keine bekannten Advisories. Codex-CLI und Betriebssystemupdates werden nicht über dieses Lockfile kontrolliert. |
| **ASI05 Unexpected Code Execution** | **Niedrig im getesteten Stand:** Codex bekommt keine Shell-/Codewerkzeuge; Dateizugriff und Agenten-Netz sind zusätzlich im Sandbox-Profil begrenzt. Zeitlimits, Prozessgruppen-Abbruch, tägliches Aufruflimit, Parallelitätsgrenze und begrenzte Antwortgröße sind aktiv. |
| **ASI06 Memory / Context Poisoning** | **Niedrig bis mittel:** Nur Host-freigegebene Notizen kommen in den Kontext. Gastfragen und freigegebene Notizen können Anweisungen enthalten und damit die Antwort beeinflussen; sie können dadurch keine Werkzeuge aufrufen. Tickets/Audit/Backups verfallen nach 90 Tagen, offene Memory-Notizen nach 30 Tagen, freigegebene Notizen nach 365 Tagen. |
| **ASI07 Insecure Inter-Agent Communication** | **Niedrig / nicht angebunden:** Keine A2A-Kommunikation, MCP-Server oder angebundenen Fremdagenten. Gastaufrufe ignorieren Nutzer-/Projektkonfiguration und deaktivieren Plugins. |
| **ASI08 Cascading Failures / Kosten** | **Niedrig bis mittel:** 20 API-Anfragen pro Loopback-IP/Minute, 2 Modellaufrufe gleichzeitig, 300 Modellaufrufe pro UTC-Tag in SQLite, maximal 60/90 Sekunden Laufzeit und Host-Not-Aus. Die Zählung ist kein direktes Token- oder Geldlimit; die In-Process-IP-Grenze wird bei einem Neustart zurückgesetzt. |
| **ASI09 Human-Agent Trust** | **Mittel, verbleibend:** Quellen und Objektfakten werden serverseitig ausgewählt, fiktive Konzepte markiert und Buchungen/Zahlungen unterbleiben. Ein LLM kann trotzdem über die bereitgestellten Fakten hinaus formulieren; hochriskante oder nicht bestätigte Fragen werden an den Host übergeben. |
| **ASI10 Rogue Agents** | **Niedrig im getesteten Stand:** Kein autonomer Dauerlauf und keine externen Schreibaktionen. Der Not-Aus sperrt neue Modellaufrufe; Modell- und Entscheidungsevents bleiben lokal prüfbar. Ein CLI-Upgrade kann diese Grenze verändern und muss erneut geprüft werden. |

## Verbleibende priorisierte Befunde

| Risiko / Bereich | Angriffsszenario | Dringlichkeit / Aufwand | Konkrete Maßnahme |
|---|---|---|---|
| **ASI03 – öffentlicher Betrieb und Identität** | Eine gehostete Instanz würde Anfragen vieler Gäste über die eine Codex-Anmeldung des Hosts senden. | **Hoch vor Veröffentlichung / hoch** | Public-Mode gesperrt lassen. Vor einer Freigabe nutzergebundene, offiziell zugelassene Modellautorisierung, HTTPS/Proxy, Konto-Wiederherstellung, dauerhafte Datenbank und unabhängigen Review ergänzen. |
| **ASI01 + ASI09 – Modellantworten** | Prompt Injection oder missverständliche Fakten führen zu einer überzeugend klingenden, aber unbestätigten Aussage. | **Mittel / mittel** | Faktenantworten in ein enges strukturiertes Schema zwingen, Aussagen gegen Objektquellen nachprüfen und adversariale multilingual Tests ergänzen. Kritische Fragen weiter menschlich bestätigen lassen. |
| **ASI04 – Codex-Lieferkette** | Ein lokales Codex-CLI-Upgrade ändert Flags, Toolangebot oder Sandboxsemantik. | **Mittel / niedrig bis mittel** | Getestete Codex-Version und benötigte Features beim Start protokollieren oder erlaubte Versionen prüfen; nach jedem Update den Prompt-Injection-/Sandbox-Test wiederholen. |
| **ASI08 – Kostenkontrolle** | Wiederholte legitime Anfragen erreichen das Tageslimit und verursachen weiterhin variable Modellkosten bis dahin. | **Niedrig lokal / niedrig** | Bei Bedarf zusätzlich ein Token- oder Ausgabenbudget des Modellanbieters setzen und Warnschwellen im Host-Dashboard anzeigen. Das bestehende Not-Aus bleibt aktiv. |

## Durchgeführte Prüfungen

- `pip-audit` auf der frischen Python-3.11-Laufzeit: **keine bekannten Schwachstellen**; `uv pip check`: **alle 22 Pakete kompatibel**.
- Authentifizierung, Passwortprüfung, Sitzungswiderruf, Chatbesitz und Tickettrennung: **bestanden**.
- SQLite-Memory, Freigabe, Ablaufdaten, Tageskontingent, Ticketantwort, Audit und Backup: **bestanden**.
- Skills-/Objektmatrix: **3.014 von 3.014 Fällen bestanden**. Der Durchlauf fand einen generischen „Apartment“-Treffer, der unbekannte Ausstattungsfragen falsch klassifizierte; der Faktenabgleich wurde eingegrenzt und die Matrix danach erneut vollständig bestanden.
- Live-HTTP-Prüfung am 26.11.2026 mit isolierter Testdatenbank: Startseite und Sicherheitsheader **200**; nicht angemeldete Skill-/Ticket-Verwaltung und vollständige Objekt-Wissensbasen **401**; Backend-, lokale Zugangsdaten- und Git-Dateien **404**; fremder Origin sowie fehlender und ungültiger CSRF-Token **403**; Admin-Anmeldung, Not-Aus, Wiederaufnahme und Abmeldung **bestanden**.
- Eine synthetische Prompt-Injection-Frage erhielt eine deutsche Codex-Antwort; die Gastantwort enthielt weder Skillnamen noch Diagnosefelder. Das ist ein gezielter Funktionstest, kein umfassender Modell-Penetrationstest.
- Synthetisches Bild wurde über den Gastchat an Codex übermittelt und korrekt beschrieben; die Wohnungssuche stellte in einem getrennten Test eine deutschsprachige Rückfrage.
- Die optionale Booking.com-Live-API wurde ohne freigeschaltete Partnerzugangsdaten nicht auf externe Verbindungen getestet.
- Keine unabhängige Prüfung, kein externer Penetrationstest und keine Modellanbieter-/Datenschutzfreigabe durchgeführt. `bandit`, `semgrep`, `gitleaks` und `trufflehog` wurden in diesem Durchlauf nicht ausgeführt.
