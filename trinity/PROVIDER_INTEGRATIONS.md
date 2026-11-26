# Anbieter- und Gastnachrichten

StayMate nutzt die Booking.com Demand API ausschließlich für die read-only Unterkunftssuche. Der Adapter ist implementiert, aber ohne freigeschalteten Partnerzugang und geheime Zugangsdaten deaktiviert. Die Einstellungsseite zeigt den Status und fehlende Voraussetzungen, aber keine Zugangsdaten. Diese Suchintegration verwaltet keine Gastgeberobjekte und sendet keine Buchung, Zahlung oder Nachricht.

## Airbnb

Airbnb stellt seine APIs für genehmigte Programme und Software-/Connectivity-Partner bereit. Vor einer technischen Verbindung braucht StayMate ein zugelassenes Partnerkonto, den genehmigten Anwendungsumfang, OAuth-Zugangsdaten und die ausdrückliche Autorisierung für jedes Hostkonto und Inserat. Zugangsdaten allein schalten diese API nicht frei.

Offizielle Einstiegspunkte:

- [Airbnb API Terms and Programs](https://www.airbnb.com/help/article/3418)
- [Airbnb Software Partners](https://www.airbnb.com/software-partners)

## Booking.com

Die Booking.com Connectivity APIs für Verwaltung und Hostverbindungen richten sich an Connectivity-Partner. Produktivzugriff erfordert das Onboarding, API-Token-Maschinenkonten und pro Unterkunft passende, vom Host erteilte Verbindungstypen. Sie sind nicht mit der unten dokumentierten Demand API zur Gästesuche gleichzusetzen.

Offizielle Dokumentation:

- [Connectivity API Übersicht](https://developers.booking.com/connectivity/docs)
- [Connections API und Hostfreigaben](https://developers.booking.com/connectivity/docs/connections-api/connections-overview)
- [Authentifizierung](https://developers.booking.com/connectivity/docs/authentication)
- [Go-live Anforderungen](https://developers.booking.com/connectivity/docs/going_live)

## Booking.com Demand API · Gästesuche

Der implementierte Adapter fragt die Angebote für die vom Gast eingegebene Stadt ab. Mit Anreise und Abreise verwendet er die Suchantwort des Anbieters für Termine, Gäste und Preisfilter; ohne konkrete Termine zeigt er Inseratsdetails, ohne Verfügbarkeit zu behaupten. Objekte ohne verfügbares Anbieterfoto werden ausgelassen. Ein freigeschalteter Partnerzugang, API-Key, Affiliate-ID und vom Konto gelieferte Fotodaten sind erforderlich. Die Zugangsdaten werden nur serverseitig gelesen.

- [Demand API-Authentifizierung](https://developers.booking.com/demand/docs/development-guide/authentication)
- [Suche nach verfügbaren Unterkünften](https://developers.booking.com/demand/docs/accommodations/search-for-available-properties)
- [Inseratsdetails und Fotos](https://developers.booking.com/demand/docs/accommodations/look-accommodation-details)

## Hostbenachrichtigungen

Der lokale Ablauf bleibt eine Host-Warteschlange mit Export und manueller Antwort. Automatische E-Mail- oder Plattformnachrichten sind nicht aktiviert. Für einen echten Versand sind ein gewählter und konfigurierter Zustelldienst, Empfängerfreigaben, Datenschutztexte, Zustell-/Fehlerbehandlung und ein revisionsfähiger Nachweis nötig. Keine Nachricht wird allein durch das Vorhandensein von Konfiguration geheim versendet.

## Umsetzungsstatus

Die Registry zeigt den Status der read-only Booking.com-Angebotssuche und die fehlenden Voraussetzungen an. Airbnb- und Booking.com-Connectivity-Funktionen, Objektverwaltung, Hostbenachrichtigungen, Preis-Synchronisierung und Buchungsabschluss sind nicht integriert. Der Gast bucht weiterhin auf der verlinkten Anbieterseite.
