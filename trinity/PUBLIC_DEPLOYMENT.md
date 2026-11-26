# Öffentlicher Betrieb: derzeit gesperrt

Die App hat eine Vorstufe für Konten, Rollen, sichere Sitzungen und Chatzuordnung. Sie lässt sich in diesem Stand dennoch **nicht** als öffentlicher Mehrbenutzerdienst starten: Gästeanfragen laufen derzeit über `codex exec` mit der Codex-Anmeldung des Serverprozesses. Das würde die Nutzung des Modells nicht pro Gastkonto trennen und könnte einen geteilten oder unzulässigen Zugang vortäuschen.

`STAYMATE_PUBLIC=1` beendet den Backend-Start daher absichtlich mit einer klaren Fehlermeldung. Entferne diese Sperre nicht, bevor die folgenden Punkte umgesetzt und geprüft sind:

1. Eine offiziell genehmigte, nutzergebundene OpenAI-Anmeldung und der passende Zugriff für gehostete Apps.
2. Tokenaustausch, verschlüsselte Speicherung, Widerruf und Erneuerung der Modellzugänge pro Nutzer.
3. Konto-/Rollenverwaltung, E-Mail-Verifikation, Passwortwiederherstellung, Sitzungsverwaltung und Missbrauchsschutz.
4. HTTPS-Ende-zu-Ende, vertrauenswürdiger Reverse Proxy, persistente Datenbank, Backups und Löschfristen.
5. Unabhängiger Security-Review und Freigabe für den Mehrbenutzerbetrieb.

Die internen Konto-, Passwort- und Sitzungskomponenten in `trinity/hub/accounts.py` sind kein Produktions-Login und werden im Standardbetrieb nicht freigeschaltet. In der Demo bezeichnet „Profil“ weiterhin ein Browserprofil ohne echtes Konto.

## Codex pro Nutzer

Die aktuelle Installation bleibt lokal (`127.0.0.1`) und verwendet die persönliche, lokale Codex-Anmeldung der jeweiligen Person. Für ein Open-Source-Tool, das lokal auf dem Gerät der Nutzer läuft, bietet OpenAI einen separaten Sign-in-/ChatGPT-Plan-Flow. Ein öffentlich gehosteter Dienst braucht eine andere, ausdrücklich zugelassene Integrationsform. Siehe [offizielle OpenAI-Dokumentation zu Codex App Server](https://learn.chatgpt.com/docs/app-server), [Sign in with ChatGPT für Websites](https://developers.openai.com/siwc/website) und [ChatGPT Plan-Nutzung in Open-Source-Apps](https://developers.openai.com/siwc/token-sharing-open-source).
